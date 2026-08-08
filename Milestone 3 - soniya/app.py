"""
app.py
------
Unified Military Analytics Dashboard - Streamlit app.

Currently implements: Quick Stats tab.
Nation Overview / Compare Powers / Coalition Builder are stubbed in as
placeholders so the navigation structure is already in place for the
next build steps.

Usage:
    streamlit run app.py

Requires:
    pip install streamlit pandas openpyxl plotly
"""

import os
import pandas as pd
import plotly.express as px
import streamlit as st

# Resolve the data file relative to THIS script's own location, not the
# current working directory. Locally, `streamlit run app.py` is launched
# from inside dashboard/, so cwd = dashboard/. On Streamlit Cloud, the app
# is launched from the repo root instead, so cwd is different there. Using
# __file__ makes this work correctly in both places.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "..", "data", "military_final.xlsx")

st.set_page_config(
    page_title="Global Military Firepower 2026",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_FILE, sheet_name="Master")
    return df


def render_quick_stats(df: pd.DataFrame):
    st.title("🌍 Global Military Firepower 2026")
    st.caption("Quick Stats — global overview of rankings, trends, and highlights")

    # --- Filters -----------------------------------------------------
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        continents = sorted(df["continent"].dropna().unique())
        selected_continents = st.multiselect("Continent", continents, default=continents)

    with col_f2:
        regions_available = sorted(
            df[df["continent"].isin(selected_continents)]["region"].dropna().unique()
        )
        selected_regions = st.multiselect("Region", regions_available, default=regions_available)

    with col_f3:
        nato_only = st.checkbox("NATO members only", value=False)

    filtered = df[
        df["continent"].isin(selected_continents) & df["region"].isin(selected_regions)
    ]
    if nato_only:
        filtered = filtered[filtered["alliance"] == "NATO"]

    if filtered.empty:
        st.warning("No countries match the selected filters.")
        return

    # --- KPI cards -----------------------------------------------------
    st.subheader("At a Glance")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Countries shown", len(filtered))
    k2.metric("Total defense budget (USD)", f"${filtered['defense_budget_usd'].sum():,.0f}")
    k3.metric("Total active personnel", f"{filtered['active_personnel'].sum():,.0f}")
    k4.metric("Total military aircraft", f"{filtered['total_military_aircraft'].sum():,.0f}")

    st.divider()

    # --- Top 10 by Power Index (lower rank number = stronger) ---------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 by Power Index")
        top10_power = filtered.nsmallest(10, "power_index_rank").sort_values("power_index_rank")
        fig = px.bar(
            top10_power,
            x="power_index_score",
            y="country",
            orientation="h",
            title=None,
            labels={"power_index_score": "Power Index Score (lower = stronger)", "country": ""},
        )
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 by Defense Budget (USD)")
        top10_budget = filtered.nlargest(10, "defense_budget_usd").sort_values(
            "defense_budget_usd", ascending=True
        )
        fig2 = px.bar(
            top10_budget,
            x="defense_budget_usd",
            y="country",
            orientation="h",
            labels={"defense_budget_usd": "Defense Budget (USD)", "country": ""},
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # --- Top 10 by military assets (aircraft + tanks + naval fleet) ---
    st.subheader("Top 10 by Total Military Assets")
    filtered = filtered.copy()
    filtered["total_assets"] = (
        filtered["total_military_aircraft"].fillna(0)
        + filtered["tanks"].fillna(0)
        + filtered["total_naval_fleet"].fillna(0)
    )
    top10_assets = filtered.nlargest(10, "total_assets").sort_values("total_assets", ascending=True)
    fig3 = px.bar(
        top10_assets,
        x="total_assets",
        y="country",
        orientation="h",
        labels={"total_assets": "Aircraft + Tanks + Naval Fleet", "country": ""},
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # --- Full table -----------------------------------------------------
    with st.expander("View full filtered data table"):
        st.dataframe(
            filtered[
                [
                    "country", "power_index_rank", "power_index_score",
                    "continent", "region", "alliance",
                    "defense_budget_usd", "active_personnel",
                    "total_military_aircraft", "tanks", "total_naval_fleet",
                ]
            ].sort_values("power_index_rank"),
            use_container_width=True,
            hide_index=True,
        )


RANK_COLUMNS = {
    "power_index_score": False,   # lower score = stronger, so ascending=True for rank
    "total_population": True,
    "active_personnel": True,
    "total_military_aircraft": True,
    "tanks": True,
    "total_naval_fleet": True,
    "defense_budget_usd": True,
    "gdp_usd": True,
}


@st.cache_data
def compute_ranks(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a '<col>_rank_of_n' column for every metric in RANK_COLUMNS."""
    ranked = df.copy()
    total = df["country"].notna().sum()
    for col, higher_is_better in RANK_COLUMNS.items():
        ranked[f"{col}_rank"] = df[col].rank(ascending=not higher_is_better, method="min")
    ranked.attrs["total_countries"] = total
    return ranked


def metric_with_rank(label: str, value_str: str, rank_val, total: int):
    if pd.isna(rank_val):
        st.metric(label, value_str, help="Rank unavailable (missing data)")
    else:
        st.metric(label, value_str, help=f"Rank {int(rank_val)} of {total}")


def render_nation_overview(df: pd.DataFrame):
    st.title("🏳️ Nation Overview")
    st.caption("Detailed analysis of an individual country's capabilities")

    ranked = compute_ranks(df)
    total = ranked.attrs["total_countries"]

    country = st.selectbox("Select a country", sorted(ranked["country"].dropna().unique()))
    row = ranked[ranked["country"] == country].iloc[0]

    # --- Header line: continent / region / alliance --------------------
    tags = [str(row["continent"]), str(row["region"])]
    if row["alliance"] == "NATO":
        tags.append("NATO member")
    st.write(" · ".join(t for t in tags if t and t != "nan"))

    # --- Headline KPIs ---------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Power Index Rank", f"{int(row['power_index_rank'])} of {total}")
    k2.metric("Power Index Score", f"{row['power_index_score']:.4f}" if pd.notna(row["power_index_score"]) else "N/A")
    gdp_rank_str = f"{int(row['gdp_rank'])} of {total}" if pd.notna(row["gdp_rank"]) else "N/A"
    k3.metric("GDP Rank", gdp_rank_str)
    gap = row["power_index_rank_gap"]
    k4.metric(
        "Power Index Rank Gap",
        f"{gap:+.0f}" if pd.notna(gap) else "N/A",
        help="GDP rank minus Power Index rank. Positive = punching above its economic weight militarily.",
    )

    st.divider()

    # --- Radar chart: relative strength across 5 categories ------------
    st.subheader("Capability Profile (percentile vs. all countries)")
    radar_metrics = {
        "Manpower": df["active_personnel"].fillna(0) + df["reserve_personnel"].fillna(0),
        "Air Power": df["total_military_aircraft"].fillna(0),
        "Land Power": (
            df["tanks"].fillna(0) + df["armored_fighting_vehicles"].fillna(0)
            + df["self_propelled_artillery"].fillna(0) + df["towed_artillery"].fillna(0)
        ),
        "Naval Power": df["total_naval_fleet"].fillna(0),
        "Economic Power": df["defense_budget_usd"].fillna(0),
    }
    percentiles = {}
    idx = df.index[df["country"] == country][0]
    for name, series in radar_metrics.items():
        percentiles[name] = series.rank(pct=True)[idx] * 100

    radar_df = pd.DataFrame({
        "Category": list(percentiles.keys()) + [list(percentiles.keys())[0]],
        "Percentile": list(percentiles.values()) + [list(percentiles.values())[0]],
    })
    fig_radar = px.line_polar(radar_df, r="Percentile", theta="Category", line_close=True)
    fig_radar.update_traces(fill="toself")
    fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0, 100])), showlegend=False)
    st.plotly_chart(fig_radar, use_container_width=True)
    st.caption("100 = strongest in that category among all 145 countries, 0 = weakest.")

    st.divider()

    # --- Category breakdowns in tabs ------------------------------------
    tab_manpower, tab_air, tab_land, tab_navy, tab_finance = st.tabs(
        ["Manpower", "Air Power", "Land Forces", "Navy", "Finance"]
    )

    with tab_manpower:
        c1, c2 = st.columns(2)
        with c1:
            metric_with_rank("Total Population", f"{row['total_population']:,.0f}" if pd.notna(row["total_population"]) else "N/A",
                              row.get("total_population_rank"), total)
            metric_with_rank("Active Personnel", f"{row['active_personnel']:,.0f}" if pd.notna(row["active_personnel"]) else "N/A",
                              row.get("active_personnel_rank"), total)
        with c2:
            st.metric("Reserve Personnel", f"{row['reserve_personnel']:,.0f}" if pd.notna(row["reserve_personnel"]) else "N/A")
            st.metric("Paramilitary", f"{row['paramilitary']:,.0f}" if pd.notna(row["paramilitary"]) else "N/A")
        manpower_bar = pd.DataFrame({
            "Category": ["Active", "Reserve", "Paramilitary"],
            "Personnel": [row["active_personnel"], row["reserve_personnel"], row["paramilitary"]],
        })
        st.plotly_chart(px.bar(manpower_bar, x="Category", y="Personnel"), use_container_width=True)

    with tab_air:
        metric_with_rank("Total Military Aircraft", f"{row['total_military_aircraft']:,.0f}" if pd.notna(row["total_military_aircraft"]) else "N/A",
                          row.get("total_military_aircraft_rank"), total)
        air_bar = pd.DataFrame({
            "Category": ["Fighters", "Attack", "Transport", "Trainer", "Special Mission", "Tanker", "Helicopters", "Attack Helicopters"],
            "Count": [
                row["fighter_aircraft"], row["attack_aircraft"], row["transport_aircraft"],
                row["trainer_aircraft"], row["special_mission_aircraft"], row["tanker_aircraft"],
                row["total_military_helicopters"], row["attack_helicopters"],
            ],
        })
        st.plotly_chart(px.bar(air_bar, x="Category", y="Count"), use_container_width=True)

    with tab_land:
        metric_with_rank("Tanks", f"{row['tanks']:,.0f}" if pd.notna(row["tanks"]) else "N/A",
                          row.get("tanks_rank"), total)
        land_bar = pd.DataFrame({
            "Category": ["Tanks", "Armored Fighting Vehicles", "Self-Propelled Artillery", "Towed Artillery", "Rocket Projectors"],
            "Count": [
                row["tanks"], row["armored_fighting_vehicles"], row["self_propelled_artillery"],
                row["towed_artillery"], row["rocket_projectors"],
            ],
        })
        st.plotly_chart(px.bar(land_bar, x="Category", y="Count"), use_container_width=True)

    with tab_navy:
        metric_with_rank("Total Naval Fleet", f"{row['total_naval_fleet']:,.0f}" if pd.notna(row["total_naval_fleet"]) else "N/A",
                          row.get("total_naval_fleet_rank"), total)
        navy_bar = pd.DataFrame({
            "Category": ["Aircraft Carriers", "Helicopter Carriers", "Submarines", "Destroyers", "Frigates", "Corvettes", "Coastal Patrol", "Mine Warfare"],
            "Count": [
                row["aircraft_carriers"], row["helicopter_carriers"], row["submarines"],
                row["destroyers"], row["frigates"], row["corvettes"],
                row["coastal_patrol_craft"], row["mine_warfare_craft"],
            ],
        })
        st.plotly_chart(px.bar(navy_bar, x="Category", y="Count"), use_container_width=True)

    with tab_finance:
        c1, c2 = st.columns(2)
        with c1:
            metric_with_rank("Defense Budget (USD)", f"${row['defense_budget_usd']:,.0f}" if pd.notna(row["defense_budget_usd"]) else "N/A",
                              row.get("defense_budget_usd_rank"), total)
            metric_with_rank("GDP (USD)", f"${row['gdp_usd']:,.0f}" if pd.notna(row["gdp_usd"]) else "N/A",
                              row.get("gdp_usd_rank"), total)
        with c2:
            st.metric("Budget-to-GDP Ratio", f"{row['budget_to_gdp_ratio']:.2%}" if pd.notna(row["budget_to_gdp_ratio"]) else "N/A")
            st.metric("Purchasing Power Parity (USD)", f"${row['purchasing_power_parity_usd']:,.0f}" if pd.notna(row["purchasing_power_parity_usd"]) else "N/A")


COMPARISON_METRICS = [
    # (Display label, column, higher_is_better, format string)
    ("Power Index Rank", "power_index_rank", False, "{:.0f}"),
    ("Power Index Score", "power_index_score", False, "{:.4f}"),
    ("Total Population", "total_population", True, "{:,.0f}"),
    ("Active Personnel", "active_personnel", True, "{:,.0f}"),
    ("Reserve Personnel", "reserve_personnel", True, "{:,.0f}"),
    ("Total Military Aircraft", "total_military_aircraft", True, "{:,.0f}"),
    ("Tanks", "tanks", True, "{:,.0f}"),
    ("Total Naval Fleet", "total_naval_fleet", True, "{:,.0f}"),
    ("Defense Budget (USD)", "defense_budget_usd", True, "${:,.0f}"),
    ("GDP (USD)", "gdp_usd", True, "${:,.0f}"),
    ("Budget-to-GDP Ratio", "budget_to_gdp_ratio", True, "{:.2%}"),
    ("Assets per Capita", "assets_per_capita", True, "{:.6f}"),
]


def _fmt(value, fmt):
    if pd.isna(value):
        return "N/A"
    return fmt.format(value)


def _winner_mark(val_a, val_b, higher_is_better):
    """Returns (mark_a, mark_b) — a checkmark next to whichever value wins."""
    if pd.isna(val_a) or pd.isna(val_b) or val_a == val_b:
        return "", ""
    a_wins = (val_a > val_b) if higher_is_better else (val_a < val_b)
    return ("✅", "") if a_wins else ("", "✅")


def grouped_bar(row_a, row_b, name_a, name_b, categories: dict, y_title: str):
    """categories: {display label: column name}"""
    records = []
    for label, col in categories.items():
        records.append({"Category": label, "Country": name_a, "Count": row_a.get(col, 0) or 0})
        records.append({"Category": label, "Country": name_b, "Count": row_b.get(col, 0) or 0})
    chart_df = pd.DataFrame(records)
    fig = px.bar(chart_df, x="Category", y="Count", color="Country", barmode="group")
    fig.update_layout(yaxis_title=y_title)
    st.plotly_chart(fig, use_container_width=True)


def render_compare_powers(df: pd.DataFrame):
    st.title("⚖️ Compare Powers")
    st.caption("Side-by-side military and economic comparison")

    countries = sorted(df["country"].dropna().unique())
    default_a = countries.index("United States") if "United States" in countries else 0
    default_b = countries.index("China") if "China" in countries else min(1, len(countries) - 1)

    col_a, col_b = st.columns(2)
    with col_a:
        country_a = st.selectbox("Country A", countries, index=default_a, key="cmp_a")
    with col_b:
        country_b = st.selectbox("Country B", countries, index=default_b, key="cmp_b")

    if country_a == country_b:
        st.warning("Pick two different countries to compare.")
        return

    row_a = df[df["country"] == country_a].iloc[0]
    row_b = df[df["country"] == country_b].iloc[0]

    st.divider()

    # --- Headline comparison table --------------------------------------
    st.subheader("Headline Comparison")
    table_rows = []
    for label, col, higher_is_better, fmt in COMPARISON_METRICS:
        val_a, val_b = row_a.get(col), row_b.get(col)
        mark_a, mark_b = _winner_mark(val_a, val_b, higher_is_better)
        table_rows.append({
            "Metric": label,
            country_a: f"{_fmt(val_a, fmt)} {mark_a}".strip(),
            country_b: f"{_fmt(val_b, fmt)} {mark_b}".strip(),
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
    st.caption("✅ marks the stronger value for each metric. Power Index Rank/Score: lower is stronger.")

    st.divider()

    # --- Category breakdown charts ---------------------------------------
    tab_manpower, tab_air, tab_land, tab_navy = st.tabs(
        ["Manpower", "Air Power", "Land Forces", "Navy"]
    )

    with tab_manpower:
        grouped_bar(row_a, row_b, country_a, country_b, {
            "Active": "active_personnel", "Reserve": "reserve_personnel", "Paramilitary": "paramilitary",
        }, "Personnel")

    with tab_air:
        grouped_bar(row_a, row_b, country_a, country_b, {
            "Fighters": "fighter_aircraft", "Attack": "attack_aircraft", "Transport": "transport_aircraft",
            "Trainer": "trainer_aircraft", "Helicopters": "total_military_helicopters",
        }, "Aircraft")

    with tab_land:
        grouped_bar(row_a, row_b, country_a, country_b, {
            "Tanks": "tanks", "Armored Fighting Vehicles": "armored_fighting_vehicles",
            "Self-Propelled Artillery": "self_propelled_artillery", "Towed Artillery": "towed_artillery",
            "Rocket Projectors": "rocket_projectors",
        }, "Units")

    with tab_navy:
        grouped_bar(row_a, row_b, country_a, country_b, {
            "Aircraft Carriers": "aircraft_carriers", "Submarines": "submarines",
            "Destroyers": "destroyers", "Frigates": "frigates", "Corvettes": "corvettes",
        }, "Vessels")


COALITION_SUM_COLS = [
    "total_population", "active_personnel", "reserve_personnel", "paramilitary",
    "total_military_aircraft", "fighter_aircraft", "attack_aircraft", "transport_aircraft",
    "trainer_aircraft", "total_military_helicopters",
    "tanks", "armored_fighting_vehicles", "self_propelled_artillery", "towed_artillery", "rocket_projectors",
    "total_naval_fleet", "aircraft_carriers", "submarines", "destroyers", "frigates", "corvettes",
    "defense_budget_usd", "gdp_usd",
]

COALITION_METRICS = [
    # (Display label, key, higher_is_better, format string)
    ("Strongest Member's Power Index Rank", "best_rank", False, "{:.0f}"),
    ("Average Power Index Score", "avg_score", False, "{:.4f}"),
    ("Total Population", "total_population", True, "{:,.0f}"),
    ("Active Personnel", "active_personnel", True, "{:,.0f}"),
    ("Reserve Personnel", "reserve_personnel", True, "{:,.0f}"),
    ("Total Military Aircraft", "total_military_aircraft", True, "{:,.0f}"),
    ("Tanks", "tanks", True, "{:,.0f}"),
    ("Total Naval Fleet", "total_naval_fleet", True, "{:,.0f}"),
    ("Combined Defense Budget (USD)", "defense_budget_usd", True, "${:,.0f}"),
    ("Combined GDP (USD)", "gdp_usd", True, "${:,.0f}"),
]


def aggregate_coalition(df: pd.DataFrame, countries: list) -> dict:
    subset = df[df["country"].isin(countries)]
    agg = subset[COALITION_SUM_COLS].sum(min_count=1).to_dict()
    agg["best_rank"] = subset["power_index_rank"].min()
    agg["avg_score"] = subset["power_index_score"].mean()
    agg["member_count"] = len(subset)
    return agg


def render_coalition_builder(df: pd.DataFrame):
    st.title("🤝 Coalition Builder")
    st.caption("Interactive simulation of alliance strength and combined assets")

    all_countries = sorted(df["country"].dropna().unique())
    nato_members = sorted(df[df["alliance"] == "NATO"]["country"].dropna().unique())

    st.subheader("Step 1 — Build Coalition A")
    preset = st.radio(
        "Quick start", ["Custom selection", "All NATO members"],
        horizontal=True, key="coalition_preset",
    )
    default_a = nato_members if preset == "All NATO members" else []
    coalition_a = st.multiselect("Coalition A members", all_countries, default=default_a, key="coalition_a")

    if len(coalition_a) == 0:
        st.info("Select at least one country to build Coalition A.")
        return

    st.subheader("Step 2 — Compare against")
    compare_mode = st.radio(
        "Comparison type", ["Single reference country", "Another coalition"],
        horizontal=True, key="coalition_compare_mode",
    )

    remaining = [c for c in all_countries if c not in coalition_a]
    if compare_mode == "Single reference country":
        default_ref = remaining.index("United States") if "United States" in remaining else 0
        ref_country = st.selectbox("Reference country", remaining, index=default_ref, key="coalition_ref")
        coalition_b = [ref_country]
        label_b = ref_country
    else:
        coalition_b = st.multiselect("Coalition B members", remaining, key="coalition_b")
        label_b = "Coalition B"
        if not coalition_b:
            st.info("Select at least one country for Coalition B.")
            return

    label_a = "Coalition A"
    agg_a = aggregate_coalition(df, coalition_a)
    agg_b = aggregate_coalition(df, coalition_b)

    st.divider()
    st.subheader(f"{label_a} ({len(coalition_a)} countries)  vs  {label_b} ({len(coalition_b)} countries)")

    col_mem_a, col_mem_b = st.columns(2)
    with col_mem_a:
        with st.expander(f"{label_a} members"):
            st.write(", ".join(coalition_a))
    with col_mem_b:
        with st.expander(f"{label_b} members"):
            st.write(", ".join(coalition_b))

    # --- Comparison table -------------------------------------------------
    table_rows = []
    for label, key, higher_is_better, fmt in COALITION_METRICS:
        val_a, val_b = agg_a.get(key), agg_b.get(key)
        mark_a, mark_b = _winner_mark(val_a, val_b, higher_is_better)
        table_rows.append({
            "Metric": label,
            label_a: f"{_fmt(val_a, fmt)} {mark_a}".strip(),
            label_b: f"{_fmt(val_b, fmt)} {mark_b}".strip(),
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
    st.caption("✅ marks the stronger side for each metric. Rank/Score: lower is stronger.")

    st.divider()

    # --- Category breakdown charts -----------------------------------------
    tab_manpower, tab_air, tab_land, tab_navy = st.tabs(
        ["Manpower", "Air Power", "Land Forces", "Navy"]
    )

    with tab_manpower:
        grouped_bar(agg_a, agg_b, label_a, label_b, {
            "Active": "active_personnel", "Reserve": "reserve_personnel", "Paramilitary": "paramilitary",
        }, "Personnel")

    with tab_air:
        grouped_bar(agg_a, agg_b, label_a, label_b, {
            "Fighters": "fighter_aircraft", "Attack": "attack_aircraft", "Transport": "transport_aircraft",
            "Trainer": "trainer_aircraft", "Helicopters": "total_military_helicopters",
        }, "Aircraft")

    with tab_land:
        grouped_bar(agg_a, agg_b, label_a, label_b, {
            "Tanks": "tanks", "Armored Fighting Vehicles": "armored_fighting_vehicles",
            "Self-Propelled Artillery": "self_propelled_artillery", "Towed Artillery": "towed_artillery",
            "Rocket Projectors": "rocket_projectors",
        }, "Units")

    with tab_navy:
        grouped_bar(agg_a, agg_b, label_a, label_b, {
            "Aircraft Carriers": "aircraft_carriers", "Submarines": "submarines",
            "Destroyers": "destroyers", "Frigates": "frigates", "Corvettes": "corvettes",
        }, "Vessels")


def main():
    df = load_data()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Quick Stats", "Nation Overview", "Compare Powers", "Coalition Builder"],
    )

    if page == "Quick Stats":
        render_quick_stats(df)
    elif page == "Nation Overview":
        render_nation_overview(df)
    elif page == "Compare Powers":
        render_compare_powers(df)
    elif page == "Coalition Builder":
        render_coalition_builder(df)


if __name__ == "__main__":
    main()
