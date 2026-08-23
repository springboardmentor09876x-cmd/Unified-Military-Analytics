"""
app.py
------
Unified Military Analytics and Comparison Dashboard
Module 5 - Dashboard Development (Quick Stats Dashboard)

Responsibilities of this file ONLY:
    - Page config / dark theme CSS
    - Header
    - Sidebar (navigation, filters, about)
    - KPI cards
    - Chart grid layout (calls functions from charts.py)
    - Country search card
    - Interactive data table
    - Footer

All data loading/filtering lives in utils.py.
All Plotly chart-building lives in charts.py.

NOTE ON CHART COLORS: charts.py is shared with the other pages (Nation
Overview / Compare Powers / Coalition Builder), so it is intentionally NOT
modified here. Instead, `_apply_qs_chart_theme()` below re-colors each
Plotly Figure object AFTER charts.py builds it and BEFORE it is rendered
on this page only -- so the Quick Stats Dashboard gets the pink/magenta
theme without touching charts.py or affecting any other page.
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import utils
import charts

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Unified Military Analytics | Quick Stats",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# QUICK STATS DASHBOARD — LOCAL UI THEME CONSTANTS (presentation only)
# ---------------------------------------------------------------------------
# Defined LOCALLY inside app.py (not imported from charts.py) so this
# visual refresh only affects the Quick Stats Dashboard page. Palette
# follows the requested deep navy / dark purple / magenta / pink scheme.
QS_BG_DEEP = "#0B0618"        # deep background
QS_BG_PURPLE = "#160B2E"      # dark purple background
QS_CARD = "#170D30"           # card / panel background
QS_PURPLE = "#5B1FA8"         # purple
QS_MAGENTA = "#9D1978"        # magenta
QS_PINK = "#D4148E"           # pink
QS_PINK_BRIGHT = "#F04BA8"    # bright pink
QS_PINK_SOFT = "#FF73C8"      # soft pink (hover / highlight)
QS_TEXT_LIGHT = "#F5F5F7"     # white
QS_TEXT_MUTED = "#A9A4B8"     # muted text
QS_GRID = "#2A2038"           # gridline / subtle border

# ---------------------------------------------------------------------------
# DARK NAVY / PURPLE / MAGENTA / PINK ANALYTICS THEME CSS
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }}
    .stApp {{
        background:
            radial-gradient(circle at 12% 8%, rgba(91,31,168,0.28) 0%, rgba(11,6,24,0) 42%),
            radial-gradient(circle at 88% 88%, rgba(255,115,200,0.10) 0%, rgba(11,6,24,0) 40%),
            radial-gradient(circle at 90% 5%, rgba(212,20,142,0.16) 0%, rgba(11,6,24,0) 35%),
            linear-gradient(165deg, {QS_BG_DEEP} 0%, {QS_BG_PURPLE} 55%, {QS_BG_DEEP} 100%);
        background-attachment: fixed;
    }}

    section[data-testid="stSidebarNav"] ul li:first-child a[aria-current="page"],
    div[data-testid="stSidebarNavItems"] li:first-child a[aria-current="page"] {{
        background-color: rgba(212, 20, 142, 0.16) !important;
        border-radius: 8px;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {QS_BG_PURPLE} 0%, #1B0F3A 60%, {QS_BG_DEEP} 100%);
        border-right: 1px solid {QS_GRID};
    }}
    [data-testid="stSidebar"] * {{
        color: {QS_TEXT_LIGHT};
    }}
    [data-testid="stSidebar"] h3 {{
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: {QS_TEXT_MUTED};
        margin-bottom: 0.4rem;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: {QS_GRID};
        margin: 1rem 0;
    }}
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: {QS_CARD} !important;
        border: 1px solid {QS_GRID} !important;
        border-radius: 10px !important;
        color: {QS_TEXT_LIGHT} !important;
    }}
    [data-testid="stSidebar"] button {{
        background: linear-gradient(90deg, {QS_PURPLE} 0%, {QS_MAGENTA} 100%) !important;
        border: 1px solid {QS_GRID} !important;
        color: {QS_TEXT_LIGHT} !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
    }}
    [data-testid="stSidebar"] button:hover {{
        background: linear-gradient(90deg, {QS_MAGENTA} 0%, {QS_PINK_BRIGHT} 100%) !important;
        border-color: {QS_PINK_SOFT} !important;
        box-shadow: 0 0 14px rgba(255, 115, 200, 0.28);
    }}
    .block-container {{
        padding-top: 3.2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }}
    h1, h2, h3, h4, p, span, label, div {{
        color: {QS_TEXT_LIGHT};
    }}
    .dashboard-header {{
        padding: 0.7rem 0 0.9rem 0;
        margin-top: 0;
        overflow: visible;
        border-bottom: 1px solid {QS_GRID};
        margin-bottom: 1.3rem;
    }}
    .dashboard-title {{
        font-size: 2.0rem;
        line-height: 1.35;
        font-weight: 800;
        letter-spacing: 0.01em;
        margin: 0;
        padding-top: 0.1rem;
        color: {QS_TEXT_LIGHT};
        text-shadow: 0 0 22px rgba(212, 20, 142, 0.22);
    }}
    .dashboard-subtitle {{
        font-size: 0.92rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        background: linear-gradient(90deg, {QS_PINK_BRIGHT} 0%, {QS_PURPLE} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.3rem 0 0.35rem 0;
        display: inline-block;
    }}
    .dashboard-desc {{
        font-size: 0.85rem;
        color: {QS_TEXT_MUTED};
        margin: 0;
    }}
    .kpi-card {{
        background: linear-gradient(160deg, {QS_CARD} 0%, #0F0A22 100%);
        border: 1px solid {QS_GRID};
        border-radius: 14px;
        padding: 1rem 1.1rem;
        text-align: left;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 10px rgba(0,0,0,0.45);
        height: 100%;
    }}
    .kpi-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {QS_PURPLE} 0%, {QS_MAGENTA} 45%, {QS_PINK} 75%, {QS_PINK_BRIGHT} 100%);
    }}
    .kpi-card:hover {{
        border-color: {QS_PINK};
        box-shadow: 0 6px 22px rgba(212, 20, 142, 0.24), 0 0 16px rgba(255, 115, 200, 0.14);
        transform: translateY(-2px);
    }}
    .kpi-icon {{
        font-size: 1.25rem;
        opacity: 0.9;
    }}
    .kpi-value {{
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        color: {QS_TEXT_LIGHT};
        margin: 0.25rem 0 0.15rem 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .kpi-label {{
        font-size: 0.72rem;
        font-weight: 600;
        color: {QS_TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .section-title {{
        font-size: 1.02rem;
        font-weight: 700;
        letter-spacing: 0.01em;
        color: {QS_TEXT_LIGHT};
        border-left: 3px solid {QS_PINK};
        padding-left: 0.65rem;
        margin: 1.7rem 0 0.7rem 0;
    }}
    .profile-card {{
        background-color: {QS_CARD};
        border: 1px solid {QS_GRID};
        border-radius: 12px;
        padding: 0.75rem 0.95rem;
        margin-bottom: 0.5rem;
    }}
    .profile-label {{
        font-size: 0.7rem;
        color: {QS_TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .profile-value {{
        font-size: 1.02rem;
        font-weight: 700;
        color: {QS_TEXT_LIGHT};
        margin-top: 0.15rem;
    }}
    .footer-text {{
        text-align: center;
        color: {QS_TEXT_MUTED};
        font-size: 0.78rem;
        letter-spacing: 0.02em;
        padding: 1.6rem 0 0.5rem 0;
        border-top: 1px solid {QS_GRID};
        margin-top: 2.2rem;
    }}
    [data-testid="stMetricValue"] {{
        color: {QS_TEXT_LIGHT};
    }}
    .stTextInput > div > div > input {{
        background-color: {QS_CARD} !important;
        color: {QS_TEXT_LIGHT} !important;
        border: 1px solid {QS_GRID} !important;
        border-radius: 10px !important;
    }}
    [data-baseweb="select"] > div {{
        background-color: {QS_CARD} !important;
        border: 1px solid {QS_GRID} !important;
        border-radius: 10px !important;
        color: {QS_TEXT_LIGHT} !important;
    }}
    [data-baseweb="popover"] li {{
        background-color: {QS_CARD} !important;
        color: {QS_TEXT_LIGHT} !important;
    }}
    [data-baseweb="popover"] li:hover {{
        background-color: rgba(212, 20, 142, 0.14) !important;
    }}
    [data-baseweb="tag"] {{
        background: linear-gradient(90deg, {QS_PURPLE} 0%, {QS_MAGENTA} 100%) !important;
    }}
    [data-testid="stExpander"] {{
        background-color: {QS_CARD};
        border: 1px solid {QS_GRID} !important;
        border-radius: 12px;
    }}
    .table-wrapper {{
        overflow-x: auto;
        border-radius: 12px;
        border: 1px solid {QS_GRID};
        margin-bottom: 1rem;
    }}
    table.military-data-table {{
        width: 100%;
        border-collapse: collapse;
        background-color: {QS_CARD};
        font-size: 0.85rem;
    }}
    table.military-data-table thead th {{
        background: linear-gradient(90deg, {QS_PURPLE} 0%, {QS_MAGENTA} 100%);
        color: {QS_TEXT_LIGHT};
        text-align: left;
        padding: 10px 14px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.04em;
        border-bottom: 1px solid {QS_GRID};
        position: sticky;
        top: 0;
    }}
    table.military-data-table tbody td {{
        padding: 8px 14px;
        color: {QS_TEXT_LIGHT};
        border-bottom: 1px solid {QS_GRID};
    }}
    table.military-data-table tbody tr:nth-child(even) {{
        background-color: rgba(255,255,255,0.02);
    }}
    table.military-data-table tbody tr:hover {{
        background-color: rgba(212, 20, 142, 0.10);
    }}
    .table-empty-message {{
        color: {QS_TEXT_MUTED};
        font-style: italic;
        padding: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR NAV LABEL FIX: "app" -> "Quick Stats" (display-only)
# ---------------------------------------------------------------------------
# Streamlit derives the sidebar label for this file from its filename
# ("app.py" -> "app") and that cannot be changed from Python without
# renaming the file itself, which is out of scope. This runs a small script
# inside a zero-size component iframe that reaches into the parent page DOM
# (same-origin, standard Streamlit component behavior) and swaps the visible
# text of the nav link that reads "app" to "Quick Stats". It re-runs on every
# DOM mutation via a MutationObserver so it keeps working across reruns/page
# switches, and it is wrapped in try/except so it can never break the app
# even if a future Streamlit version changes the sidebar nav markup.
components.html(
    """
    <script>
    (function () {
        function renameSidebarNavLabel() {
            try {
                const doc = window.parent.document;
                const navLinks = doc.querySelectorAll(
                    '[data-testid="stSidebarNav"] a, [data-testid="stSidebarNavItems"] a'
                );
                navLinks.forEach(function (link) {
                    const span = link.querySelector('span');
                    const target = span || link;
                    if (target && target.textContent.trim().toLowerCase() === 'app') {
                        target.textContent = 'Quick Stats';
                    }
                });
            } catch (e) {
                /* no-op: never break the app if the sidebar DOM shape changes */
            }
        }
        renameSidebarNavLabel();
        try {
            const doc = window.parent.document;
            const navRoot = doc.querySelector('[data-testid="stSidebarNav"]') || doc.body;
            const observer = new MutationObserver(renameSidebarNavLabel);
            observer.observe(navRoot, { childList: true, subtree: true });
        } catch (e) {
            /* no-op */
        }
    })();
    </script>
    """,
    height=0,
    width=0,
)


def render_html_table(df: pd.DataFrame, empty_message: str = "No data available.", max_height: str = None):
    """
    Renders a DataFrame as a styled HTML table via st.markdown, completely
    avoiding st.dataframe()/st.table() so no PyArrow dependency is ever
    triggered (PyArrow causes a Segmentation fault on this machine).

    max_height: optional CSS max-height (e.g. "460px"). When provided, the
    table wrapper becomes vertically scrollable (with the header sticky at
    the top) instead of expanding the page. Defaults to None, which keeps
    the original unbounded-height behavior -- so every existing call site
    that doesn't pass this argument renders exactly as before.
    """
    if df is None or df.empty:
        st.markdown(f'<div class="table-empty-message">{empty_message}</div>', unsafe_allow_html=True)
        return

    html_table = df.to_html(
        index=False,
        classes="military-data-table",
        border=0,
        escape=True,
        float_format=lambda x: f"{x:,.2f}",
    )
    wrapper_style = f' style="max-height:{max_height}; overflow-y:auto;"' if max_height else ""
    st.markdown(f'<div class="table-wrapper"{wrapper_style}>{html_table}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# QUICK STATS CHART THEME (post-processes figures returned by charts.py --
# does NOT modify charts.py, so every other page that imports it is
# completely unaffected).
# ---------------------------------------------------------------------------
_QS_COLORWAY = [
    QS_PINK_BRIGHT, QS_PURPLE, QS_MAGENTA, QS_PINK, QS_PINK_SOFT,
    "#7A3FD4", "#C13B92", "#B784F0",
]
_QS_SCALE = [[0.0, QS_PURPLE], [0.5, QS_MAGENTA], [1.0, QS_PINK_BRIGHT]]


def _hex_to_rgba(hex_color: str, alpha: float = 0.22) -> str:
    """Converts a '#RRGGBB' hex color into a valid Plotly rgba() string."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def _apply_qs_chart_theme(fig):
    """
    Re-colors a Plotly figure with the pink/magenta Quick Stats theme.
    Only cosmetic properties are touched (backgrounds, fonts, gridlines,
    trace colors/colorscales) -- the figure's underlying data, x/y values,
    and hover text are left completely untouched.
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, Arial", color=QS_TEXT_LIGHT, size=12),
        colorway=_QS_COLORWAY,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=QS_TEXT_LIGHT)),
        hoverlabel=dict(bgcolor=QS_CARD, font_size=12, font_family="Inter, Arial",
                         font_color=QS_TEXT_LIGHT, bordercolor=QS_GRID),
    )
    fig.update_xaxes(gridcolor=QS_GRID, zerolinecolor=QS_GRID, color=QS_TEXT_MUTED)
    fig.update_yaxes(gridcolor=QS_GRID, zerolinecolor=QS_GRID, color=QS_TEXT_MUTED)

    try:
        fig.update_geos(bgcolor="rgba(0,0,0,0)", showland=True,
                         landcolor=QS_BG_PURPLE, showocean=True, oceancolor=QS_BG_DEEP,
                         showlakes=False, showcountries=True, countrycolor=QS_GRID)
    except Exception:
        pass

    for i, trace in enumerate(fig.data):
        color = _QS_COLORWAY[i % len(_QS_COLORWAY)]
        ttype = getattr(trace, "type", "")
        try:
            if ttype in ("bar",):
                marker_color = trace.marker.color if trace.marker is not None else None
                if marker_color is None or isinstance(marker_color, str):
                    trace.marker.color = color
                    if trace.marker.line is not None:
                        trace.marker.line.color = "rgba(255,255,255,0.06)"
                else:
                    # Values-driven colorscale (e.g. a metric encoded as color) --
                    # keep the underlying values, just repaint the scale.
                    trace.marker.colorscale = _QS_SCALE

            elif ttype == "scatter":
                mode = trace.mode or ""
                if "lines" in mode:
                    trace.line.color = color
                if "markers" in mode and trace.marker is not None:
                    marker_color = trace.marker.color
                    if marker_color is None or isinstance(marker_color, str):
                        trace.marker.color = QS_PINK_SOFT
                    else:
                        trace.marker.colorscale = _QS_SCALE
                if getattr(trace, "fill", None) not in (None, "none"):
                    trace.fillcolor = _hex_to_rgba(color, 0.20)

            elif ttype == "scatterpolar":
                trace.line.color = color
                if getattr(trace, "fill", None) not in (None, "none"):
                    trace.fillcolor = _hex_to_rgba(color, 0.22)
                if trace.marker is not None:
                    trace.marker.color = QS_PINK_SOFT

            elif ttype == "pie":
                n = len(trace.labels) if trace.labels is not None else len(_QS_COLORWAY)
                trace.marker.colors = [_QS_COLORWAY[j % len(_QS_COLORWAY)] for j in range(n)]
                if trace.marker.line is not None:
                    trace.marker.line.color = QS_BG_DEEP

            elif ttype == "choropleth":
                trace.colorscale = _QS_SCALE
                trace.marker.line.color = QS_GRID

        except Exception:
            # Never let cosmetic re-theming break the underlying chart.
            pass

    return fig


# ---------------------------------------------------------------------------
# LOAD DATA (cached)
# ---------------------------------------------------------------------------
try:
    final_df, long_df = utils.load_data()
except FileNotFoundError:
    st.error(
        "Could not find the dataset files. Make sure both "
        "`data/military_final.xlsx` and `data/military_long.xlsx` exist "
        "inside the Module-5 project folder."
    )
    st.stop()
except Exception as e:
    st.error(f"Failed to load the dataset. Details: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📊 Dashboard")
    st.markdown("**Quick Stats Dashboard**")
    st.divider()

    st.markdown("### 🔎 Filters")

    # -----------------------------------------------------------------
    # RESET-SAFE WIDGET KEYS
    # -----------------------------------------------------------------
    # Every filter widget's key embeds a "reset token" counter. Clicking
    # "Reset Filters" simply increments this counter (see the button
    # handler below) instead of trying to delete/mutate existing widget
    # state. Because the key changes, Streamlit instantiates brand-new
    # multiselect widgets with no prior state at all -- this is the most
    # reliable way to guarantee a full, instant clear with no stale values
    # and no browser refresh, regardless of Streamlit version quirks
    # around delete-then-rerun timing.
    if "filter_reset_token" not in st.session_state:
        st.session_state.filter_reset_token = 0
    _rt = st.session_state.filter_reset_token
    KEY_COUNTRY = f"filter_country_{_rt}"
    KEY_REGION = f"filter_region_{_rt}"
    KEY_CONTINENT = f"filter_continent_{_rt}"
    KEY_ALLIANCE = f"filter_alliance_{_rt}"

    # -----------------------------------------------------------------
    # CASCADING / DEPENDENT FILTER OPTIONS
    # -----------------------------------------------------------------
    # Read whatever is CURRENTLY selected for each filter (from the
    # previous run) before creating any widget this run.
    _sel_country_now = st.session_state.get(KEY_COUNTRY, [])
    _sel_region_now = st.session_state.get(KEY_REGION, [])
    _sel_continent_now = st.session_state.get(KEY_CONTINENT, [])
    _sel_alliance_now = st.session_state.get(KEY_ALLIANCE, [])

    def _cross_filtered(exclude: str) -> pd.DataFrame:
        """
        Returns the subset of final_df matching every ACTIVE filter
        EXCEPT `exclude`. Used to compute the valid option list for
        `exclude`'s own dropdown, so each filter is always constrained by
        every other currently-selected filter (data-driven, no hard-coded
        country/region/continent relationships).
        """
        d = final_df
        if exclude != "country" and _sel_country_now:
            d = d[d["country"].isin(_sel_country_now)]
        if exclude != "region" and _sel_region_now:
            d = d[d["Region"].isin(_sel_region_now)]
        if exclude != "continent" and _sel_continent_now:
            d = d[d["Continent"].isin(_sel_continent_now)]
        if exclude != "alliance" and _sel_alliance_now:
            d = d[d["Alliance"].isin(_sel_alliance_now)]
        return d

    country_options = sorted(_cross_filtered("country")["country"].dropna().unique().tolist())
    region_options = sorted(_cross_filtered("region")["Region"].dropna().unique().tolist())
    continent_options = sorted(_cross_filtered("continent")["Continent"].dropna().unique().tolist())
    alliance_options = sorted(_cross_filtered("alliance")["Alliance"].dropna().unique().tolist())

    # Prune any now-invalid persisted selections BEFORE the widgets are
    # instantiated. This is required, not optional: Streamlit raises an
    # exception if a multiselect's stored value contains an item that is
    # not in the `options` list being passed to it this run (which would
    # otherwise happen the instant one filter narrows another's options).
    st.session_state[KEY_COUNTRY] = [v for v in _sel_country_now if v in country_options]
    st.session_state[KEY_REGION] = [v for v in _sel_region_now if v in region_options]
    st.session_state[KEY_CONTINENT] = [v for v in _sel_continent_now if v in continent_options]
    st.session_state[KEY_ALLIANCE] = [v for v in _sel_alliance_now if v in alliance_options]

    selected_countries = st.multiselect("Country", options=country_options, key=KEY_COUNTRY)
    selected_regions = st.multiselect("Region", options=region_options, key=KEY_REGION)
    selected_continents = st.multiselect("Continent", options=continent_options, key=KEY_CONTINENT)
    selected_alliances = st.multiselect("Alliance", options=alliance_options, key=KEY_ALLIANCE)

    if st.button("🔄 Reset Filters", use_container_width=True):
        st.session_state.filter_reset_token += 1
        st.rerun()

    st.divider()
    st.markdown("### ℹ️ About Dashboard")
    st.caption(
        "The Quick Stats Dashboard provides a concise overview of global "
        "military capabilities across countries. It highlights key indicators "
        "such as Military Power Index, Defense Budget, Military Manpower, "
        "Military Aircraft, Tanks, and Naval Fleet strength. Use the filters "
        "to explore countries by region, continent, and alliance and quickly "
        "identify major differences in military capability."
    )

# ---------------------------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------------------------
filtered_df = utils.apply_filters(
    final_df,
    countries=selected_countries,
    regions=selected_regions,
    continents=selected_continents,
    alliances=selected_alliances,
)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="dashboard-header">
    <p class="dashboard-title">🌍 UNIFIED MILITARY ANALYTICS</p>
    <p class="dashboard-subtitle">Quick Stats Dashboard</p>
    <p class="dashboard-desc">Global military capability, defense spending, manpower and strategic assets at a glance.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# ZERO-RESULT GUARD
# ---------------------------------------------------------------------------
if filtered_df.empty:
    st.warning("No countries match the selected filters. Try adjusting or resetting your filters from the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------------------------
kpis = utils.compute_kpis(filtered_df)


def kpi_card(col, icon, label, value):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)


row1 = st.columns(4)
kpi_card(row1[0], "🌍", "Total Countries", kpis["total_countries"])
kpi_card(row1[1], "⚡", "Avg Power Index", kpis["avg_power_index"])
kpi_card(row1[2], "💰", "Total Defense Budget", kpis["total_budget"])
kpi_card(row1[3], "✈️", "Total Military Aircraft", kpis["total_aircraft"])

row2 = st.columns(4)
kpi_card(row2[0], "🪖", "Total Tanks", kpis["total_tanks"])
kpi_card(row2[1], "⚓", "Total Naval Fleet", kpis["total_naval"])
kpi_card(row2[2], "👥", "Total Military Manpower", kpis["total_manpower"])
kpi_card(row2[3], "🏆", "Best Ranked Country", kpis["best_country"])

# ---------------------------------------------------------------------------
# CHART GRID
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Power & Budget Overview</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(_apply_qs_chart_theme(charts.top_power_index_chart(filtered_df)), use_container_width=True)
with c2:
    st.plotly_chart(_apply_qs_chart_theme(charts.top_defense_budget_chart(filtered_df)), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(_apply_qs_chart_theme(charts.top_military_assets_chart(filtered_df)), use_container_width=True)
with c4:
    st.plotly_chart(_apply_qs_chart_theme(charts.top_ppp_chart(filtered_df)), use_container_width=True)

st.markdown('<div class="section-title">Military Rank by Country</div>', unsafe_allow_html=True)
map_fig, map_rendered_as_choropleth = charts.military_rank_map(filtered_df)
st.plotly_chart(_apply_qs_chart_theme(map_fig), use_container_width=True)
if not map_rendered_as_choropleth:
    st.caption("Showing a ranked bar chart fallback -- some country names could not be matched to the map.")

st.markdown('<div class="section-title">Asset Breakdown</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)
with c5:
    st.plotly_chart(_apply_qs_chart_theme(charts.top_aircraft_chart(filtered_df)), use_container_width=True)
with c6:
    st.plotly_chart(_apply_qs_chart_theme(charts.top_tanks_chart(filtered_df)), use_container_width=True)

c7, c8 = st.columns(2)
with c7:
    st.plotly_chart(_apply_qs_chart_theme(charts.top_naval_chart(filtered_df)), use_container_width=True)
with c8:
    st.plotly_chart(_apply_qs_chart_theme(charts.defense_budget_bubble_chart(filtered_df)), use_container_width=True)

st.markdown('<div class="section-title">Distribution</div>', unsafe_allow_html=True)
c9, c10 = st.columns(2)
with c9:
    st.plotly_chart(_apply_qs_chart_theme(charts.continent_distribution_chart(filtered_df)), use_container_width=True)
with c10:
    st.plotly_chart(_apply_qs_chart_theme(charts.alliance_distribution_chart(filtered_df)), use_container_width=True)

st.markdown('<div class="section-title">Military Capability Comparison</div>', unsafe_allow_html=True)
st.plotly_chart(_apply_qs_chart_theme(charts.military_capability_comparison_chart(filtered_df)), use_container_width=True)

# ---------------------------------------------------------------------------
# COUNTRY SEARCH
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🔍 Country Search</div>', unsafe_allow_html=True)

available_countries = sorted(filtered_df["country"].unique().tolist())
search_country = st.selectbox("Select a country to view full statistics", options=available_countries, key="country_search")

if search_country:
    profile = utils.get_country_profile(final_df, search_country)
    if profile:
        profile_items = list(profile.items())
        cols = st.columns(4)
        for i, (label, value) in enumerate(profile_items):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-label">{label}</div>
                    <div class="profile-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        with st.expander(f"📄 View all raw metrics for {search_country} (from military_long.xlsx)"):
            long_metrics = utils.get_country_long_metrics(long_df, search_country)
            render_html_table(
                long_metrics,
                empty_message=f"No military metrics available for {search_country}.",
            )
    else:
        st.info("No profile data found for this country.")

# ---------------------------------------------------------------------------
# INTERACTIVE DATA TABLE
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Country Military Overview</div>', unsafe_allow_html=True)

table_search = st.text_input("Search countries in the table below", placeholder="Type a country name...")
table_df = filtered_df.copy()
if table_search:
    table_df = table_df[table_df["country"].str.contains(table_search, case=False, na=False)]

display_columns = [
    "country", "Continent", "Region", "Alliance", "power_index_rank", "power_index_score",
    "defense_budget_usd", "total_military_aircraft", "tanks", "total_naval_fleet",
    "total_military_manpower", "GDP",
]
display_columns = [c for c in display_columns if c in table_df.columns]

render_html_table(
    table_df[display_columns].sort_values("power_index_rank"),
    empty_message="No military metrics available for the selected filters.",
    max_height="460px",
)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="footer-text">
    Developed for Infosys Virtual Internship &nbsp;|&nbsp; Unified Military Analytics and Comparison Dashboard
</div>
""", unsafe_allow_html=True)