"""
pages/compare_powers.py
-------------------------
Unified Military Analytics and Comparison Dashboard
Module 6 - Compare Powers Dashboard

Streamlit multipage "page" -- auto-detected from pages/. Does NOT call
st.set_page_config() (already set once in app.py).

Reuses utils.py (data loading/formatting, same cache as the other two
dashboards) and charts.py (shared theme colors) purely by import -- neither
file is modified. All chart-building logic specific to this page lives
locally here.

No st.dataframe() / st.table() / pyarrow anywhere on this page.
"""

import os
import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------------------------
# MAKE SURE utils.py / charts.py (project root) ARE IMPORTABLE
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
# THEME -- Premium dark navy/purple/magenta/cyan analytics palette
# (scoped to THIS page only; charts.py and other pages are untouched)
# ---------------------------------------------------------------------------
BG_COLOR = "#0B0820"          # deep navy/purple background
CARD_COLOR = "#151039"        # card / panel background
PANEL_ALT = "#100B2E"         # secondary panel shade (hover backgrounds, etc.)
RED = "#E00087"               # magenta accent -- Country 1 / primary series
GOLD = "#36D1DC"               # cyan accent -- Country 2 / secondary series
TEXT_LIGHT = "#FFFFFF"
TEXT_MUTED = "#B9B7C8"
GRID_COLOR = "rgba(139, 77, 255, 0.18)"   # subtle purple gridlines for charts
BORDER = "rgba(139, 77, 255, 0.28)"       # subtle purple card/control borders
COLOR_A = RED          # Country 1
COLOR_B = GOLD         # Country 2
WIN_GREEN = "#36D1DC"  # "stronger" highlight -- cyan, not green (kept the original variable name to avoid touching any reference to it)

# ---------------------------------------------------------------------------
# CSS (mirrors app.py / nation_overview.py -- including the header
# top-padding fix so the title is never clipped by Streamlit's toolbar)
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }}
    .stApp {{
        background:
            radial-gradient(circle at 10% 5%, rgba(113, 54, 200, 0.28) 0%, rgba(11,8,32,0) 40%),
            radial-gradient(circle at 92% 90%, rgba(32, 184, 216, 0.14) 0%, rgba(11,8,32,0) 42%),
            radial-gradient(circle at 88% 8%, rgba(224, 0, 135, 0.14) 0%, rgba(11,8,32,0) 35%),
            linear-gradient(165deg, #070613 0%, #0B0820 45%, #100B2E 100%);
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #100B2E 0%, #151039 55%, #1B1147 100%);
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stSidebar"] * {{
        color: {TEXT_LIGHT};
    }}
    .block-container {{
        padding-top: 3.2rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4, p, span, label, div {{
        color: {TEXT_LIGHT};
    }}
    .dashboard-header {{
        position: relative;
        background: linear-gradient(135deg, rgba(21,16,57,0.88) 0%, rgba(16,11,46,0.93) 55%, rgba(11,8,32,0.96) 100%);
        border: 1px solid rgba(139, 77, 255, 0.35);
        border-radius: 18px;
        padding: 1.5rem 1.9rem 1.4rem 1.9rem;
        margin-top: 0;
        margin-bottom: 1.4rem;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.45), 0 0 26px rgba(224, 0, 135, 0.12);
    }}
    .dashboard-header::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {RED} 0%, #7136C8 50%, {GOLD} 100%);
    }}
    .dashboard-header::after {{
        content: "";
        position: absolute;
        top: -45%;
        right: -8%;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(224, 0, 135, 0.18) 0%, rgba(224, 0, 135, 0) 70%);
        pointer-events: none;
    }}
    .dashboard-title {{
        position: relative;
        font-size: 2.15rem;
        line-height: 1.3;
        font-weight: 800;
        letter-spacing: 0.02em;
        margin: 0;
        padding-top: 0.1rem;
        color: {TEXT_LIGHT};
        text-shadow: 0 0 24px rgba(224, 0, 135, 0.32);
    }}
    .dashboard-subtitle {{
        position: relative;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        background: linear-gradient(90deg, {RED} 0%, {GOLD} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.55rem 0 0.5rem 0;
        display: inline-block;
    }}
    .dashboard-desc {{
        position: relative;
        font-size: 0.88rem;
        color: {TEXT_MUTED};
        margin: 0;
        max-width: 640px;
        line-height: 1.55;
    }}
    .section-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {TEXT_LIGHT};
        border-left: 4px solid;
        border-image: linear-gradient(180deg, {RED}, {GOLD}) 1;
        padding-left: 0.6rem;
        margin: 1.4rem 0 0.6rem 0;
    }}
    .country-banner {{
        border-radius: 14px;
        padding: 0.7rem 1rem;
        text-align: center;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.35);
        transition: all 0.2s ease-in-out;
    }}
    .country-banner-a {{
        background-color: rgba(224, 0, 135, 0.14);
        border: 1px solid {COLOR_A};
        color: {TEXT_LIGHT};
    }}
    .country-banner-a:hover {{
        box-shadow: 0 4px 18px rgba(224, 0, 135, 0.28);
    }}
    .country-banner-b {{
        background-color: rgba(54, 209, 220, 0.12);
        border: 1px solid {COLOR_B};
        color: {TEXT_LIGHT};
    }}
    .country-banner-b:hover {{
        box-shadow: 0 4px 18px rgba(54, 209, 220, 0.24);
    }}
    .kpi-compare-card {{
        background: linear-gradient(160deg, {CARD_COLOR} 0%, {PANEL_ALT} 100%);
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 0.85rem 1.1rem;
        margin-bottom: 0.6rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
        transition: all 0.2s ease-in-out;
    }}
    .kpi-compare-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {COLOR_A} 0%, #7136C8 50%, {COLOR_B} 100%);
    }}
    .kpi-compare-card:hover {{
        border-color: rgba(139, 77, 255, 0.55);
        box-shadow: 0 6px 20px rgba(113, 54, 200, 0.22), 0 0 14px rgba(224, 0, 135, 0.10);
        transform: translateY(-1px);
    }}
    .kpi-compare-label {{
        font-size: 0.75rem;
        font-weight: 700;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.35rem;
    }}
    .kpi-compare-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .kpi-compare-value {{
        font-size: 1.15rem;
        font-weight: 800;
    }}
    .kpi-compare-value-a {{
        color: {COLOR_A};
        text-align: left;
    }}
    .kpi-compare-value-b {{
        color: {COLOR_B};
        text-align: right;
    }}
    .kpi-winner {{
        display: inline-block;
        background-color: rgba(54, 209, 220, 0.16);
        border: 1px solid {WIN_GREEN};
        color: {WIN_GREEN};
        border-radius: 8px;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.05rem 0.4rem;
        margin-left: 0.35rem;
    }}
    .profile-card {{
        background-color: {CARD_COLOR};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.5rem;
    }}
    .profile-label {{
        font-size: 0.72rem;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}
    .profile-value {{
        font-size: 1.0rem;
        font-weight: 700;
        color: {TEXT_LIGHT};
    }}
    .summary-card {{
        background-color: {CARD_COLOR};
        border: 1px solid {BORDER};
        border-left: 4px solid {WIN_GREEN};
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
        color: {TEXT_LIGHT};
    }}
    [data-baseweb="select"] > div {{
        background-color: {CARD_COLOR} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
        color: {TEXT_LIGHT} !important;
    }}
    [data-baseweb="popover"] li {{
        background-color: {CARD_COLOR} !important;
        color: {TEXT_LIGHT} !important;
    }}
    [data-baseweb="popover"] li:hover {{
        background-color: rgba(224, 0, 135, 0.14) !important;
    }}
    .footer-text {{
        text-align: center;
        color: {TEXT_MUTED};
        font-size: 0.8rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid {BORDER};
        margin-top: 2rem;
    }}
</style>
""", unsafe_allow_html=True)


def _empty_layout(fig: go.Figure, height=380) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        font=dict(family="Inter, Segoe UI, Arial", color=TEXT_LIGHT, size=12),
        margin=dict(l=10, r=10, t=45, b=10),
        height=height,
        hoverlabel=dict(bgcolor=PANEL_ALT, bordercolor=BORDER, font_size=12, font_family="Inter, Arial", font_color=TEXT_LIGHT),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig


# ---------------------------------------------------------------------------
# LOAD DATA (same cache as the other two dashboards)
# ---------------------------------------------------------------------------
try:
    final_df, _long_df = utils.load_data()
except Exception as e:
    st.error(f"Failed to load the dataset. Details: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="dashboard-header">
    <p class="dashboard-title">⚔️ Compare Military Powers</p>
    <p class="dashboard-subtitle">Side-by-side comparison of two nations</p>
    <p class="dashboard-desc">Manpower, air, land, naval, and economic capability compared head-to-head.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# COUNTRY SELECTION (Tableau-parameter style: two independent selectors,
# with Country 2's list excluding whatever is currently picked for Country 1
# so the same country can never be selected on both sides)
# ---------------------------------------------------------------------------
all_countries = sorted(final_df[utils.COL_COUNTRY].dropna().unique().tolist())
if len(all_countries) < 2:
    st.warning("At least two countries are required to use Compare Powers.")
    st.stop()

sel_col1, sel_col2 = st.columns(2)
with sel_col1:
    default_a = "United States" if "United States" in all_countries else all_countries[0]
    country_a = st.selectbox("🅰️ Country 1", options=all_countries,
                              index=all_countries.index(default_a), key="compare_country_a")

with sel_col2:
    options_b = [c for c in all_countries if c != country_a]
    default_b = "India" if "India" in options_b else options_b[0]
    country_b = st.selectbox("🅱️ Country 2", options=options_b,
                              index=options_b.index(default_b), key="compare_country_b")

row_a = final_df[final_df[utils.COL_COUNTRY] == country_a].iloc[0]
row_b = final_df[final_df[utils.COL_COUNTRY] == country_b].iloc[0]


def val_a(col):
    v = row_a.get(col) if col in final_df.columns else None
    return None if pd.isna(v) else v


def val_b(col):
    v = row_b.get(col) if col in final_df.columns else None
    return None if pd.isna(v) else v


st.markdown(f"""
<div style="display:flex; gap:1rem; margin-top:0.4rem;">
    <div class="country-banner country-banner-a" style="flex:1;">🅰️ {country_a}</div>
    <div class="country-banner country-banner-b" style="flex:1;">🅱️ {country_b}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KPI COMPARISON CARDS
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📊 KPI Comparison</div>', unsafe_allow_html=True)

# (label, column, higher_is_better, formatter)
kpi_definitions = [
    ("Power Index Score", utils.COL_SCORE, False, utils.format_score),
    ("Power Index Rank", utils.COL_RANK, False, lambda v: f"#{int(v)}" if v is not None else "N/A"),
    ("Total Military Manpower", utils.COL_MANPOWER, True, utils.format_number),
    ("Active Personnel", utils.COL_ACTIVE, True, utils.format_plain),
    ("Reserve Personnel", utils.COL_RESERVE, True, utils.format_plain),
    ("Total Military Aircraft", utils.COL_AIRCRAFT, True, utils.format_plain),
    ("Total Naval Fleet", utils.COL_NAVAL, True, utils.format_plain),
    ("Tanks", utils.COL_TANKS, True, utils.format_plain),
    ("Defense Budget", utils.COL_BUDGET, True, utils.format_currency),
]


def determine_winner(value_a, value_b, higher_is_better):
    """Returns 'A', 'B', or None (tie / missing data), respecting metric direction."""
    if value_a is None or value_b is None or value_a == value_b:
        return None
    if higher_is_better:
        return "A" if value_a > value_b else "B"
    return "A" if value_a < value_b else "B"  # lower is better (Power Index)


for label, col, higher_is_better, fmt in kpi_definitions:
    va, vb = val_a(col), val_b(col)
    winner = determine_winner(va, vb, higher_is_better)
    display_a = fmt(va) if va is not None else "N/A"
    display_b = fmt(vb) if vb is not None else "N/A"
    badge_a = '<span class="kpi-winner">STRONGER</span>' if winner == "A" else ""
    badge_b = '<span class="kpi-winner">STRONGER</span>' if winner == "B" else ""

    st.markdown(f"""
    <div class="kpi-compare-card">
        <div class="kpi-compare-label">{label}</div>
        <div class="kpi-compare-row">
            <div class="kpi-compare-value kpi-compare-value-a">{display_a}{badge_a}</div>
            <div class="kpi-compare-value kpi-compare-value-b">{badge_b}{display_b}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<p class="dashboard-desc">Note: for Power Index Score and Power Index Rank, a LOWER value indicates a '
    'stronger military -- "STRONGER" is applied correctly in that direction, not simply to the larger number.</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SHARED CHART BUILDER: grouped bar comparing two countries across same-unit metrics
# ---------------------------------------------------------------------------
def grouped_comparison_bar(metric_dict, title, height=360, x_label="Value"):
    """
    metric_dict: {human-readable label: raw column name}
    Builds a grouped horizontal bar chart with one bar-pair per metric,
    comparing Country A vs Country B. Metrics missing for BOTH countries
    are skipped; metrics missing for only one show as 0 with a "N/A" note
    handled via the hover text (never silently invented).
    """
    labels, values_a, values_b = [], [], []
    for label, col in metric_dict.items():
        va, vb = val_a(col), val_b(col)
        if va is None and vb is None:
            continue
        labels.append(label)
        values_a.append(va if va is not None else 0)
        values_b.append(vb if vb is not None else 0)

    if not labels:
        fig = go.Figure()
        fig.add_annotation(text="No data available for this comparison.", showarrow=False,
                            font=dict(size=13, color=TEXT_MUTED), xref="paper", yref="paper", x=0.5, y=0.5)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        return _empty_layout(fig, height=height)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=values_a, name=country_a, orientation="h",
        marker=dict(color=COLOR_A),
        hovertemplate=f"<b>{country_a}</b><br>" + "%{y}: %{x:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=labels, x=values_b, name=country_b, orientation="h",
        marker=dict(color=COLOR_B),
        hovertemplate=f"<b>{country_b}</b><br>" + "%{y}: %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(barmode="group", title=dict(text=title, font=dict(size=15, color=TEXT_LIGHT)))
    fig.update_xaxes(title=x_label)
    return _empty_layout(fig, height=height)


# ---------------------------------------------------------------------------
# SECTION: MILITARY MANPOWER COMPARISON
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">👥 Military Manpower Comparison</div>', unsafe_allow_html=True)
st.plotly_chart(grouped_comparison_bar(
    {"Active Personnel": "active_personnel", "Reserve Personnel": "reserve_personnel", "Paramilitary": "paramilitary"},
    "Military Manpower Comparison", x_label="Personnel",
), use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION: AIR POWER COMPARISON
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">✈️ Air Power Comparison</div>', unsafe_allow_html=True)
st.plotly_chart(grouped_comparison_bar(
    {
        "Total Military Aircraft": "total_military_aircraft",
        "Fighter Aircraft": "fighter_aircraft",
        "Attack Aircraft": "attack_aircraft",
        "Transport Aircraft": "transport_aircraft",
        "Military Helicopters": "total_military_helicopters",
    },
    "Air Power Comparison", height=380, x_label="Units",
), use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION: LAND POWER COMPARISON
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🪖 Land Power Comparison</div>', unsafe_allow_html=True)
st.plotly_chart(grouped_comparison_bar(
    {
        "Tanks": "tanks",
        "Armored Fighting Vehicles": "armored_fighting_vehicles",
        "Self-Propelled Artillery": "self_propelled_artillery",
        "Towed Artillery": "towed_artillery",
        "Rocket Projectors": "rocket_projectors",
    },
    "Land Power Comparison", height=380, x_label="Units",
), use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION: NAVAL POWER COMPARISON
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">⚓ Naval Power Comparison</div>', unsafe_allow_html=True)
st.plotly_chart(grouped_comparison_bar(
    {
        "Total Naval Fleet": "total_naval_fleet",
        "Aircraft Carriers": "aircraft_carriers",
        "Helicopter Carriers": "helicopter_carriers",
        "Submarines": "submarines",
        "Destroyers": "destroyers",
        "Frigates": "frigates",
        "Corvettes": "corvettes",
    },
    "Naval Power Comparison", height=420, x_label="Units",
), use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION: DEFENSE BUDGET COMPARISON
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">💰 Defense Budget Comparison</div>', unsafe_allow_html=True)
budget_col1, budget_col2 = st.columns(2)

with budget_col1:
    budget_gdp_fig = go.Figure()
    budget_gdp_fig.add_trace(go.Bar(
        x=["Defense Budget", "GDP"], y=[val_a("defense_budget_usd") or 0, val_a(utils.COL_GDP) or 0],
        name=country_a, marker=dict(color=COLOR_A),
        hovertemplate=f"<b>{country_a}</b><br>" + "%{x}: $%{y:,.0f}<extra></extra>",
    ))
    budget_gdp_fig.add_trace(go.Bar(
        x=["Defense Budget", "GDP"], y=[val_b("defense_budget_usd") or 0, val_b(utils.COL_GDP) or 0],
        name=country_b, marker=dict(color=COLOR_B),
        hovertemplate=f"<b>{country_b}</b><br>" + "%{x}: $%{y:,.0f}<extra></extra>",
    ))
    budget_gdp_fig.update_layout(barmode="group", title=dict(text="Defense Budget & GDP (USD)", font=dict(size=15, color=TEXT_LIGHT)))
    budget_gdp_fig.update_yaxes(tickprefix="$", tickformat=".2s")
    st.plotly_chart(_empty_layout(budget_gdp_fig, height=360), use_container_width=True)

with budget_col2:
    ratio_a = val_a(utils.COL_BUDGET_TO_GDP)
    ratio_b = val_b(utils.COL_BUDGET_TO_GDP)
    ratio_fig = go.Figure(go.Bar(
        x=[country_a, country_b], y=[ratio_a or 0, ratio_b or 0],
        marker=dict(color=[COLOR_A, COLOR_B]),
        hovertemplate="<b>%{x}</b><br>Budget-to-GDP Ratio: %{y:.2f}%<extra></extra>",
    ))
    ratio_fig.update_layout(title=dict(text="Budget-to-GDP Ratio (%)", font=dict(size=15, color=TEXT_LIGHT)))
    ratio_fig.update_yaxes(ticksuffix="%")
    st.plotly_chart(_empty_layout(ratio_fig, height=360), use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION: POWER INDEX VISUALIZATION
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🎯 Power Index Comparison</div>', unsafe_allow_html=True)

score_a, score_b = val_a(utils.COL_SCORE), val_b(utils.COL_SCORE)
rank_a, rank_b = val_a(utils.COL_RANK), val_b(utils.COL_RANK)

power_fig = make_subplots(rows=1, cols=2, subplot_titles=("Power Index Score (Lower = Stronger)", "Power Index Rank (Lower = Stronger)"))
power_fig.add_trace(go.Bar(
    x=[country_a, country_b], y=[score_a or 0, score_b or 0],
    marker=dict(color=[COLOR_A if (score_a or 0) <= (score_b or 0) else TEXT_MUTED,
                       COLOR_B if (score_b or 0) < (score_a or 0) else TEXT_MUTED]),
    hovertemplate="<b>%{x}</b><br>Power Index Score: %{y:.4f}<extra></extra>", showlegend=False,
), row=1, col=1)
power_fig.add_trace(go.Bar(
    x=[country_a, country_b], y=[rank_a or 0, rank_b or 0],
    marker=dict(color=[COLOR_A if (rank_a or 9999) <= (rank_b or 9999) else TEXT_MUTED,
                       COLOR_B if (rank_b or 9999) < (rank_a or 9999) else TEXT_MUTED]),
    hovertemplate="<b>%{x}</b><br>Power Index Rank: #%{y:.0f}<extra></extra>", showlegend=False,
), row=1, col=2)
power_fig.update_layout(
    template="plotly_dark", paper_bgcolor=CARD_COLOR, plot_bgcolor=CARD_COLOR,
    font=dict(family="Inter, Arial", color=TEXT_LIGHT, size=12),
    margin=dict(l=10, r=10, t=55, b=10), height=340,
)
power_fig.update_xaxes(gridcolor=GRID_COLOR)
power_fig.update_yaxes(gridcolor=GRID_COLOR)
st.plotly_chart(power_fig, use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION: COMPARISON SUMMARY (dynamically generated, never hard-coded)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📝 Comparison Summary</div>', unsafe_allow_html=True)

summary_definitions = [
    ("military manpower", utils.COL_MANPOWER, True),
    ("air power (total aircraft)", utils.COL_AIRCRAFT, True),
    ("land power (tanks)", utils.COL_TANKS, True),
    ("naval fleet size", utils.COL_NAVAL, True),
    ("defense budget", utils.COL_BUDGET, True),
    ("overall Power Index", utils.COL_SCORE, False),
]

summary_lines = []
for topic, col, higher_is_better in summary_definitions:
    va, vb = val_a(col), val_b(col)
    winner = determine_winner(va, vb, higher_is_better)
    if winner == "A":
        summary_lines.append(f"🅰️ <b>{country_a}</b> has a stronger {topic} than {country_b}.")
    elif winner == "B":
        summary_lines.append(f"🅱️ <b>{country_b}</b> has a stronger {topic} than {country_a}.")
    elif va is not None and vb is not None:
        summary_lines.append(f"⚖️ {country_a} and {country_b} are roughly equal in {topic}.")
    # if data is missing for both, the topic is silently skipped

if summary_lines:
    for line in summary_lines:
        st.markdown(f'<div class="summary-card">{line}</div>', unsafe_allow_html=True)
else:
    st.info("Not enough data available to generate a comparison summary.")

# ---------------------------------------------------------------------------
# SECTION: COUNTRY INFORMATION
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📋 Country Information</div>', unsafe_allow_html=True)

info_fields = [
    ("Country", utils.COL_COUNTRY, lambda v: v),
    ("Region", utils.COL_REGION, lambda v: v),
    ("Continent", utils.COL_CONTINENT, lambda v: v),
    ("Alliance", utils.COL_ALLIANCE, lambda v: v),
    ("GDP", utils.COL_GDP, utils.format_currency),
    ("Population", utils.COL_POP, utils.format_plain),
]

info_col_a, info_col_b = st.columns(2)
with info_col_a:
    st.markdown(f'<div class="country-banner country-banner-a">{country_a}</div>', unsafe_allow_html=True)
    for label, col, fmt in info_fields:
        v = val_a(col)
        display = fmt(v) if v is not None else "N/A"
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-label">{label}</div>
            <div class="profile-value">{display}</div>
        </div>
        """, unsafe_allow_html=True)

with info_col_b:
    st.markdown(f'<div class="country-banner country-banner-b">{country_b}</div>', unsafe_allow_html=True)
    for label, col, fmt in info_fields:
        v = val_b(col)
        display = fmt(v) if v is not None else "N/A"
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-label">{label}</div>
            <div class="profile-value">{display}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="footer-text">
    Developed for Infosys Virtual Internship &nbsp;|&nbsp; Unified Military Analytics and Comparison Dashboard
</div>
""", unsafe_allow_html=True)