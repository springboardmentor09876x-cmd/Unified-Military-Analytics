"""
pages/coalition_builder.py
---------------------------------------------------------------------------
Unified Military Analytics and Comparison Dashboard
Module 6 — Coalition Builder

Lets the user assemble two military coalitions (Coalition A / Coalition B)
from the real dataset (data/military_final.xlsx), plus a single Reference
Country, and compares them across manpower, air, land, naval and economic
dimensions using native Streamlit components styled as a premium dark navy
/ cyan / blue-purple command-center dashboard.
---------------------------------------------------------------------------
"""

import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ===========================================================================
# PAGE CONFIG
# ===========================================================================
try:
    st.set_page_config(
        page_title="Coalition Builder | UMACD",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except Exception:
    # set_page_config can only be called once per script run — if this page
    # is ever imported rather than run directly, ignore the duplicate call.
    pass

# ===========================================================================
# THEME CONSTANTS — dark navy / cyan / blue-purple command-center palette.
# Purely visual — used only by CSS below and by the Plotly styling helpers
# further down. No data, calculation, or logic value derives from these.
# ===========================================================================
BG_1 = "#071426"
BG_2 = "#0A1B33"
BG_3 = "#0D2340"

CARD_1 = "#10294A"
CARD_2 = "#132F52"
CARD_3 = "#0E2645"

CYAN = "#20C4E8"
CYAN_2 = "#27B9E8"
PURPLE = "#5865F2"
PURPLE_2 = "#7357D9"

TEXT_WHITE = "#F5F7FA"
TEXT_LIGHT = "#B8C4D4"
TEXT_MUTED = "#718096"

BORDER_SOFT = "rgba(39, 185, 232, 0.18)"
GRID_COLOR = "rgba(184, 196, 212, 0.10)"

# ---------------------------------------------------------------------------
# Coalition Country Table — dedicated blue/midnight-blue palette so the
# table blends into the surrounding dashboard. NOTE: st.dataframe() renders
# through Glide Data Grid (a canvas/WebGL component), so its cell surface
# cannot be repainted with CSS -- that is why earlier CSS-only attempts had
# no visible effect. The table below is instead rendered as a real HTML
# <table> (see build_coalition_table_html()), which these colors style
# directly and reliably.
# ---------------------------------------------------------------------------
TABLE_BG_MAIN = "#071A33"
TABLE_BG_LIGHT = "#0B2342"
TABLE_SURFACE = "#0D2747"
TABLE_HEADER = "#102E52"
TABLE_BORDER = "#1E5A7A"
TABLE_TEXT = "#F5F7FF"

# ===========================================================================
# GLOBAL CSS — restyles native Streamlit components only (metric, header,
# sidebar, divider, dataframe, selectbox, multiselect, buttons). No
# Streamlit call signatures, data, or logic are touched anywhere below.
# ===========================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', 'Segoe UI', sans-serif; }}

    .stApp {{
        background: radial-gradient(circle at 10% 0%, {BG_3}AA 0%, {BG_2} 45%, {BG_1} 100%);
        color: {TEXT_LIGHT};
    }}

    div.block-container {{
        padding-top: 2.6rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* ---------------- Sidebar ---------------- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BG_2} 0%, #060F1E 100%);
        border-right: 1px solid {BORDER_SOFT};
    }}
    section[data-testid="stSidebar"] * {{
        color: {TEXT_LIGHT} !important;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {TEXT_WHITE} !important;
    }}
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {CARD_1} !important;
        border: 1px solid {BORDER_SOFT} !important;
        border-radius: 10px !important;
    }}
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {{
        background-color: rgba(32, 196, 232, 0.18) !important;
        border: 1px solid rgba(32, 196, 232, 0.45) !important;
        color: {TEXT_WHITE} !important;
        border-radius: 8px !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: {BORDER_SOFT} !important;
    }}

    /* ---------------- Titles / headers ---------------- */
    h1, h2, h3, h4, h5 {{
        color: {TEXT_WHITE} !important;
        font-weight: 800 !important;
        letter-spacing: 0.2px;
    }}
    .stApp > header {{
        background: transparent;
    }}
    div[data-testid="stAppViewContainer"] h1:first-of-type {{
        border-bottom: 2px solid {CYAN};
        padding-bottom: 0.6rem;
        text-shadow: 0 0 18px rgba(32, 196, 232, 0.25);
    }}
    div[data-testid="stHeading"] h2 {{
        border-left: 4px solid {CYAN};
        padding-left: 0.7rem;
        margin-top: 0.4rem !important;
        text-shadow: 0 0 10px rgba(32, 196, 232, 0.15);
    }}
    div[data-testid="stHeading"] h3 {{
        border-left: 3px solid {PURPLE_2};
        padding-left: 0.6rem;
    }}

    /* Caption / info / warning boxes */
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {TEXT_MUTED} !important;
    }}
    div[data-testid="stAlert"] {{
        background-color: {CARD_3} !important;
        border: 1px solid {BORDER_SOFT} !important;
        border-radius: 12px !important;
        color: {TEXT_LIGHT} !important;
    }}

    /* ---------------- Dividers ---------------- */
    hr {{
        border: none;
        border-top: 1px solid {BORDER_SOFT};
        margin: 1.4rem 0;
    }}

    /* ---------------- KPI / st.metric cards ---------------- */
    div[data-testid="stMetric"] {{
        background: linear-gradient(160deg, {CARD_2} 0%, {CARD_3} 100%);
        border: 1px solid {BORDER_SOFT};
        border-radius: 14px;
        padding: 0.9rem 1.1rem 0.8rem 1.1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.35);
        position: relative;
        overflow: hidden;
        transition: all 0.18s ease-in-out;
    }}
    div[data-testid="stMetric"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {CYAN}, {PURPLE});
    }}
    div[data-testid="stMetric"]:hover {{
        border-color: {CYAN};
        box-shadow: 0 4px 18px rgba(32, 196, 232, 0.22);
        transform: translateY(-2px);
    }}
    div[data-testid="stMetricLabel"] {{
        color: {TEXT_MUTED} !important;
        font-size: 0.74rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    div[data-testid="stMetricValue"] {{
        color: {TEXT_WHITE} !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
    }}
    div[data-testid="stMetricDelta"] {{
        font-weight: 700 !important;
        font-size: 0.8rem !important;
    }}

    /* ---------------- Plotly chart container ---------------- */
    div[data-testid="stPlotlyChart"] {{
        background: linear-gradient(160deg, {CARD_2}55 0%, {CARD_3}55 100%);
        border: 1px solid {BORDER_SOFT};
        border-radius: 16px;
        padding: 10px 14px;
        margin-bottom: 0.6rem;
    }}

    /* ---------------- Selectbox / Multiselect (main area) ---------------- */
    div[data-baseweb="select"] > div {{
        background-color: {CARD_1} !important;
        border: 1px solid {BORDER_SOFT} !important;
        border-radius: 10px !important;
        color: {TEXT_WHITE} !important;
    }}
    div[data-baseweb="popover"] {{
        background-color: {CARD_1} !important;
    }}
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background-color: {CARD_1} !important;
    }}

    /* ---------------- Coalition Country Table (custom HTML table) ----------
       st.dataframe() renders through Glide Data Grid, a canvas/WebGL
       component whose cell surface cannot be restyled with CSS -- that is
       why the visible table stayed white/black regardless of earlier CSS
       attempts. The Coalition Country Table below is instead rendered as a
       real HTML <table> (see build_coalition_table_html()), which these
       rules style directly, reliably, and consistently with the rest of
       the blue/navy dashboard. Only presentation is affected here -- the
       underlying data, column set, and sort order are unchanged.
    ------------------------------------------------------------------- */
    .coalition-table-wrapper {{
        overflow-x: auto;
        border-radius: 14px;
        border: 1px solid {TABLE_BORDER};
        background-color: {TABLE_BG_MAIN};
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.35);
    }}
    table.coalition-data-table {{
        width: 100%;
        border-collapse: collapse;
        background-color: {TABLE_BG_MAIN};
        font-size: 0.86rem;
    }}
    table.coalition-data-table thead th {{
        background-color: {TABLE_HEADER};
        color: {TABLE_TEXT};
        text-align: left;
        padding: 10px 14px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.04em;
        border-bottom: 1px solid {TABLE_BORDER};
        white-space: nowrap;
    }}
    table.coalition-data-table tbody td {{
        padding: 9px 14px;
        color: {TABLE_TEXT};
        background-color: {TABLE_SURFACE};
        border-bottom: 1px solid {TABLE_BORDER}55;
        white-space: nowrap;
    }}
    table.coalition-data-table tbody tr:nth-child(even) td {{
        background-color: {TABLE_BG_LIGHT};
    }}
    table.coalition-data-table tbody tr:hover td {{
        background-color: rgba(32, 196, 232, 0.10);
    }}
    .coalition-table-empty {{
        color: {TEXT_MUTED};
        font-style: italic;
        padding: 1rem 0;
    }}

    /* ---------------- Buttons ---------------- */
    .stButton > button, .stDownloadButton > button {{
        background: linear-gradient(90deg, {CYAN_2}, {PURPLE}) !important;
        color: {TEXT_WHITE} !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 10px rgba(32, 196, 232, 0.25);
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        box-shadow: 0 4px 16px rgba(115, 87, 217, 0.35);
        transform: translateY(-1px);
    }}

    /* ---------------- Plain text / write blocks ---------------- */
    div[data-testid="stMarkdownContainer"] p {{
        color: {TEXT_LIGHT};
    }}
</style>
""", unsafe_allow_html=True)

# ===========================================================================
# REQUIRED DATASET COLUMNS
# ===========================================================================
REQUIRED_COLUMNS = [
    "country",
    "power_index_rank",
    "power_index_score",
    "active_personnel",
    "reserve_personnel",
    "paramilitary",
    "total_military_manpower",
    "total_military_aircraft",
    "fighter_aircraft",
    "attack_aircraft",
    "transport_aircraft",
    "total_military_helicopters",
    "tanks",
    "armored_fighting_vehicles",
    "self_propelled_artillery",
    "towed_artillery",
    "rocket_projectors",
    "total_naval_fleet",
    "aircraft_carriers",
    "helicopter_carriers",
    "submarines",
    "destroyers",
    "frigates",
    "corvettes",
    "defense_budget_usd",
    "GDP",
    "total_population",
    "Region",
    "Continent",
    "Alliance",
]

COUNTRY_COL = "country"
RANK_COL = "power_index_rank"
SCORE_COL = "power_index_score"

MANPOWER_METRICS = [
    ("active_personnel", "Active Personnel"),
    ("reserve_personnel", "Reserve Personnel"),
    ("paramilitary", "Paramilitary"),
]
AIR_METRICS = [
    ("total_military_aircraft", "Total Aircraft"),
    ("fighter_aircraft", "Fighter Aircraft"),
    ("attack_aircraft", "Attack Aircraft"),
    ("transport_aircraft", "Transport Aircraft"),
    ("total_military_helicopters", "Helicopters"),
]
LAND_METRICS = [
    ("tanks", "Tanks"),
    ("armored_fighting_vehicles", "Armored Fighting Vehicles"),
    ("self_propelled_artillery", "Self-Propelled Artillery"),
    ("towed_artillery", "Towed Artillery"),
    ("rocket_projectors", "Rocket Projectors"),
]
NAVAL_METRICS = [
    ("total_naval_fleet", "Total Naval Fleet"),
    ("aircraft_carriers", "Aircraft Carriers"),
    ("helicopter_carriers", "Helicopter Carriers"),
    ("submarines", "Submarines"),
    ("destroyers", "Destroyers"),
    ("frigates", "Frigates"),
    ("corvettes", "Corvettes"),
]

# KPI catalogue: (column, label, format_type)
# format_type: "count" -> comma separated | "large" -> K/M/B/T suffix | "currency" -> $ + suffix
KPI_METRICS = [
    ("total_military_manpower", "Total Military Manpower", "large"),
    ("active_personnel", "Active Personnel", "count"),
    ("reserve_personnel", "Reserve Personnel", "count"),
    ("total_military_aircraft", "Total Military Aircraft", "count"),
    ("fighter_aircraft", "Fighter Aircraft", "count"),
    ("tanks", "Tanks", "count"),
    ("total_naval_fleet", "Total Naval Fleet", "count"),
    ("submarines", "Submarines", "count"),
    ("defense_budget_usd", "Defense Budget", "currency"),
    ("GDP", "GDP", "currency"),
    ("total_population", "Population", "large"),
]

CONTRIB_METRICS = [
    ("total_military_manpower", "Manpower"),
    ("total_military_aircraft", "Aircraft"),
    ("tanks", "Tanks"),
    ("total_naval_fleet", "Naval Fleet"),
    ("defense_budget_usd", "Defense Budget"),
]

VS_REF_METRICS = [
    ("total_military_manpower", "Manpower"),
    ("total_military_aircraft", "Aircraft"),
    ("tanks", "Tanks"),
    ("total_naval_fleet", "Naval Fleet"),
    ("defense_budget_usd", "Defense Budget"),
]


# ===========================================================================
# DATA LOADING
# ===========================================================================
@st.cache_data(show_spinner="Loading coalition dataset...")
def load_military_data():
    """
    Loads data/military_final.xlsx using the EXACT column names supplied by
    the project (no renaming). Path is resolved relative to the project
    root (one level above this /pages file) so it works regardless of the
    current working directory the app is launched from.

    Returns (dataframe, error_message). error_message is None on success.
    """
    pages_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(pages_dir)
    data_path = os.path.join(project_root, "data", "military_final.xlsx")

    if not os.path.exists(data_path):
        return None, f"Dataset not found at expected path: `{data_path}`."

    try:
        data = pd.read_excel(data_path, engine="openpyxl")
    except Exception as exc:
        return None, f"Failed to read the Excel file: {exc}"

    data.columns = [str(c).strip() for c in data.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        return None, "The dataset is missing required column(s): " + ", ".join(missing)

    # Clean whitespace in text columns.
    text_cols = data.select_dtypes(include="object").columns
    for c in text_cols:
        data[c] = data[c].astype(str).str.strip()

    # Fill numeric NaNs with 0 so no chart/KPI ever shows "NaN".
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data[numeric_cols] = data[numeric_cols].fillna(0)

    return data, None


df, load_error = load_military_data()

if load_error:
    st.error(f"⚠️ {load_error}")
    st.stop()

if df is None or df.empty:
    st.error("⚠️ The dataset loaded but contains no rows.")
    st.stop()


# ===========================================================================
# FORMATTING HELPERS
# ===========================================================================
def fmt_count(v) -> str:
    if v is None or pd.isna(v):
        return "N/A"
    return f"{v:,.0f}"


def fmt_large(v) -> str:
    if v is None or pd.isna(v):
        return "N/A"
    a = abs(v)
    if a >= 1_000_000_000_000:
        return f"{v/1_000_000_000_000:.2f}T"
    if a >= 1_000_000_000:
        return f"{v/1_000_000_000:.2f}B"
    if a >= 1_000_000:
        return f"{v/1_000_000:.2f}M"
    if a >= 1_000:
        return f"{v/1_000:.2f}K"
    return f"{v:,.0f}"


def fmt_currency(v) -> str:
    if v is None or pd.isna(v):
        return "N/A"
    return "$" + fmt_large(v)


def fmt_by_type(v, fmt_type):
    if fmt_type == "count":
        return fmt_count(v)
    if fmt_type == "currency":
        return fmt_currency(v)
    return fmt_large(v)


def pct_delta(value, base):
    """Percentage delta of `value` vs `base`. Returns None if base is 0/NaN/missing."""
    if base is None or pd.isna(base) or base == 0:
        return None
    return (value - base) / base * 100.0


def fmt_delta(delta):
    """Text used as the `delta` argument of st.metric(). None -> no delta shown."""
    if delta is None:
        return None
    return f"{delta:+.1f}% vs Reference"


# ===========================================================================
# AGGREGATION LOGIC
# ===========================================================================
def get_group_df(countries):
    """Subset of the dataframe for the given list of country names."""
    if not countries:
        return df.iloc[0:0]
    return df[df[COUNTRY_COL].isin(countries)]


def aggregate_group(group_df: pd.DataFrame) -> dict:
    """
    Builds the aggregate metric dictionary for a coalition (or a
    single-country reference group treated the same way).
    Sums are used for additive military/economic quantities; the Power
    Index Score is averaged (not summed) since it is a relative ranking
    metric, not an additive one.
    """
    agg = {"count": int(group_df.shape[0])}

    numeric_cols = set(group_df.select_dtypes(include=[np.number]).columns)
    all_metric_cols = (
        [m[0] for m in KPI_METRICS]
        + [m[0] for m in MANPOWER_METRICS]
        + [m[0] for m in AIR_METRICS]
        + [m[0] for m in LAND_METRICS]
        + [m[0] for m in NAVAL_METRICS]
    )
    for col in set(all_metric_cols):
        if col in numeric_cols:
            agg[col] = float(group_df[col].sum())
        else:
            agg[col] = 0.0

    if group_df.empty:
        agg["avg_power_index_score"] = None
        agg["best_rank"] = None
        agg["best_rank_country"] = None
        agg["agg_budget_to_gdp"] = None
    else:
        agg["avg_power_index_score"] = float(group_df[SCORE_COL].mean())
        best_row = group_df.loc[group_df[RANK_COL].idxmin()]
        agg["best_rank"] = int(best_row[RANK_COL])
        agg["best_rank_country"] = best_row[COUNTRY_COL]
        total_gdp = agg.get("GDP", 0.0)
        agg["agg_budget_to_gdp"] = (
            agg.get("defense_budget_usd", 0.0) / total_gdp * 100.0
        ) if total_gdp else None

    return agg


# ===========================================================================
# CHART BUILDER — navy/cyan/purple styling only. Data, trace order, trace
# names, and hovertemplate content are unchanged from the original.
# ===========================================================================
def _style_layout(fig, height):
    """Shared dark navy chart chrome applied on top of the existing traces."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, Arial", color=TEXT_LIGHT, size=12.5),
        height=height,
        margin=dict(l=10, r=16, t=16, b=10),
        legend=dict(orientation="h", y=-0.16, x=0.5, xanchor="center",
                    bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_LIGHT)),
        hoverlabel=dict(bgcolor=CARD_1, font_size=12.5, font_family="Inter, Arial",
                         bordercolor=BORDER_SOFT, font_color=TEXT_WHITE),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=TEXT_LIGHT)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=TEXT_LIGHT)
    return fig


def grouped_bar_chart(metric_list, agg_a, agg_b, agg_ref, name_a, name_b, name_ref, height=380):
    """Grouped horizontal bar chart comparing Coalition A / B / Reference across a metric list."""
    labels = [m[1] for m in metric_list]
    vals_a = [agg_a.get(m[0], 0.0) for m in metric_list]
    vals_b = [agg_b.get(m[0], 0.0) for m in metric_list]
    vals_ref = [agg_ref.get(m[0], 0.0) for m in metric_list]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=vals_a, name=name_a, orientation="h",
        marker=dict(color=CYAN, line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
        hovertemplate="<b>%{y}</b><br>" + name_a + ": %{x:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=labels, x=vals_b, name=name_b, orientation="h",
        marker=dict(color=PURPLE_2, line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
        hovertemplate="<b>%{y}</b><br>" + name_b + ": %{x:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=labels, x=vals_ref, name=name_ref, orientation="h",
        marker=dict(color=TEXT_MUTED, line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
        hovertemplate="<b>%{y}</b><br>" + name_ref + ": %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        barmode="group",
        yaxis=dict(autorange="reversed"),
    )
    return _style_layout(fig, height)


def contribution_bar(group_df, metric_col, metric_label):
    """Simple horizontal bar chart of each country's contribution within its coalition."""
    if group_df.empty or metric_col not in group_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="No countries selected", showarrow=False,
            font=dict(size=13, color=TEXT_MUTED),
            xref="paper", yref="paper", x=0.5, y=0.5,
        )
        fig.update_layout(height=260, margin=dict(l=10, r=16, t=16, b=10))
        return _style_layout(fig, 260)

    d = group_df[[COUNTRY_COL, metric_col]].copy().sort_values(metric_col, ascending=True)
    total = d[metric_col].sum()
    d["share"] = (d[metric_col] / total * 100.0) if total else 0.0

    fig = go.Figure(go.Bar(
        x=d[metric_col], y=d[COUNTRY_COL], orientation="h",
        marker=dict(
            color=d[metric_col],
            colorscale=[[0, PURPLE_2], [1, CYAN]],
            showscale=False,
            line=dict(color="rgba(255,255,255,0.06)", width=0.5),
        ),
        customdata=d["share"],
        text=[f"{s:.1f}%" for s in d["share"]],
        textposition="outside",
        textfont=dict(color=TEXT_LIGHT),
        hovertemplate=f"<b>%{{y}}</b><br>{metric_label}: %{{x:,.0f}}<br>Share of coalition: %{{customdata:.1f}}%<extra></extra>",
    ))
    fig.update_layout(
        xaxis_title=metric_label,
        yaxis_title="",
    )
    return _style_layout(fig, max(260, 34 * len(d) + 60))


# ===========================================================================
# COALITION COUNTRY TABLE — custom HTML renderer (see CSS note above for
# why st.dataframe() could not be re-colored). Formats the SAME columns,
# in the SAME order, with the SAME number formatting that the previous
# st.dataframe(column_config=...) call used, so only the visible surface
# changes, not the content.
# ===========================================================================
def build_coalition_table_html(display_df: pd.DataFrame) -> str:
    """
    Renders display_df as a styled HTML <table> matching the previous
    st.dataframe column_config formatting exactly:
      - Power Index Score -> 4 decimal places
      - Military Manpower / Aircraft / Tanks / Naval Fleet -> comma-separated integers
      - Defense Budget / GDP -> $ + comma-separated integers
      - all other columns -> shown as-is
    """
    formatted = display_df.copy()

    if "Power Index Score" in formatted.columns:
        formatted["Power Index Score"] = formatted["Power Index Score"].map(
            lambda v: f"{v:.4f}" if pd.notna(v) else ""
        )
    for col in ["Military Manpower", "Aircraft", "Tanks", "Naval Fleet"]:
        if col in formatted.columns:
            formatted[col] = formatted[col].map(
                lambda v: f"{v:,.0f}" if pd.notna(v) else ""
            )
    for col in ["Defense Budget", "GDP"]:
        if col in formatted.columns:
            formatted[col] = formatted[col].map(
                lambda v: f"${v:,.0f}" if pd.notna(v) else ""
            )

    html_table = formatted.to_html(
        index=False,
        classes="coalition-data-table",
        border=0,
        escape=True,
    )
    return f'<div class="coalition-table-wrapper">{html_table}</div>'


# ===========================================================================
# HEADER
# ===========================================================================
st.title("🛡️ Coalition Builder")
st.caption("Build and compare military coalitions using real-world defense metrics")
st.info(f"📊 {len(df)} nations analyzed in the current dataset.")

# ===========================================================================
# SIDEBAR — COALITION CONFIGURATION
# ===========================================================================
all_countries = sorted(df[COUNTRY_COL].dropna().unique().tolist())

st.sidebar.header("⚙️ Coalition Configuration")
st.sidebar.caption("Select countries to build and compare custom military coalitions.")

st.sidebar.subheader("🟢 Coalition A")
default_a = [c for c in ["United States", "India", "Japan"] if c in all_countries]
coalition_a = st.sidebar.multiselect(
    "Select Coalition A countries", options=all_countries, default=default_a, key="coalition_a_select",
)

st.sidebar.subheader("🟡 Coalition B")
default_b = [c for c in ["China", "Russia"] if c in all_countries]
coalition_b = st.sidebar.multiselect(
    "Select Coalition B countries", options=all_countries, default=default_b, key="coalition_b_select",
)

st.sidebar.subheader("🔵 Reference Country")
default_ref_index = all_countries.index("United States") if "United States" in all_countries else 0
reference_country = st.sidebar.selectbox(
    "Select a reference country", options=all_countries, index=default_ref_index, key="reference_select",
)

st.sidebar.markdown("---")
st.sidebar.caption("All KPIs, charts and tables below update automatically based on your selections.")

# ===========================================================================
# VALIDATION — graceful, no crashes
# ===========================================================================
if not coalition_a:
    st.warning("⚠️ **Coalition A is empty.** Please select at least one country for Coalition A from the sidebar to view the comparison dashboard.")
    st.stop()

if not coalition_b:
    st.warning("⚠️ **Coalition B is empty.** Please select at least one country for Coalition B from the sidebar to view the comparison dashboard.")
    st.stop()

# ===========================================================================
# BUILD GROUP DATA + AGGREGATES
# ===========================================================================
df_a = get_group_df(coalition_a)
df_b = get_group_df(coalition_b)
df_ref = get_group_df([reference_country])

agg_a = aggregate_group(df_a)
agg_b = aggregate_group(df_b)
agg_ref = aggregate_group(df_ref)

NAME_A, NAME_B, NAME_REF = "Coalition A", "Coalition B", "Reference"

# ===========================================================================
# COALITION A / B / REFERENCE OVERVIEW
# ===========================================================================
st.divider()
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🟢 Coalition A")
    st.caption(f"{len(coalition_a)} countries selected")
    st.write(", ".join(coalition_a))

with c2:
    st.subheader("🟡 Coalition B")
    st.caption(f"{len(coalition_b)} countries selected")
    st.write(", ".join(coalition_b))

with c3:
    st.subheader("🔵 Reference Country")
    st.caption("Single-country baseline")
    st.write(reference_country)

# ===========================================================================
# KPI SECTION
# ===========================================================================
st.divider()
st.header("📊 Key Metric Comparison")
st.caption("Coalition A vs Coalition B vs Reference Country — percentages compare each coalition against the Reference baseline.")

for col, label, fmt_type in KPI_METRICS:
    val_a = agg_a.get(col, 0.0)
    val_b = agg_b.get(col, 0.0)
    val_ref = agg_ref.get(col, 0.0)
    delta_a = pct_delta(val_a, val_ref)
    delta_b = pct_delta(val_b, val_ref)

    st.markdown(f"**{label}**")
    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric(label="Coalition A", value=fmt_by_type(val_a, fmt_type), delta=fmt_delta(delta_a))
    with k2:
        st.metric(label="Coalition B", value=fmt_by_type(val_b, fmt_type), delta=fmt_delta(delta_b))
    with k3:
        st.metric(label="Reference", value=fmt_by_type(val_ref, fmt_type))

# ===========================================================================
# POWER INDEX ANALYSIS
# ===========================================================================
st.divider()
st.header("⚔️ Power Index Analysis")
st.caption(
    "Power Index Score is a relative ranking metric where a LOWER score means a STRONGER "
    "military. It is averaged (not summed) across coalition members because it is not an "
    "additive quantity. The 'Best Ranked Member' is the single strongest country "
    "(lowest power_index_rank) inside each group."
)

p1, p2, p3 = st.columns(3)
groups_for_power = [
    (p1, NAME_A, agg_a),
    (p2, NAME_B, agg_b),
    (p3, NAME_REF, agg_ref),
]
for col_widget, name, agg in groups_for_power:
    with col_widget:
        st.subheader(name)
        avg_score = agg.get("avg_power_index_score")
        best_country = agg.get("best_rank_country") or "N/A"
        best_rank = agg.get("best_rank")
        st.metric("Average Power Index Score", f"{avg_score:.4f}" if avg_score is not None else "N/A")
        st.write(f"**Best Ranked Member:** {best_country} (Rank #{best_rank if best_rank is not None else 'N/A'})")
        st.write(f"**Countries in Group:** {agg.get('count', 0)}")

# ===========================================================================
# MILITARY MANPOWER / AIR / LAND / NAVAL POWER CHARTS
# ===========================================================================
st.divider()
st.header("🎖️ Military Manpower")
st.caption("Active Personnel, Reserve Personnel and Paramilitary forces compared across groups.")
st.plotly_chart(
    grouped_bar_chart(MANPOWER_METRICS, agg_a, agg_b, agg_ref, NAME_A, NAME_B, NAME_REF, height=340),
    use_container_width=True,
)

st.divider()
st.header("✈️ Air Power")
st.caption("Total Aircraft, Fighters, Attack Aircraft, Transport Aircraft and Helicopters.")
st.plotly_chart(
    grouped_bar_chart(AIR_METRICS, agg_a, agg_b, agg_ref, NAME_A, NAME_B, NAME_REF, height=380),
    use_container_width=True,
)

st.divider()
st.header("🏜️ Land Power")
st.caption("Tanks, Armored Fighting Vehicles, Self-Propelled & Towed Artillery and Rocket Projectors.")
st.plotly_chart(
    grouped_bar_chart(LAND_METRICS, agg_a, agg_b, agg_ref, NAME_A, NAME_B, NAME_REF, height=380),
    use_container_width=True,
)

st.divider()
st.header("⚓ Naval Power")
st.caption("Total Naval Fleet, Carriers, Submarines, Destroyers, Frigates and Corvettes.")
st.plotly_chart(
    grouped_bar_chart(NAVAL_METRICS, agg_a, agg_b, agg_ref, NAME_A, NAME_B, NAME_REF, height=420),
    use_container_width=True,
)

# ===========================================================================
# DEFENSE ECONOMICS
# ===========================================================================
st.divider()
st.header("💰 Defense Economics")
st.caption(
    "Defense Budget and GDP are summed across each group. Budget-to-GDP is computed as "
    "total defense budget ÷ total GDP (not averaged per-country) for a mathematically "
    "sound aggregate ratio."
)

e1, e2, e3 = st.columns(3)
econ_groups = [(e1, NAME_A, agg_a), (e2, NAME_B, agg_b), (e3, NAME_REF, agg_ref)]
for col_widget, name, agg in econ_groups:
    with col_widget:
        st.subheader(name)
        ratio = agg.get("agg_budget_to_gdp")
        ratio_str = f"{ratio:.2f}%" if ratio is not None else "N/A"
        st.metric("Defense Budget", fmt_currency(agg.get("defense_budget_usd", 0.0)))
        st.metric("GDP", fmt_currency(agg.get("GDP", 0.0)))
        st.metric("Budget-to-GDP Ratio", ratio_str)

# ===========================================================================
# COALITION COMPOSITION / COUNTRY CONTRIBUTION
# ===========================================================================
st.divider()
st.header("📈 Country Contribution")
st.caption("Choose a metric to see how much each country contributes within its coalition.")

metric_choice_label = st.selectbox(
    "Select metric to analyze", options=[m[1] for m in CONTRIB_METRICS], index=0, key="contrib_metric",
)
metric_choice_col = dict((label, col) for col, label in CONTRIB_METRICS)[metric_choice_label]

cc1, cc2 = st.columns(2)
with cc1:
    st.subheader(f"Coalition A — {metric_choice_label}")
    st.plotly_chart(
        contribution_bar(df_a, metric_choice_col, metric_choice_label),
        use_container_width=True,
    )
with cc2:
    st.subheader(f"Coalition B — {metric_choice_label}")
    st.plotly_chart(
        contribution_bar(df_b, metric_choice_col, metric_choice_label),
        use_container_width=True,
    )

# ===========================================================================
# COALITION vs REFERENCE
# ===========================================================================
st.divider()
st.header("🎯 Coalition vs Reference")
st.caption(f"Percentage advantage or disadvantage of Coalition A and Coalition B relative to {reference_country} (baseline = 0%).")

for col, label in VS_REF_METRICS:
    ref_val = agg_ref.get(col, 0.0)
    d_a = pct_delta(agg_a.get(col, 0.0), ref_val)
    d_b = pct_delta(agg_b.get(col, 0.0), ref_val)

    st.markdown(f"**{label}**")
    v1, v2, v3 = st.columns(3)
    with v1:
        st.metric("Coalition A", fmt_delta(d_a) if d_a is not None else "N/A")
    with v2:
        st.metric("Coalition B", fmt_delta(d_b) if d_b is not None else "N/A")
    with v3:
        st.metric("Reference", "Baseline")

# ===========================================================================
# COALITION SUMMARY (auto-generated, no hard-coded results)
# ===========================================================================
st.divider()
st.header("🏆 Coalition Summary")

summary_metrics = [
    ("total_military_manpower", "combined military manpower"),
    ("total_military_aircraft", "combined aircraft fleet"),
    ("tanks", "combined tank force"),
    ("total_naval_fleet", "larger naval capacity"),
    ("defense_budget_usd", "combined defense budget"),
]

summary_lines = []
for col, phrase in summary_metrics:
    val_a, val_b = agg_a.get(col, 0.0), agg_b.get(col, 0.0)
    if val_a == val_b:
        summary_lines.append(f"Coalition A and Coalition B have an equal {phrase}.")
    else:
        stronger = NAME_A if val_a > val_b else NAME_B
        if col == "total_naval_fleet":
            summary_lines.append(f"{stronger} has {phrase}.")
        else:
            summary_lines.append(f"{stronger} has the {phrase}.")

# Power index comparison (lower average score = stronger)
score_a, score_b = agg_a.get("avg_power_index_score"), agg_b.get("avg_power_index_score")
if score_a is not None and score_b is not None:
    if score_a < score_b:
        summary_lines.append(f"{NAME_A} has the stronger average Power Index Score ({score_a:.4f} vs {score_b:.4f}).")
    elif score_b < score_a:
        summary_lines.append(f"{NAME_B} has the stronger average Power Index Score ({score_b:.4f} vs {score_a:.4f}).")
    else:
        summary_lines.append("Coalition A and Coalition B have an identical average Power Index Score.")

for line in summary_lines:
    st.write(f"✓ {line}")

# ===========================================================================
# COALITION COUNTRY TABLE
# ===========================================================================
st.divider()
st.header("📋 Coalition Country Table")
st.caption("All selected coalition & reference countries with key comparison metrics.")

table_cols = {
    COUNTRY_COL: "Country",
    RANK_COL: "Power Index Rank",
    SCORE_COL: "Power Index Score",
    "total_military_manpower": "Military Manpower",
    "total_military_aircraft": "Aircraft",
    "tanks": "Tanks",
    "total_naval_fleet": "Naval Fleet",
    "defense_budget_usd": "Defense Budget",
    "GDP": "GDP",
    "Region": "Region",
    "Continent": "Continent",
    "Alliance": "Alliance",
}


def _tagged(group_df, tag):
    if group_df.empty:
        return group_df.assign(Coalition=tag)
    out = group_df.copy()
    out["Coalition"] = tag
    return out


tbl_a = _tagged(df_a, "Coalition A")
tbl_b = _tagged(df_b, "Coalition B")
tbl_ref = _tagged(df_ref, "Reference")

combined_tbl = pd.concat([tbl_a, tbl_b, tbl_ref], ignore_index=True)

# If a country appears in more than one group (user selected it twice, or it
# is also the reference country), merge its Coalition tags instead of
# showing duplicate rows.
if not combined_tbl.empty:
    combined_tbl = (
        combined_tbl.groupby(COUNTRY_COL, as_index=False)
        .agg({**{c: "first" for c in combined_tbl.columns if c not in (COUNTRY_COL, "Coalition")},
              "Coalition": lambda s: " & ".join(sorted(set(s)))})
    )

    display_tbl = combined_tbl[list(table_cols.keys()) + ["Coalition"]].rename(columns=table_cols)
    display_tbl = display_tbl[["Country", "Coalition"] + [v for k, v in table_cols.items() if k != COUNTRY_COL]]
    display_tbl = display_tbl.sort_values("Power Index Rank")

    st.markdown(build_coalition_table_html(display_tbl), unsafe_allow_html=True)
else:
    st.markdown('<div class="coalition-table-empty">No countries to display.</div>', unsafe_allow_html=True)

# ===========================================================================
# FOOTER
# ===========================================================================
st.divider()
st.caption("Unified Military Analytics and Comparison Dashboard • Module 6 — Coalition Builder • Developed for Infosys Virtual Internship")