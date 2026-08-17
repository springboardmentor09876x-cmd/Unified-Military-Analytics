import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# GLOBAL MILITARY FIREPOWER 2025
# Python/Streamlit recreation of the Power BI dashboard
# ============================================================

st.set_page_config(
    page_title="Global Military Firepower 2025",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DATA
# ============================================================

DATA_PATH = Path(__file__).parent / "data" / "military_final.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(DATA_PATH, sheet_name="Wide_Format")
    df.columns = df.columns.str.strip()
    return df

if not DATA_PATH.exists():
    st.error(
        "military_final.xlsx was not found. Put it inside the 'data' "
        "folder next to app.py."
    )
    st.stop()

df = load_data()

# Create a derived field safely. The Excel file does NOT contain
# combined_personnel, so we calculate it from the three existing fields.
df["combined_personnel"] = (
    pd.to_numeric(df["active_personnel"], errors="coerce").fillna(0)
    + pd.to_numeric(df["reserve_personnel"], errors="coerce").fillna(0)
    + pd.to_numeric(df["paramilitary"], errors="coerce").fillna(0)
)

# ============================================================
# HELPERS
# ============================================================

def num(row, column):
    return pd.to_numeric(row[column], errors="coerce") if column in row.index else 0

def money(value):
    value = float(value or 0)
    if abs(value) >= 1_000_000_000_000:
        return f"${value/1_000_000_000_000:.2f}T"
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    return f"${value:,.0f}"

def integer(value):
    return f"{float(value or 0):,.0f}"

def metric_card(label, value, icon=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def section_title(title, subtitle=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)

# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101827 0%, #17243a 100%);
        min-width: 270px;
    }

    [data-testid="stSidebar"] * {
        color: #f7f9fc !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        border-radius: 10px;
        padding: 7px 10px;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #17243a;
        margin-bottom: 3px;
    }

    .main-subtitle {
        color: #667085;
        font-size: 15px;
        margin-bottom: 24px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #17243a;
        margin-top: 20px;
        margin-bottom: 3px;
    }

    .section-subtitle {
        color: #667085;
        margin-bottom: 14px;
    }

    .metric-card {
        background: white;
        border: 1px solid #e5e9f2;
        border-radius: 15px;
        padding: 18px 20px;
        min-height: 105px;
        box-shadow: 0 3px 12px rgba(16, 24, 40, 0.06);
        margin-bottom: 14px;
    }

    .metric-label {
        color: #667085;
        font-size: 13px;
        font-weight: 650;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #17243a;
        font-size: 25px;
        font-weight: 800;
    }

    .info-card {
        background: white;
        border: 1px solid #e5e9f2;
        border-radius: 15px;
        padding: 16px 18px;
        box-shadow: 0 3px 12px rgba(16, 24, 40, 0.05);
        margin-bottom: 12px;
    }

    .info-label {
        color: #667085;
        font-size: 12px;
        margin-bottom: 4px;
    }

    .info-value {
        color: #17243a;
        font-size: 17px;
        font-weight: 700;
    }

    .page-pill {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 20px;
        background: #e8eefc;
        color: #3156a3;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    div[data-testid="stPlotlyChart"] {
        background: white;
        border: 1px solid #e5e9f2;
        border-radius: 15px;
        padding: 8px;
        box-shadow: 0 3px 12px rgba(16, 24, 40, 0.05);
    }

    .footer {
        text-align: center;
        color: #98a2b3;
        font-size: 12px;
        padding: 25px 0 5px;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 650;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# NAVIGATION
# ============================================================

st.sidebar.markdown("## 🌍 Military Analytics")
st.sidebar.caption("Global Military Firepower 2025")

dashboard = st.sidebar.radio(
    "Select Dashboard",
    [
        "Quick Stats",
        "Nation Overview",
        "Compare Power",
        "Coalition Builder"
    ]
)

st.sidebar.divider()
st.sidebar.caption(f"{len(df):,} countries • {len(df.columns)-1:,} source fields")

# ============================================================
# QUICK STATS
# ============================================================

if dashboard == "Quick Stats":

    st.markdown('<div class="page-pill">OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Quick Stats</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Global military strength, budget and ranking overview.</div>',
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("### Filters")

        region_options = sorted(df["region"].dropna().astype(str).unique())
        continent_options = sorted(df["continent"].dropna().astype(str).unique())
        alliance_options = sorted(df["alliance"].dropna().astype(str).unique())
        country_options = sorted(df["country"].dropna().astype(str).unique())

        selected_regions = st.multiselect(
            "Region",
            region_options,
            default=[
                "Eastern Asia",
                "Southern Asia",
                "Eastern Europe",
                "Northern America"
            ],
            key="qs_region"
        )

        selected_continents = st.multiselect(
            "Continent",
            continent_options,
            default=[
                "Asia",
                "Europe",
                "Americas"
            ],
            key="qs_continent"
        )

        selected_alliances = st.multiselect(
            "Alliance",
            alliance_options,
            default=["NATO"],
            key="qs_alliance"
        )
        default_countries = [c for c in ["India", "United States", "China", "Russia"] if c in country_options]

        selected_countries = st.multiselect(
            "Country",
            country_options,
            default=default_countries,
            key="qs_country"
        )

    filtered_df = df.copy()

    if selected_regions:
        filtered_df = filtered_df[filtered_df["region"].astype(str).isin(selected_regions)]
    if selected_continents:
        filtered_df = filtered_df[filtered_df["continent"].astype(str).isin(selected_continents)]
    if selected_alliances:
        filtered_df = filtered_df[filtered_df["alliance"].astype(str).isin(selected_alliances)]
    if selected_countries:
        filtered_df = filtered_df[filtered_df["country"].astype(str).isin(selected_countries)]

    # Aggregations: rank/ratios are averaged for multi-country filters;
    # budgets are summed.
    avg_rank = safe_numeric(filtered_df["power_index_rank"]).mean() if not filtered_df.empty else 0
    avg_ratio = safe_numeric(filtered_df["budget_to_gdp_ratio"]).mean() if not filtered_df.empty else 0
    total_budget = safe_numeric(filtered_df["defense_budget_usd"]).sum()
    avg_gap = safe_numeric(filtered_df["power_index_rank_gap"]).mean() if not filtered_df.empty else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        metric_card("Power Index Rank", integer(avg_rank), "🏅")
    with k2:
        metric_card("Budget-to-GDP Ratio", f"{avg_ratio:.2f}", "📊")
    with k3:
        metric_card("Defense Budget", money(total_budget), "💰")
    with k4:
        metric_card("Power Index Rank Gap", integer(avg_gap), "↔️")

    st.caption(f"Showing {len(filtered_df):,} of {len(df):,} countries.")

    c1, c2 = st.columns(2)

    with c1:
        country_budget = (
            filtered_df.groupby("country", as_index=False)["defense_budget_usd"]
            .sum()
            .sort_values("defense_budget_usd", ascending=False)
            .head(10)
        )
        fig = px.bar(
            country_budget,
            x="defense_budget_usd",
            y="country",
            orientation="h",
            title="Top 10 Countries by Defense Budget",
            text_auto=".3s"
        )
        fig.update_layout(
            xaxis_title="Defense Budget (USD)",
            yaxis_title="",
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        region_budget = (
            filtered_df.groupby("region", as_index=False)["defense_budget_usd"]
            .sum()
            .sort_values("defense_budget_usd", ascending=False)
        )
        fig = px.bar(
            region_budget,
            x="region",
            y="defense_budget_usd",
            title="Defense Budget by Region",
            text_auto=".3s"
        )
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Defense Budget (USD)",
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        continent_count = (
            filtered_df.groupby("continent", as_index=False)["country"]
            .count()
            .rename(columns={"country": "Country Count"})
        )
        fig = px.pie(
            continent_count,
            names="continent",
            values="Country Count",
            hole=0.48,
            title="Countries by Continent"
        )
        fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        rank_data = (
            filtered_df[["country", "power_index_rank"]]
            .dropna()
            .sort_values("power_index_rank", ascending=True)
            .head(10)
        )
        fig = px.bar(
            rank_data,
            x="power_index_rank",
            y="country",
            orientation="h",
            title="Top 10 Power Index Ranks",
            text="power_index_rank"
        )
        fig.update_layout(
            xaxis_title="Power Index Rank",
            yaxis_title="",
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# NATION OVERVIEW
# ============================================================

elif dashboard == "Nation Overview":

    st.markdown('<div class="page-pill">COUNTRY PROFILE</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Nation Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Detailed military, economic and personnel profile for a selected country.</div>',
        unsafe_allow_html=True
    )

    countries = sorted(df["country"].dropna().astype(str).unique())
    selected_country = st.selectbox(
        "Select Country",
        countries,
        key="nation_country"
    )

    selected_nation = df[df["country"].astype(str) == selected_country]
    if selected_nation.empty:
        st.warning("No data found for the selected country.")
        st.stop()

    nation = selected_nation.iloc[0]

    info1, info2, info3, info4 = st.columns(4)
    with info1:
        metric_card("Region", str(nation["region"]), "🌐")
    with info2:
        metric_card("Continent", str(nation["continent"]), "🗺️")
    with info3:
        metric_card("Alliance", str(nation["alliance"]), "🤝")
    with info4:
        metric_card("NATO Flag", integer(nation["nato_flag"]), "🏳️")

    n1, n2, n3, n4 = st.columns(4)
    with n1:
        metric_card("Power Index Rank", integer(nation["power_index_rank"]), "🏅")
    with n2:
        metric_card("Defense Budget", money(nation["defense_budget_usd"]), "💰")
    with n3:
        metric_card("Budget-to-GDP Ratio", f"{float(nation['budget_to_gdp_ratio']):.2f}", "📊")
    with n4:
        metric_card("Assets per Capita", f"{float(nation['assets_per_capita']):,.2f}", "👤")

    section_title(
        f"{selected_country} — Major Military Assets",
        "Core land, air and naval asset counts."
    )

    major_assets = pd.DataFrame({
        "Metric": [
            "Military Aircraft",
            "Military Helicopters",
            "Tanks",
            "Armored Fighting Vehicles",
            "Naval Fleet"
        ],
        "Value": [
            nation["total_military_aircraft"],
            nation["total_military_helicopters"],
            nation["tanks"],
            nation["armored_fighting_vehicles"],
            nation["total_naval_fleet"]
        ]
    })

    fig = px.bar(
        major_assets,
        x="Metric",
        y="Value",
        text="Value",
        title="Major Military Assets"
    )
    fig.update_layout(
        xaxis_title="Asset Type",
        yaxis_title="Count",
        margin=dict(l=10, r=10, t=55, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        air_power = pd.DataFrame({
            "Aircraft Type": [
                "Fighter", "Attack", "Transport", "Trainer",
                "Special Mission", "Tanker", "Attack Helicopters"
            ],
            "Count": [
                nation["fighter_aircraft"],
                nation["attack_aircraft"],
                nation["transport_aircraft"],
                nation["trainer_aircraft"],
                nation["special_mission_aircraft"],
                nation["tanker_aircraft"],
                nation["attack_helicopters"]
            ]
        })
        fig = px.bar(
            air_power,
            x="Aircraft Type",
            y="Count",
            text="Count",
            title="Air Power Profile"
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Aircraft",
            xaxis_tickangle=-30,
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        active = float(nation["active_personnel"])
        reserve = float(nation["reserve_personnel"])
        paramilitary = float(nation["paramilitary"])
        combined = active + reserve + paramilitary

        personnel_data = pd.DataFrame({
            "Personnel Type": [
                "Active Personnel",
                "Reserve Personnel",
                "Paramilitary"
            ],
            "Count": [active, reserve, paramilitary]
        })

        fig = px.bar(
            personnel_data,
            x="Personnel Type",
            y="Count",
            text="Count",
            title="Military Personnel"
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Personnel",
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption(f"Combined personnel: {combined:,.0f}")

    c1, c2 = st.columns(2)

    with c1:
        economic_data = pd.DataFrame({
            "Metric": ["GDP", "Defense Budget"],
            "Value": [nation["gdp"], nation["defense_budget_usd"]]
        })
        fig = px.bar(
            economic_data,
            x="Metric",
            y="Value",
            text_auto=".3s",
            title="Economic Strength"
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="USD",
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Power Index</div>
                <div class="info-value">{float(nation["power_index"]):.4f}</div>
            </div>
            <div class="info-card">
                <div class="info-label">GDP Rank</div>
                <div class="info-value">{integer(nation["gdp_rank"])}</div>
            </div>
            <div class="info-card">
                <div class="info-label">Power Index Rank Gap</div>
                <div class="info-value">{integer(nation["power_index_rank_gap"])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# COMPARE POWER
# ============================================================

elif dashboard == "Compare Power":

    st.markdown('<div class="page-pill">SIDE-BY-SIDE ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Compare Power</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Compare military strength, personnel, aircraft, navy and budget.</div>',
        unsafe_allow_html=True
    )

    countries = sorted(df["country"].dropna().astype(str).unique())

    ca, cb = st.columns(2)
    with ca:
        country_a = st.selectbox(
            "Country A",
            countries,
            index=0,
            key="compare_a"
        )
    with cb:
        default_b = 1 if len(countries) > 1 else 0
        country_b = st.selectbox(
            "Country B",
            countries,
            index=default_b,
            key="compare_b"
        )

    a = df[df["country"].astype(str) == country_a].iloc[0]
    b = df[df["country"].astype(str) == country_b].iloc[0]

    st.markdown(f"### {country_a} vs {country_b}")

    a1, a2, a3, a4 = st.columns(4)
    with a1:
        metric_card(f"{country_a} — Power Rank", integer(a["power_index_rank"]), "🏅")
    with a2:
        metric_card(f"{country_a} — Defense Budget", money(a["defense_budget_usd"]), "💰")
    with a3:
        metric_card(f"{country_a} — Active Personnel", integer(a["active_personnel"]), "👥")
    with a4:
        metric_card(f"{country_a} — Aircraft", integer(a["total_military_aircraft"]), "✈️")

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        metric_card(f"{country_b} — Power Rank", integer(b["power_index_rank"]), "🏅")
    with b2:
        metric_card(f"{country_b} — Defense Budget", money(b["defense_budget_usd"]), "💰")
    with b3:
        metric_card(f"{country_b} — Active Personnel", integer(b["active_personnel"]), "👥")
    with b4:
        metric_card(f"{country_b} — Aircraft", integer(b["total_military_aircraft"]), "✈️")

    comparison = pd.DataFrame({
        "Country": [country_a, country_b],
        "Military Aircraft": [a["total_military_aircraft"], b["total_military_aircraft"]],
        "Naval Fleet": [a["total_naval_fleet"], b["total_naval_fleet"]],
        "Active Personnel": [a["active_personnel"], b["active_personnel"]],
        "Defense Budget": [a["defense_budget_usd"], b["defense_budget_usd"]]
    })

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            comparison,
            x="Country",
            y="Military Aircraft",
            text="Military Aircraft",
            title="Military Aircraft Comparison"
        )
        fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            comparison,
            x="Country",
            y="Naval Fleet",
            text="Naval Fleet",
            title="Naval Fleet Comparison"
        )
        fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        fig = px.bar(
            comparison,
            x="Country",
            y="Active Personnel",
            text="Active Personnel",
            title="Active Personnel Comparison"
        )
        fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        fig = px.bar(
            comparison,
            x="Country",
            y="Defense Budget",
            text="Defense Budget",
            title="Defense Budget Comparison"
        )
        fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# COALITION BUILDER
# ============================================================

elif dashboard == "Coalition Builder":

    st.markdown('<div class="page-pill">MULTI-COUNTRY ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Coalition Builder</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Aggregate selected countries and compare the coalition with a reference country.</div>',
        unsafe_allow_html=True
    )

    countries = sorted(df["country"].dropna().astype(str).unique())

    selected_coalition = st.multiselect(
        "Select Coalition Countries",
        countries,
        key="coalition_countries"
    )

    if not selected_coalition:
        st.info("Select one or more countries to build the coalition.")
    else:
        coalition_df = df[df["country"].astype(str).isin(selected_coalition)].copy()

        coalition_budget = safe_numeric(coalition_df["defense_budget_usd"]).sum()
        coalition_personnel = safe_numeric(coalition_df["active_personnel"]).sum()
        coalition_aircraft = safe_numeric(coalition_df["total_military_aircraft"]).sum()
        coalition_naval = safe_numeric(coalition_df["total_naval_fleet"]).sum()

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            metric_card("Total Defense Budget", money(coalition_budget), "💰")
        with k2:
            metric_card("Total Active Personnel", integer(coalition_personnel), "👥")
        with k3:
            metric_card("Total Aircraft", integer(coalition_aircraft), "✈️")
        with k4:
            metric_card("Total Naval Fleet", integer(coalition_naval), "⚓")

        reference_country = st.selectbox(
            "Select Reference Country",
            countries,
            key="reference_country"
        )

        reference = df[df["country"].astype(str) == reference_country].iloc[0]

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            metric_card("Reference Defense Budget", money(reference["defense_budget_usd"]), "💰")
        with r2:
            metric_card("Reference Active Personnel", integer(reference["active_personnel"]), "👥")
        with r3:
            metric_card("Reference Aircraft", integer(reference["total_military_aircraft"]), "✈️")
        with r4:
            metric_card("Reference Naval Fleet", integer(reference["total_naval_fleet"]), "⚓")

        comparison = pd.DataFrame({
            "Group": ["Coalition", reference_country],
            "Defense Budget": [coalition_budget, reference["defense_budget_usd"]],
            "Personnel": [coalition_personnel, reference["active_personnel"]],
            "Aircraft": [coalition_aircraft, reference["total_military_aircraft"]],
            "Naval Fleet": [coalition_naval, reference["total_naval_fleet"]]
        })

        c1, c2 = st.columns(2)

        with c1:
            fig = px.bar(
                comparison,
                x="Group",
                y="Defense Budget",
                text="Defense Budget",
                title="Coalition vs Reference — Defense Budget"
            )
            fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.bar(
                comparison,
                x="Group",
                y="Personnel",
                text="Personnel",
                title="Coalition vs Reference — Personnel"
            )
            fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)

        c3, c4 = st.columns(2)

        with c3:
            fig = px.bar(
                comparison,
                x="Group",
                y="Aircraft",
                text="Aircraft",
                title="Coalition vs Reference — Aircraft"
            )
            fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with c4:
            fig = px.bar(
                comparison,
                x="Group",
                y="Naval Fleet",
                text="Naval Fleet",
                title="Coalition vs Reference — Naval Fleet"
            )
            fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)

st.markdown(
    '<div class="footer">Global Military Firepower 2025 • Built with Python, Streamlit, Pandas and Plotly</div>',
    unsafe_allow_html=True
)
