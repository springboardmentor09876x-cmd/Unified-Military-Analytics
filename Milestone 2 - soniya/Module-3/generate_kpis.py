"""
generate_kpis.py
-----------------
Module 3 deliverable: KPI Engineering and metadata enrichment.

Takes the already-scraped Master dataset (GFP_Military_Dashboard.xlsx) and
enriches it using Military_Dataset_Lookups.xlsx, then computes the
remaining KPI: power_index_rank_gap.

Fills in these previously-empty columns on the Master sheet:
    - region
    - continent
    - alliance          (NATO flag)
    - gdp_usd           (most recent available year per country)
    - power_index_rank_gap

Output: military_final.xlsx (single enriched Master table)

Usage:
    python generate_kpis.py
"""

import pandas as pd

SOURCE_FILE = "GFP_Military_Dashboard.xlsx"
LOOKUPS_FILE = "Military_Dataset_Lookups.xlsx"
OUTPUT_FILE = "military_final.xlsx"

# ---------------------------------------------------------------------------
# Manual name-mapping tables.
# The Master sheet's country names don't always match the lookup files'
# naming conventions (e.g. World Bank uses "Korea, Rep." for South Korea).
# Every mismatch found during inspection is mapped here explicitly.
# ---------------------------------------------------------------------------
CONTINENT_REGION_NAME_MAP = {
    "Beliz": "Belize",
    "Bosnia and Herzegovina": "Bosnia And Herzegovina",
    "Czechia": "Czech Republic",
    "Democratic Republic of the Congo": "Congo (Democratic Republic Of The)",
    "Ivory Coast": "Côte D'Ivoire",
    "North Macedonia": "Macedonia",
    "Republic of the Congo": "Congo",
    "Turkiye": "Turkey",
    # Kosovo and North Korea are not present in the lookup file at all
    # (both have disputed/limited international recognition and are
    # commonly excluded from ISO-based country lists). Filled manually below.
}

# Countries absent from the lookup entirely — filled by hand.
MANUAL_CONTINENT_REGION = {
    "Kosovo": ("Europe", "Southern Europe"),
    "North Korea": ("Asia", "Eastern Asia"),
}

GDP_NAME_MAP = {
    "Beliz": "Belize",
    "Democratic Republic of the Congo": "Congo, Dem. Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Iran": "Iran, Islamic Rep.",
    "Ivory Coast": "Cote d'Ivoire",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Laos": "Lao PDR",
    "Republic of the Congo": "Congo, Rep.",
    "Russia": "Russian Federation",
    "Slovakia": "Slovak Republic",
    "South Korea": "Korea, Rep.",
    "Syria": "Syrian Arab Republic",
    "Venezuela": "Venezuela, RB",
    "Yemen": "Yemen, Rep.",
    # North Korea and Taiwan are not tracked by the World Bank GDP series
    # used here — their gdp_usd (and any KPI that depends on it, i.e.
    # budget_to_gdp_ratio and power_index_rank_gap) will be left blank.
}

NATO_NAME_MAP = {
    "Czechia": "Czech Republic",
    # The lookup file's Turkiye entry is mojibake (encoding corruption):
    # the raw string is "TÃ¼rkiye" instead of "Türkiye". Mapped directly.
    "Turkiye": "TÃ¼rkiye",
}


def load_data():
    master = pd.read_excel(SOURCE_FILE, sheet_name="Master")
    continent_region = pd.read_excel(LOOKUPS_FILE, sheet_name="Continent & Region")
    gdp = pd.read_excel(LOOKUPS_FILE, sheet_name="GDP - 1")
    nato = pd.read_excel(LOOKUPS_FILE, sheet_name="NATO Alliance")
    return master, continent_region, gdp, nato


def build_continent_region_lookup(continent_region: pd.DataFrame) -> dict:
    """country -> (continent, region)"""
    lookup = {
        row["Country"]: (row["Continent"], row["Region"])
        for _, row in continent_region.iterrows()
    }
    lookup.update(MANUAL_CONTINENT_REGION)
    return lookup


def build_gdp_lookup(gdp: pd.DataFrame) -> dict:
    """country -> most recent available GDP (USD)"""
    latest = gdp.sort_values("Year").groupby("Country").last()
    return latest["GDP"].to_dict()


def enrich(master: pd.DataFrame, continent_region: pd.DataFrame,
           gdp: pd.DataFrame, nato: pd.DataFrame) -> pd.DataFrame:
    cr_lookup = build_continent_region_lookup(continent_region)
    gdp_lookup = build_gdp_lookup(gdp)
    nato_members = set(nato.iloc[:, 0].dropna())
    nato_members = {NATO_NAME_MAP.get(c, c) for c in nato_members}
    # also add reverse-mapped master-side names so both spellings match
    nato_members |= {c for c in NATO_NAME_MAP if NATO_NAME_MAP[c] in nato.iloc[:, 0].values}

    def get_continent_region(country):
        key = CONTINENT_REGION_NAME_MAP.get(country, country)
        return cr_lookup.get(key, (None, None))

    def get_gdp(country):
        key = GDP_NAME_MAP.get(country, country)
        return gdp_lookup.get(key)

    def get_alliance(country):
        # Check both the master-side name and the NATO-list-side mapped name
        mapped = NATO_NAME_MAP.get(country, country)
        return "NATO" if (country in nato_members or mapped in nato_members) else None

    master["continent"] = master["country"].apply(lambda c: get_continent_region(c)[0])
    master["region"] = master["country"].apply(lambda c: get_continent_region(c)[1])
    master["gdp_usd"] = master["country"].apply(get_gdp)
    master["alliance"] = master["country"].apply(get_alliance)

    # power_index_rank_gap: compares each country's GDP rank against its
    # Power Index rank. Positive = punching above its economic weight
    # militarily; negative = military rank lags its economic size.
    # Assumption (not specified in the original brief): gdp_rank is computed
    # only among countries with known GDP; countries missing gdp_usd
    # (North Korea, Taiwan) get a blank rank_gap.
    master["gdp_rank"] = master["gdp_usd"].rank(ascending=False, method="min")
    master["power_index_rank_gap"] = master["gdp_rank"] - master["power_index_rank"]

    return master


def main():
    master, continent_region, gdp, nato = load_data()
    enriched = enrich(master, continent_region, gdp, nato)

    missing_gdp = enriched[enriched["gdp_usd"].isna()]["country"].tolist()
    missing_cr = enriched[enriched["continent"].isna()]["country"].tolist()
    print(f"Rows: {len(enriched)}")
    print(f"Countries missing GDP (and therefore rank_gap/budget_to_gdp): {missing_gdp}")
    print(f"Countries missing continent/region: {missing_cr}")

    enriched.to_excel(OUTPUT_FILE, sheet_name="Master", index=False)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
