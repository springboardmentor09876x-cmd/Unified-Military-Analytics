"""
charts.py
---------
Unified Military Analytics and Comparison Dashboard
Module 5 - Dashboard Development (Quick Stats)

Responsibilities of this file ONLY:
    - Every Plotly chart-building function used by app.py

Every function:
    - Takes an already-filtered dataframe (plus any extra params it needs)
    - Returns a Plotly Figure, OR None if there isn't enough data to plot
    - Never raises -- app.py checks for None and shows a clean message instead
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# THEME CONSTANTS (Military Intelligence / Executive Command Center palette)
# Restrained navy/charcoal with a single muted teal accent -- no rainbow of
# bright colors. Constant NAMES are kept unchanged (RED, GOLD, etc.) because
# app.py and every page under pages/ import them directly; only the VALUES
# changed, so nothing else needs to be touched.
# ---------------------------------------------------------------------------
BG_COLOR = "#0B0F17"
CARD_COLOR = "#141A24"
RED = "#3EC6B8"          # primary accent (muted teal)
DARK_RED = "#2E8B84"     # darker teal variant, for emphasis/hover states
GOLD = "#6B7A90"         # secondary neutral (muted slate-blue)
TEXT_LIGHT = "#E8ECF1"
TEXT_MUTED = "#8A94A6"
GRID_COLOR = "#232A35"

# Power Index world-map gradient (pink/magenta) -- used ONLY by
# military_rank_map() below via CONTINUOUS_RED_SCALE[::-1]. This is the sole
# consumer of this constant, so changing its values only affects the map
# and its Power Index colorbar/legend (which share the same Plotly
# coloraxis and therefore always match each other automatically). Ordered
# darkest -> lightest, exactly like the previous teal scale it replaces, so
# the existing "which end of the scale is which value" mapping is preserved.
CONTINUOUS_RED_SCALE = ["#3A0A3F", "#64105F", "#9E176F", "#D52B91", "#F044A8", "#FF7AC8"]
CATEGORY_PALETTE = [RED, "#5B7A99", "#6B7A90", "#7FA8A0", "#4C6B8A", "#2E8B84", "#8A94A6", "#B7C4D1"]

# Renames applied ONLY for the choropleth map trace, to match the country
# names Plotly's built-in "country names" location mode expects. This does
# NOT change the underlying dataset -- it's a display-only lookup.
MAP_NAME_OVERRIDES = {
    "Turkiye": "Turkey",
    "Democratic Republic of the Congo": "Democratic Republic of the Congo",
    "Republic of the Congo": "Republic of Congo",
    "Micronesia": "Federated States of Micronesia",
    "Cape Verde": "Cabo Verde",
    "Laos": "Laos",
    "Brunei": "Brunei Darussalam",
    "Czechia": "Czech Republic",
    "Ivory Coast": "Ivory Coast",
    "North Macedonia": "North Macedonia",
    "Eswatini": "Eswatini",
}


def _empty_layout(fig: go.Figure) -> go.Figure:
    """Applies the shared executive-dashboard theme layout to any figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        font=dict(family="Inter, Segoe UI, Arial", color=TEXT_LIGHT, size=12),
        title_font=dict(family="Inter, Segoe UI, Arial", size=14, color=TEXT_LIGHT),
        margin=dict(l=16, r=16, t=48, b=16),
        height=380,
        bargap=0.28,
        hoverlabel=dict(bgcolor="#1C2430", bordercolor=GRID_COLOR, font_size=12, font_family="Inter, Arial", font_color=TEXT_LIGHT),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, showline=False, tickfont=dict(size=11, color=TEXT_MUTED))
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, showline=False, tickfont=dict(size=11, color=TEXT_MUTED))
    return fig


def _no_data_figure(message="No data available for this selection.") -> go.Figure:
    """A clean placeholder figure shown instead of crashing when there's no data."""
    fig = go.Figure()
    fig.add_annotation(
        text=message, showarrow=False, font=dict(size=14, color=TEXT_MUTED),
        xref="paper", yref="paper", x=0.5, y=0.5,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _empty_layout(fig)


def _top_n_horizontal_bar(df, value_col, label, title, n=10, currency=False, color=RED, ascending_is_stronger=False):
    """
    Shared builder for every 'Top N Countries by <metric>' horizontal bar chart.
    ascending_is_stronger=True means SMALLER values rank higher (used for
    power_index_score, where a lower score = a stronger military).
    """
    if df.empty or value_col not in df.columns or df[value_col].dropna().empty:
        return _no_data_figure()

    working = df[["country", value_col]].dropna().copy()
    working = working.sort_values(value_col, ascending=ascending_is_stronger).head(n)
    working = working.sort_values(value_col, ascending=not ascending_is_stronger)

    text_fmt = [f"${v:,.0f}" if currency and v >= 1000 else f"{v:,.2f}" if isinstance(v, float) and not currency else f"{v:,.0f}"
                for v in working[value_col]]

    fig = go.Figure(go.Bar(
        x=working[value_col],
        y=working["country"],
        orientation="h",
        marker=dict(color=color, line=dict(width=0)),
        text=text_fmt,
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>" + label + ": %{text}<extra></extra>",
    ))
    fig.update_layout(title=dict(text=title, font=dict(size=15, color=TEXT_LIGHT)))
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None, autorange="reversed" if not ascending_is_stronger else None)
    return _empty_layout(fig)


# ---------------------------------------------------------------------------
# SECTION 1: Top 10 Countries by Military Power (Power Index)
# ---------------------------------------------------------------------------
def top_power_index_chart(df, n=10):
    # Lower power_index_score = stronger military -- ranking direction handled explicitly.
    return _top_n_horizontal_bar(
        df, "power_index_score", "Power Index Score",
        "Top 10 Countries by Power Index (Lower Score = Stronger)",
        n=n, color=RED, ascending_is_stronger=True,
    )


# ---------------------------------------------------------------------------
# SECTION 2: Top Countries by Defense Budget
# ---------------------------------------------------------------------------
def top_defense_budget_chart(df, n=10):
    if df.empty or "defense_budget_usd" not in df.columns or df["defense_budget_usd"].dropna().empty:
        return _no_data_figure()
    working = df[["country", "defense_budget_usd"]].dropna().sort_values("defense_budget_usd", ascending=False).head(n)
    working = working.sort_values("defense_budget_usd", ascending=True)

    fig = go.Figure(go.Bar(
        x=working["defense_budget_usd"],
        y=working["country"],
        orientation="h",
        marker=dict(color=GOLD),
        hovertemplate="<b>%{y}</b><br>Defense Budget: $%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(title=dict(text="Top 10 Countries by Defense Budget", font=dict(size=15, color=TEXT_LIGHT)))
    fig.update_xaxes(tickprefix="$", tickformat=".2s")
    return _empty_layout(fig)


# ---------------------------------------------------------------------------
# SECTION 3: Top Countries by Military Assets
# ---------------------------------------------------------------------------
def top_military_assets_chart(df, n=10):
    """
    Combining aircraft + tanks + naval fleet counts is misleading (different
    unit meaning per asset type), so this uses total_military_aircraft alone
    as the clearest single, meaningful "military assets" comparison metric.
    """
    return _top_n_horizontal_bar(
        df, "total_military_aircraft", "Total Military Aircraft",
        "Top 10 Countries by Military Aircraft (Assets Measure)",
        n=n, color="#5B7A99",
    )


# ---------------------------------------------------------------------------
# SECTION 4: Military Rank by Country -- World Map (with safe fallback)
# ---------------------------------------------------------------------------
def military_rank_map(df):
    if df.empty or "power_index_score" not in df.columns:
        return _no_data_figure(), False

    try:
        working = df[["country", "power_index_score", "power_index_rank"]].dropna().copy()
        if working.empty:
            return _no_data_figure(), False

        working["map_name"] = working["country"].replace(MAP_NAME_OVERRIDES)

        fig = px.choropleth(
            working,
            locations="map_name",
            locationmode="country names",
            color="power_index_score",
            hover_name="country",
            hover_data={"power_index_rank": True, "power_index_score": ":.4f", "map_name": False},
            color_continuous_scale=CONTINUOUS_RED_SCALE[::-1],
            title="Military Rank by Country (Darker = Stronger Power Index)",
        )
        fig.update_geos(
            bgcolor=CARD_COLOR, showframe=False, showcoastlines=True,
            coastlinecolor=GRID_COLOR, landcolor="#1B222D", oceancolor=BG_COLOR,
            showocean=True,
        )
        fig.update_layout(
            template="plotly_dark", paper_bgcolor=CARD_COLOR,
            font=dict(family="Inter, Arial", color=TEXT_LIGHT, size=12),
            margin=dict(l=16, r=16, t=48, b=16), height=420,
            title=dict(font=dict(size=14, color=TEXT_LIGHT)),
            coloraxis_colorbar=dict(title="Power<br>Index", tickfont=dict(color=TEXT_MUTED)),
        )
        return fig, True
    except Exception:
        # Graceful fallback: never let a map failure crash the dashboard.
        fallback_fig = top_power_index_chart(df)
        return fallback_fig, False


# ---------------------------------------------------------------------------
# SECTION 5: Top 10 Countries by Purchasing Power Parity
# ---------------------------------------------------------------------------
def top_ppp_chart(df, n=10):
    return _top_n_horizontal_bar(
        df, "purchasing_power_parity_usd", "Purchasing Power Parity",
        "Top 10 Countries by Purchasing Power Parity", n=n, currency=True, color=GOLD,
    )


# ---------------------------------------------------------------------------
# SECTION 6-8: Aircraft / Tanks / Naval Fleet
# ---------------------------------------------------------------------------
def top_aircraft_chart(df, n=10):
    return _top_n_horizontal_bar(df, "total_military_aircraft", "Total Aircraft", "Top 10 Countries by Military Aircraft", n=n, color="#5B7A99")


def top_tanks_chart(df, n=10):
    return _top_n_horizontal_bar(df, "tanks", "Total Tanks", "Top 10 Countries by Tank Strength", n=n, color="#4C6B8A")


def top_naval_chart(df, n=10):
    return _top_n_horizontal_bar(df, "total_naval_fleet", "Naval Fleet Size", "Top 10 Countries by Naval Fleet", n=n, color="#4FA88A")


# ---------------------------------------------------------------------------
# SECTION 9: Defense Budget Bubble Chart
# ---------------------------------------------------------------------------
def defense_budget_bubble_chart(df):
    required = ["defense_budget_usd", "power_index_score", "total_military_aircraft", "country"]
    if df.empty or any(c not in df.columns for c in required):
        return _no_data_figure()

    working = df.dropna(subset=required).copy()
    if working.empty:
        return _no_data_figure()

    color_col = "Continent" if "Continent" in working.columns else None

    fig = px.scatter(
        working,
        x="defense_budget_usd",
        y="power_index_score",
        size="total_military_aircraft",
        color=color_col,
        hover_name="country",
        size_max=45,
        color_discrete_sequence=CATEGORY_PALETTE,
        custom_data=["country", "defense_budget_usd", "power_index_score", "total_military_aircraft", "tanks", "total_naval_fleet"]
        if all(c in working.columns for c in ["tanks", "total_naval_fleet"]) else None,
    )
    fig.update_traces(
        marker=dict(line=dict(width=0.5, color=BG_COLOR), opacity=0.85),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Defense Budget: $%{customdata[1]:,.0f}<br>"
            "Power Index: %{customdata[2]:.4f}<br>"
            "Aircraft: %{customdata[3]:,.0f}<br>"
            "Tanks: %{customdata[4]:,.0f}<br>"
            "Naval Fleet: %{customdata[5]:,.0f}<extra></extra>"
        ) if working.shape[0] > 0 and "tanks" in working.columns else None,
    )
    fig.update_layout(title=dict(text="Defense Budget vs. Power Index (Bubble = Aircraft Count)", font=dict(size=15, color=TEXT_LIGHT)))
    fig.update_xaxes(title="Defense Budget (USD)", tickprefix="$", tickformat=".2s")
    fig.update_yaxes(title="Power Index Score (Lower = Stronger)")
    return _empty_layout(fig)


# ---------------------------------------------------------------------------
# SECTION 10 & 11: Continent / Alliance Distribution (Donut charts)
# ---------------------------------------------------------------------------
def continent_distribution_chart(df):
    if df.empty or "Continent" not in df.columns:
        return _no_data_figure()
    counts = df["Continent"].value_counts().reset_index()
    counts.columns = ["Continent", "Count"]

    fig = px.pie(
        counts, names="Continent", values="Count", hole=0.55,
        color_discrete_sequence=CATEGORY_PALETTE,
    )
    fig.update_traces(textinfo="percent+label", hovertemplate="<b>%{label}</b><br>Countries: %{value}<extra></extra>")
    fig.update_layout(title=dict(text="Countries by Continent", font=dict(size=15, color=TEXT_LIGHT)), showlegend=True)
    return _empty_layout(fig)


def alliance_distribution_chart(df):
    if df.empty or "Alliance" not in df.columns:
        return _no_data_figure()
    counts = df["Alliance"].value_counts().reset_index()
    counts.columns = ["Alliance", "Count"]

    fig = px.pie(
        counts, names="Alliance", values="Count", hole=0.55,
        color_discrete_sequence=[RED, TEXT_MUTED],
    )
    fig.update_traces(textinfo="percent+label", hovertemplate="<b>%{label}</b><br>Countries: %{value}<extra></extra>")
    fig.update_layout(title=dict(text="Countries by Alliance", font=dict(size=15, color=TEXT_LIGHT)), showlegend=True)
    return _empty_layout(fig)


# ---------------------------------------------------------------------------
# SECTION 12: Military Capability Comparison (small multiples, NOT one axis)
# ---------------------------------------------------------------------------
def military_capability_comparison_chart(df, n=8):
    """
    Aircraft, Tanks, Naval Fleet, and Manpower have wildly different scales
    (manpower is in the hundreds of thousands, naval fleet is in the tens/
    hundreds). Putting them on one shared axis would be misleading, so this
    uses faceted subplots (small multiples) -- one panel per metric, each
    with its own axis scale, for the top N countries by Power Index.
    """
    required = ["total_military_aircraft", "tanks", "total_naval_fleet", "total_military_manpower", "power_index_score"]
    if df.empty or any(c not in df.columns for c in required):
        return _no_data_figure()

    top_countries = df.dropna(subset=["power_index_score"]).sort_values("power_index_score", ascending=True).head(n)["country"]
    working = df[df["country"].isin(top_countries)].copy()
    if working.empty:
        return _no_data_figure()

    melted = working.melt(
        id_vars="country",
        value_vars=["total_military_aircraft", "tanks", "total_naval_fleet", "total_military_manpower"],
        var_name="Metric", value_name="Value",
    )
    label_map = {
        "total_military_aircraft": "Aircraft (units)",
        "tanks": "Tanks (units)",
        "total_naval_fleet": "Naval Fleet (units)",
        "total_military_manpower": "Manpower (personnel)",
    }
    melted["Metric"] = melted["Metric"].map(label_map)

    fig = px.bar(
        melted, x="Value", y="country", color="Metric", orientation="h",
        facet_col="Metric", facet_col_wrap=2,
        color_discrete_sequence=CATEGORY_PALETTE,
    )
    fig.update_xaxes(matches=None, showticklabels=True, tickformat=".2s")
    fig.update_yaxes(matches=None, title=None)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1], font=dict(color=TEXT_LIGHT, size=11)))
    fig.update_layout(
        title=dict(text="Military Capability Comparison (Top Countries -- Each Metric on Its Own Scale)", font=dict(size=15, color=TEXT_LIGHT)),
        showlegend=False, height=560,
    )
    return _empty_layout(fig)