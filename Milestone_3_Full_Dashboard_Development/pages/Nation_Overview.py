"""
pages/nation_overview.py
-------------------------
Unified Military Analytics and Comparison Dashboard
Module 5 - Dashboard Development (Nation Overview Dashboard)

This is a Streamlit multipage "page" -- it is automatically picked up from
the sidebar navigation because it lives inside pages/. It does NOT call
st.set_page_config() (that already happens once, in the main app.py).

Reuses utils.py for data loading/formatting (same cached dataset as the
Quick Stats dashboard). charts.py is not used for theme constants on this
page -- the premium dark navy/violet/magenta/cyan palette below is local to
this file so it can be restyled independently. All chart-building logic
specific to this page lives locally in this file.

No st.dataframe() / st.table() / pyarrow anywhere on this page either --
any tabular output uses the same pandas-to-HTML approach as the main app.
"""

import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# MAKE SURE utils.py / charts.py (in the project root) ARE IMPORTABLE
# ---------------------------------------------------------------------------
try:
    import utils
    import charts
except ImportError:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
    import utils
    import charts

# ---------------------------------------------------------------------------
# THEME -- Premium midnight navy / violet / magenta / cyan intelligence
# dashboard palette. These are LOCAL display constants for this page only;
# they do not touch utils.py, charts.py, or any data/calculation logic.
# ---------------------------------------------------------------------------
BG_DARK = "#070B16"
BG_DARK_2 = "#0D1324"
BG_CARD = "#10152B"
BG_CARD_2 = "#161B3A"

PURPLE_1 = "#5A2E9C"
PURPLE_2 = "#6A38B8"
PURPLE_3 = "#7C4DFF"   # Violet accent

MAGENTA_1 = "#B01870"
MAGENTA_2 = "#E83E9F"  # Electric Pink / Magenta -- primary accent
MAGENTA_3 = "#F0529F"
MAGENTA_4 = "#FF6BCB"  # Soft Pink -- highlight

BLUE_1 = "#1E6FA8"
BLUE_2 = "#35B8FF"      # Electric Blue -- supporting series
CYAN_1 = "#28BDB8"
CYAN_2 = "#32D6D0"      # Cyan accent

TEXT_WHITE = "#F5F7FF"
TEXT_LIGHT = "#E7EAF5"
TEXT_MUTED = "#9DA6BA"
GRID_COLOR = "rgba(255,255,255,0.07)"

# Section accent colors (used for single-color chart series -- purely
# cosmetic, does not alter any values or chart data).
BLUE = CYAN_2        # Air Power chart accent
GREEN = PURPLE_3      # Military Manpower chart accent
GOLD = MAGENTA_3      # Land Power chart accent
RED = MAGENTA_2        # Primary highlight / alert accent

# ---------------------------------------------------------------------------
# CSS (mirrors app.py exactly -- each Streamlit page re-renders its own CSS,
# including the header top-padding fix so the title is never clipped by the
# fixed Streamlit toolbar)
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
    .stApp {{
        background:
            radial-gradient(circle at 15% 0%, rgba(124, 77, 255, 0.10) 0%, rgba(7,11,22,0) 40%),
            radial-gradient(circle at 85% 100%, rgba(232, 62, 159, 0.08) 0%, rgba(7,11,22,0) 45%),
            linear-gradient(135deg, {BG_DARK} 0%, {BG_CARD} 45%, #160B29 100%);
        color: {TEXT_LIGHT};
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BG_DARK_2} 0%, #0A0818 100%);
        border-right: 1px solid rgba(124, 77, 255, 0.30);
    }}
    [data-testid="stSidebar"] * {{
        color: {TEXT_LIGHT} !important;
    }}
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {BG_CARD} !important;
        border: 1px solid rgba(232, 62, 159, 0.35) !important;
        border-radius: 10px !important;
    }}
    .block-container {{
        padding-top: 3.2rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4, p, span, label, div {{
        color: {TEXT_LIGHT};
    }}
    .dashboard-header {{
        padding: 0.7rem 1.1rem 0.8rem 1.1rem;
        margin-top: 0;
        overflow: visible;
        border: 1px solid rgba(124, 77, 255, 0.30);
        border-radius: 16px;
        margin-bottom: 1.3rem;
        background: linear-gradient(120deg, rgba(90,46,156,0.35) 0%, rgba(16,21,43,0.55) 45%, rgba(30,111,168,0.20) 100%);
        box-shadow: 0 0 24px rgba(232, 62, 159, 0.10), 0 8px 24px rgba(0,0,0,0.45);
    }}
    .dashboard-title {{
        font-size: 1.95rem;
        line-height: 1.35;
        font-weight: 800;
        margin: 0;
        padding-top: 0.1rem;
        color: {TEXT_WHITE};
        letter-spacing: 0.2px;
        text-shadow: 0 0 18px rgba(232, 62, 159, 0.25);
    }}
    .dashboard-subtitle {{
        font-size: 1.05rem;
        font-weight: 700;
        background: linear-gradient(90deg, {MAGENTA_3}, {CYAN_2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.2rem 0 0.3rem 0;
        display: inline-block;
    }}
    .dashboard-desc {{
        font-size: 0.85rem;
        color: {TEXT_MUTED};
        margin: 0;
    }}
    .kpi-card {{
        background: linear-gradient(160deg, {BG_CARD_2} 0%, {BG_CARD} 100%);
        border: 1px solid rgba(124, 77, 255, 0.30);
        border-radius: 16px;
        padding: 0.95rem 1.05rem;
        text-align: left;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 10px rgba(0,0,0,0.45);
        height: 100%;
        position: relative;
    }}
    .kpi-card:hover {{
        border-color: {MAGENTA_3};
        box-shadow: 0 4px 22px rgba(232, 62, 159, 0.28), 0 0 14px rgba(50, 214, 208, 0.18);
        transform: translateY(-3px);
    }}
    .kpi-icon {{
        font-size: 1.3rem;
        filter: drop-shadow(0 0 6px rgba(232, 62, 159, 0.35));
    }}
    .kpi-value {{
        font-size: 1.32rem;
        font-weight: 800;
        color: {TEXT_WHITE};
        margin: 0.18rem 0 0.05rem 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .kpi-label {{
        font-size: 0.73rem;
        font-weight: 600;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .section-title {{
        font-size: 1.08rem;
        font-weight: 700;
        color: {TEXT_WHITE};
        border-left: 4px solid {MAGENTA_3};
        padding-left: 0.65rem;
        margin: 1.5rem 0 0.65rem 0;
        text-shadow: 0 0 10px rgba(232, 62, 159, 0.15);
    }}
    .profile-card {{
        background: linear-gradient(160deg, {BG_CARD_2} 0%, {BG_CARD} 100%);
        border: 1px solid rgba(50, 214, 208, 0.30);
        border-radius: 14px;
        padding: 0.75rem 0.95rem;
        margin-bottom: 0.55rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.35);
    }}
    .profile-label {{
        font-size: 0.72rem;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}
    .profile-value {{
        font-size: 1.06rem;
        font-weight: 700;
        color: {TEXT_WHITE};
    }}
    .rank-pill {{
        display: inline-block;
        background: linear-gradient(90deg, rgba(176, 24, 112, 0.20), rgba(50, 214, 208, 0.16));
        border: 1px solid rgba(232, 62, 159, 0.45);
        color: {TEXT_LIGHT};
        border-radius: 20px;
        padding: 0.32rem 0.95rem;
        font-size: 0.85rem;
        font-weight: 700;
        margin: 0.15rem 0.3rem 0.15rem 0;
        box-shadow: 0 0 10px rgba(232, 62, 159, 0.10);
    }}
    .caption-text {{
        font-size: 0.8rem;
        color: {TEXT_MUTED};
        font-style: italic;
        margin-top: -0.4rem;
        margin-bottom: 0.8rem;
    }}
    .footer-text {{
        text-align: center;
        color: {TEXT_MUTED};
        font-size: 0.8rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid rgba(124, 77, 255, 0.30);
        margin-top: 2rem;
    }}
</style>
""", unsafe_allow_html=True)


def _empty_layout(fig: go.Figure, height=380) -> go.Figure:
    """Shared dark theme layout, identical styling across this page's charts."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font=dict(family="Inter, Segoe UI, Arial", color=TEXT_LIGHT, size=12),
        margin=dict(l=10, r=10, t=45, b=10),
        height=height,
        hoverlabel=dict(bgcolor=BG_CARD_2, font_size=12, font_family="Inter, Arial",
                         bordercolor="rgba(232, 62, 159, 0.35)"),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig


# ---------------------------------------------------------------------------
# LOAD DATA (same cache as Quick Stats -- instant on this page)
# ---------------------------------------------------------------------------
try:
    final_df, long_df = utils.load_data()
except Exception as e:
    st.error(f"Failed to load the dataset. Details: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="dashboard-header">
    <p class="dashboard-title">🌍 Unified Military Analytics</p>
    <p class="dashboard-subtitle">Nation Overview Dashboard</p>
    <p class="dashboard-desc">Detailed military capability, manpower, economic and strategic profile of the selected nation.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# COUNTRY SELECTOR
# ---------------------------------------------------------------------------
country_list = sorted(final_df[utils.COL_COUNTRY].dropna().unique().tolist())
default_country = "United States" if "United States" in country_list else (country_list[0] if country_list else None)

if not country_list:
    st.warning("No countries available in the dataset.")
    st.stop()

default_index = country_list.index(default_country) if default_country in country_list else 0
selected_country = st.selectbox("🌎 Select Country", options=country_list, index=default_index, key="nation_overview_country")

row = final_df[final_df[utils.COL_COUNTRY] == selected_country]
if row.empty:
    st.warning("Selected country not found in the dataset.")
    st.stop()
row = row.iloc[0]


def val(col):
    """Safely reads a column value for the selected country row; None if missing/NaN."""
    if col not in final_df.columns:
        return None
    v = row.get(col)
    if pd.isna(v):
        return None
    return v


# ---------------------------------------------------------------------------
# SECTION 1: COUNTRY SUMMARY (KPI CARDS)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🏆 Country Summary</div>', unsafe_allow_html=True)


def kpi_card(col, icon, label, value):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)


rank_val = val(utils.COL_RANK)
rank_display = f"#{int(rank_val)}" if rank_val is not None else "N/A"

r1 = st.columns(4)
kpi_card(r1[0], "🏆", "Power Rank", rank_display)
kpi_card(r1[1], "⚡", "Power Index", utils.format_score(val(utils.COL_SCORE)))
kpi_card(r1[2], "💰", "Defense Budget", utils.format_currency(val(utils.COL_BUDGET)))
kpi_card(r1[3], "👥", "Active Personnel", utils.format_plain(val(utils.COL_ACTIVE)))

r2 = st.columns(4)
kpi_card(r2[0], "🎖️", "Reserve Personnel", utils.format_plain(val(utils.COL_RESERVE)))
kpi_card(r2[1], "✈️", "Total Military Aircraft", utils.format_plain(val(utils.COL_AIRCRAFT)))
kpi_card(r2[2], "🪖", "Tanks", utils.format_plain(val(utils.COL_TANKS)))
kpi_card(r2[3], "⚓", "Total Naval Fleet", utils.format_plain(val(utils.COL_NAVAL)))

# ---------------------------------------------------------------------------
# SECTION 2: COUNTRY PROFILE
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📋 Country Profile</div>', unsafe_allow_html=True)

profile_fields = [
    ("Country", val(utils.COL_COUNTRY) or "N/A"),
    ("Continent", val(utils.COL_CONTINENT) or "N/A"),
    ("Region", val(utils.COL_REGION) or "N/A"),
    ("Alliance", val(utils.COL_ALLIANCE) or "N/A"),
    ("Power Index Rank", rank_display),
    ("Power Index Score", utils.format_score(val(utils.COL_SCORE))),
    ("GDP", utils.format_currency(val(utils.COL_GDP))),
    ("Population", utils.format_plain(val(utils.COL_POP))),
    ("Land Area (sq km)", utils.format_plain(val("total_land_area_sq_km"))),
    ("Coastline (km)", utils.format_plain(val("coastline_coverage_km"))),
    ("Border Coverage (km)", utils.format_plain(val("border_coverage_km"))),
]

pcols = st.columns(4)
for i, (label, value) in enumerate(profile_fields):
    with pcols[i % 4]:
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-label">{label}</div>
            <div class="profile-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SHARED CHART BUILDER: single-country metric breakdown (same-unit metrics)
# ---------------------------------------------------------------------------
def single_country_bar(metric_dict, title, color, height=340, pct_of_total=None, x_label="Value",
                        gradient_end=None):
    """
    Builds a horizontal bar chart of several same-unit metrics for ONE
    country (e.g. all aircraft counts, all personnel counts). Metrics with
    missing/NaN data are simply left out rather than crashing.

    metric_dict: {human-readable label: raw column name}
    pct_of_total: raw column name to compute "% of total" in the hover text
    gradient_end: optional second color; when provided, bars are colored on
    a value-based colorscale from `color` to `gradient_end` for a premium
    gradient look. This is purely cosmetic and does not affect the bar
    values, ordering, or underlying data.
    """
    labels, values, pct_text = [], [], []
    total = val(pct_of_total) if pct_of_total else None

    for label, col in metric_dict.items():
        v = val(col)
        if v is None:
            continue
        labels.append(label)
        values.append(v)
        if total and total > 0:
            pct_text.append(f"{(v / total) * 100:.1f}% of total")
        else:
            pct_text.append("")

    if not labels:
        fig = go.Figure()
        fig.add_annotation(text="No data available for this section.", showarrow=False,
                            font=dict(size=13, color=TEXT_MUTED), xref="paper", yref="paper", x=0.5, y=0.5)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        return _empty_layout(fig, height=height)

    order = np.argsort(values)
    labels = [labels[i] for i in order]
    values = [values[i] for i in order]
    pct_text = [pct_text[i] for i in order]

    if gradient_end:
        marker = dict(
            color=values,
            colorscale=[[0, color], [1, gradient_end]],
            showscale=False,
            line=dict(color="rgba(255,255,255,0.08)", width=0.5),
        )
    else:
        marker = dict(color=color, line=dict(color="rgba(255,255,255,0.08)", width=0.5))

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=marker,
        customdata=pct_text,
        text=[f"{v:,.0f}" for v in values],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>" + x_label + ": %{x:,.0f}<br>%{customdata}<extra></extra>",
    ))
    fig.update_layout(title=dict(text=title, font=dict(size=15, color=TEXT_WHITE)))
    return _empty_layout(fig, height=height)


# ---------------------------------------------------------------------------
# SECTION 3: MILITARY MANPOWER
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">👥 Military Manpower</div>', unsafe_allow_html=True)
manpower_fig = single_country_bar(
    {
        "Active Personnel": "active_personnel",
        "Reserve Personnel": "reserve_personnel",
        "Paramilitary": "paramilitary",
        "Total Military Manpower": "total_military_manpower",
    },
    "Military Manpower Composition", PURPLE_3,
    pct_of_total="total_military_manpower", x_label="Personnel",
    gradient_end=MAGENTA_3,
)
st.plotly_chart(manpower_fig, use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION 4: AIR POWER
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">✈️ Air Power</div>', unsafe_allow_html=True)
air_fig = single_country_bar(
    {
        "Total Military Aircraft": "total_military_aircraft",
        "Fighter Aircraft": "fighter_aircraft",
        "Attack Aircraft": "attack_aircraft",
        "Transport Aircraft": "transport_aircraft",
        "Trainer Aircraft": "trainer_aircraft",
        "Special Mission Aircraft": "special_mission_aircraft",
        "Tanker Aircraft": "tanker_aircraft",
        "Total Military Helicopters": "total_military_helicopters",
        "Attack Helicopters": "attack_helicopters",
    },
    "Air Power Profile", BLUE_2, height=420, x_label="Units",
    gradient_end=CYAN_2,
)
st.plotly_chart(air_fig, use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION 5: LAND POWER
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🪖 Land Power</div>', unsafe_allow_html=True)
land_fig = single_country_bar(
    {
        "Tanks": "tanks",
        "Armored Fighting Vehicles": "armored_fighting_vehicles",
        "Self-Propelled Artillery": "self_propelled_artillery",
        "Towed Artillery": "towed_artillery",
        "Rocket Projectors": "rocket_projectors",
    },
    "Land Forces", PURPLE_1, x_label="Units",
    gradient_end=MAGENTA_4,
)
st.plotly_chart(land_fig, use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION 6: NAVAL POWER
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">⚓ Naval Power</div>', unsafe_allow_html=True)

naval_col1, naval_col2 = st.columns([3, 1])
with naval_col1:
    naval_fig = single_country_bar(
        {
            "Total Naval Fleet": "total_naval_fleet",
            "Aircraft Carriers": "aircraft_carriers",
            "Helicopter Carriers": "helicopter_carriers",
            "Submarines": "submarines",
            "Destroyers": "destroyers",
            "Frigates": "frigates",
            "Corvettes": "corvettes",
            "Coastal Patrol Craft": "coastal_patrol_craft",
            "Mine Warfare Craft": "mine_warfare_craft",
        },
        "Naval Forces", BLUE_1, height=420, x_label="Units",
        gradient_end=CYAN_1,
    )
    st.plotly_chart(naval_fig, use_container_width=True)
with naval_col2:
    st.markdown("<br>", unsafe_allow_html=True)
kpi_card(naval_col2, "🚢", "Total Naval Fleet Tonnage", utils.format_number(val("total_naval_fleet_tonnage_mt")))

# ---------------------------------------------------------------------------
# SECTION 7: RADAR CHART -- STRATEGIC CAPABILITY PROFILE
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🎯 Strategic Capability Profile</div>', unsafe_allow_html=True)


def safe_max(col):
    if col not in final_df.columns:
        return None
    m = final_df[col].max()
    return m if pd.notna(m) and m > 0 else None


def normalize_pct(value, max_value):
    if value is None or max_value is None:
        return 0.0
    return round(float(value) / float(max_value) * 100, 1)


infra_components = ["total_serviceable_airports", "major_ports_and_terminals",
                     "railway_coverage_km", "roadway_coverage_km", "waterway_coverage_km"]
infra_scores = []
for c in infra_components:
    mx = safe_max(c)
    v = val(c)
    if mx is not None and v is not None:
        infra_scores.append(normalize_pct(v, mx))
infrastructure_score = round(sum(infra_scores) / len(infra_scores), 1) if infra_scores else 0.0

radar_categories = ["Air Power", "Land Power", "Naval Power", "Manpower", "Defense Budget", "Infrastructure"]
radar_values = [
    normalize_pct(val("total_military_aircraft"), safe_max("total_military_aircraft")),
    normalize_pct(val("tanks"), safe_max("tanks")),
    normalize_pct(val("total_naval_fleet"), safe_max("total_naval_fleet")),
    normalize_pct(val("total_military_manpower"), safe_max("total_military_manpower")),
    normalize_pct(val("defense_budget_usd"), safe_max("defense_budget_usd")),
    infrastructure_score,
]

radar_fig = go.Figure()
radar_fig.add_trace(go.Scatterpolar(
    r=radar_values + [radar_values[0]],
    theta=radar_categories + [radar_categories[0]],
    fill="toself",
    line=dict(color=CYAN_2, width=2.5),
    fillcolor="rgba(232, 62, 159, 0.22)",
    marker=dict(color=MAGENTA_4, size=6),
    hovertemplate="<b>%{theta}</b><br>Normalized Score: %{r:.1f} / 100<extra></extra>",
))
radar_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor=BG_CARD,
    polar=dict(
        bgcolor=BG_CARD,
        radialaxis=dict(visible=True, range=[0, 100], gridcolor=GRID_COLOR, color=TEXT_MUTED),
        angularaxis=dict(gridcolor=GRID_COLOR, color=TEXT_LIGHT),
    ),
    font=dict(family="Inter, Arial", color=TEXT_LIGHT, size=12),
    margin=dict(l=40, r=40, t=40, b=30),
    height=460,
    showlegend=False,
    title=dict(text=f"Strategic Capability Profile -- {selected_country}", font=dict(size=15, color=TEXT_WHITE)),
)
st.plotly_chart(radar_fig, use_container_width=True)
st.markdown(
    '<div class="caption-text">Each axis is normalized to 0-100 by dividing this country\'s value by the '
    'highest value for that metric across all 145 countries (e.g. Air Power = this country\'s aircraft '
    '&divide; maximum aircraft in the dataset &times; 100). Infrastructure is a composite average of normalized '
    'airports, ports, railway, roadway, and waterway coverage. This keeps very different units (aircraft counts, '
    'USD budgets, personnel) fairly comparable on one chart.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SECTION 8: ECONOMIC & STRATEGIC METRICS
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">💰 Economic & Strategic Metrics</div>', unsafe_allow_html=True)

e1 = st.columns(3)
kpi_card(e1[0], "🌐", "GDP", utils.format_currency(val(utils.COL_GDP)))
kpi_card(e1[1], "💰", "Defense Budget", utils.format_currency(val(utils.COL_BUDGET)))
budget_gdp = val(utils.COL_BUDGET_TO_GDP)
kpi_card(e1[2], "📊", "Budget / GDP", f"{budget_gdp:.2f}%" if budget_gdp is not None else "N/A")

e2 = st.columns(3)
kpi_card(e2[0], "📉", "External Debt", utils.format_currency(val("external_debt_usd")))
kpi_card(e2[1], "🏦", "Purchasing Power Parity", utils.format_currency(val(utils.COL_PPP)))
kpi_card(e2[2], "💵", "Forex & Gold Reserves", utils.format_currency(val("foreign_exchange_and_gold_reserves_usd")))

# ---------------------------------------------------------------------------
# SECTION 9: STRATEGIC INFRASTRUCTURE
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🏗️ Strategic Infrastructure</div>', unsafe_allow_html=True)

infra_metric_cols = {
    "Serviceable Airports": "total_serviceable_airports",
    "Major Ports & Terminals": "major_ports_and_terminals",
    "Merchant Marine Fleet": "total_merchant_marine_fleet",
    "Railway Coverage (km)": "railway_coverage_km",
    "Roadway Coverage (km)": "roadway_coverage_km",
    "Waterway Coverage (km)": "waterway_coverage_km",
    "Coastline Coverage (km)": "coastline_coverage_km",
    "Border Coverage (km)": "border_coverage_km",
}
infra_rows = []
for label, col in infra_metric_cols.items():
    v = val(col)
    if v is not None:
        unit = "km" if "km" in label else "count"
        infra_rows.append({"Metric": label, "Value": v, "Unit Group": "Distance (km)" if unit == "km" else "Count"})

if infra_rows:
    infra_df = pd.DataFrame(infra_rows)
    infra_chart_fig = px.bar(
        infra_df, x="Value", y="Metric", orientation="h",
        facet_col="Unit Group", color="Unit Group",
        color_discrete_sequence=[PURPLE_3, CYAN_2],
    )
    infra_chart_fig.update_xaxes(matches=None, tickformat=",")
    infra_chart_fig.update_yaxes(matches=None, title=None)
    infra_chart_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1], font=dict(color=TEXT_LIGHT, size=11)))
    infra_chart_fig.update_layout(
        title=dict(text="Strategic Infrastructure (grouped by unit type)", font=dict(size=15, color=TEXT_WHITE)),
        showlegend=False, height=420,
    )
    st.plotly_chart(_empty_layout(infra_chart_fig, height=420), use_container_width=True)
else:
    st.info("No infrastructure data available for this country.")

# ---------------------------------------------------------------------------
# SECTION 10: NATURAL RESOURCES (grouped compact cards -- not overloaded)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🛢️ Natural Resources</div>', unsafe_allow_html=True)

resource_groups = [
    ("Oil", "🛢️", "oil_production_bbl", "oil_consumption_bbl", "proven_oil_reserves_bbl", "bbl"),
    ("Natural Gas", "🔥", "natural_gas_production_cum", "natural_gas_consumption_cum", "proven_natural_gas_reserves_cum", "cu.m"),
    ("Coal", "⛏️", "coal_production_cum", "coal_consumption_mt", "proven_coal_reserves_cum", "mt/cu.m"),
]
for group_name, icon, prod_col, cons_col, reserve_col, unit in resource_groups:
    st.markdown(f"**{icon} {group_name}** <span class='caption-text'>(units: {unit})</span>", unsafe_allow_html=True)
    rcols = st.columns(3)
    kpi_card(rcols[0], icon, f"{group_name} Production", utils.format_number(val(prod_col)))
    kpi_card(rcols[1], icon, f"{group_name} Consumption", utils.format_number(val(cons_col)))
    kpi_card(rcols[2], icon, f"{group_name} Proven Reserves", utils.format_number(val(reserve_col)))

# ---------------------------------------------------------------------------
# SECTION 11: SELECTED COUNTRY VS GLOBAL AVERAGE
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📊 Selected Country vs Global Average</div>', unsafe_allow_html=True)

comparison_metrics = {
    "Power Index Score": utils.COL_SCORE,
    "Defense Budget": utils.COL_BUDGET,
    "Active Personnel": utils.COL_ACTIVE,
    "Total Aircraft": utils.COL_AIRCRAFT,
    "Tanks": utils.COL_TANKS,
    "Naval Fleet": utils.COL_NAVAL,
}

comparison_rows = []
for label, col in comparison_metrics.items():
    if col not in final_df.columns:
        continue
    country_value = val(col)
    global_avg = final_df[col].mean()
    if country_value is None or pd.isna(global_avg) or global_avg == 0:
        continue
    ratio_pct = round((country_value / global_avg) * 100, 1)
    comparison_rows.append({
        "Metric": label, "Ratio (%)": ratio_pct,
        "Country Value": country_value, "Global Average": global_avg,
    })

if comparison_rows:
    comp_df = pd.DataFrame(comparison_rows)

    def _fmt_compare(row_):
        if row_["Metric"] in ("Defense Budget",):
            return utils.format_currency(row_["Country Value"]), utils.format_currency(row_["Global Average"])
        if row_["Metric"] == "Power Index Score":
            return utils.format_score(row_["Country Value"]), utils.format_score(row_["Global Average"])
        return utils.format_plain(row_["Country Value"]), utils.format_plain(row_["Global Average"])

    formatted = comp_df.apply(_fmt_compare, axis=1, result_type="expand")
    comp_df["Country Display"] = formatted[0]
    comp_df["Average Display"] = formatted[1]

    comp_fig = go.Figure(go.Bar(
        x=comp_df["Metric"], y=comp_df["Ratio (%)"],
        marker=dict(color=[MAGENTA_3 if r >= 100 else TEXT_MUTED for r in comp_df["Ratio (%)"]]),
        customdata=np.stack([comp_df["Country Display"], comp_df["Average Display"]], axis=-1),
        hovertemplate=(
            "<b>%{x}</b><br>" + selected_country + ": %{customdata[0]}<br>"
            "Global Average: %{customdata[1]}<br>%{y:.1f}% of global average<extra></extra>"
        ),
    ))
    comp_fig.add_hline(y=100, line_dash="dash", line_color=CYAN_2,
                        annotation_text="Global Average (100%)", annotation_font_color=TEXT_MUTED)
    comp_fig.update_layout(title=dict(text=f"{selected_country} vs Global Average (100% = Average)", font=dict(size=15, color=TEXT_WHITE)))
    comp_fig.update_yaxes(title="% of Global Average")
    st.plotly_chart(_empty_layout(comp_fig, height=400), use_container_width=True)
    st.markdown(
        '<div class="caption-text">Bars show this country\'s value as a percentage of the global average '
        'across all 145 countries. 100% means exactly average; above 100% means above average.</div>',
        unsafe_allow_html=True,
    )
else:
    st.info("Not enough data available to build the global average comparison.")

# ---------------------------------------------------------------------------
# SECTION 12: RANK / COMPARISON INFORMATION
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🥇 Rank Information</div>', unsafe_allow_html=True)

total_countries = final_df[utils.COL_COUNTRY].nunique()


def compute_rank(col, higher_is_better):
    """Computes this country's rank for a column among all countries with valid data."""
    if col not in final_df.columns:
        return None
    valid = final_df.dropna(subset=[col])
    if selected_country not in valid[utils.COL_COUNTRY].values:
        return None
    ranks = valid[col].rank(method="min", ascending=not higher_is_better)
    country_rank = ranks[valid[utils.COL_COUNTRY] == selected_country]
    if country_rank.empty:
        return None
    return int(country_rank.iloc[0]), len(valid)


rank_pills = []

if rank_val is not None:
    rank_pills.append(f"Power Index Rank: #{int(rank_val)} of {total_countries}")

aircraft_rank = compute_rank("total_military_aircraft", higher_is_better=True)
if aircraft_rank:
    rank_pills.append(f"Aircraft Rank: #{aircraft_rank[0]} of {aircraft_rank[1]}")

tank_rank = compute_rank("tanks", higher_is_better=True)
if tank_rank:
    rank_pills.append(f"Tank Rank: #{tank_rank[0]} of {tank_rank[1]}")

naval_rank = compute_rank("total_naval_fleet", higher_is_better=True)
if naval_rank:
    rank_pills.append(f"Naval Fleet Rank: #{naval_rank[0]} of {naval_rank[1]}")

budget_rank = compute_rank("defense_budget_usd", higher_is_better=True)
if budget_rank:
    rank_pills.append(f"Defense Budget Rank: #{budget_rank[0]} of {budget_rank[1]}")

if rank_pills:
    pills_html = "".join(f'<span class="rank-pill">{p}</span>' for p in rank_pills)
    st.markdown(pills_html, unsafe_allow_html=True)
else:
    st.info("Rank information not available for this country.")

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="footer-text">
    Developed for Infosys Virtual Internship &nbsp;|&nbsp; Unified Military Analytics and Comparison Dashboard
</div>
""", unsafe_allow_html=True)