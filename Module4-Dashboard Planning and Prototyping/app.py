import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Unified Military Analytics Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    css_file = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "style.css"
    )

    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_excel("military_final.xlsx")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df

df = load_data()

# ============================================================
# COLORS
# ============================================================

PRIMARY = "#42A5F5"
SECONDARY = "#1565C0"
CARD = "#0C2340"
BACKGROUND = "#061528"
TEXT = "white"

# ============================================================
# PLOTLY THEME
# ============================================================

plot_template = dict(

    paper_bgcolor=CARD,

    plot_bgcolor=CARD,

    font=dict(
        color="white",
        family="Segoe UI"
    ),

    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    )
)

# ============================================================
# HEADER
# ============================================================

# ============================================================
# PREMIUM HEADER
# ============================================================

st.markdown("""
<div style="
background: linear-gradient(135deg,#071A2F,#0B2E4F);
padding:30px;
border-radius:18px;
border:1px solid rgba(92,200,255,.15);
box-shadow:0 10px 25px rgba(0,0,0,.35);
margin-bottom:25px;
">

<div style="display:flex;align-items:center;">

<div style="
font-size:65px;
margin-right:22px;
">
🛡️
</div>

<div>

<h1 style="
margin:0;
color:white;
font-size:44px;
font-weight:700;
letter-spacing:.5px;">
Unified Military Analytics
</h1>

<div style="
margin-top:6px;
font-size:22px;
color:#4FC3F7;
font-weight:600;">
Global Defense Intelligence Dashboard
</div>

<div style="
margin-top:10px;
color:#BFD7EA;
font-size:15px;">
Real-time comparison of military strength, defense spending,
air power, land forces, naval assets and strategic capabilities across nations.
</div>

</div>

</div>

</div>
""", unsafe_allow_html=True)

st.markdown("---")
# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <h2 style="color:white;margin-bottom:0px;">
    🎯 Dashboard Filters
    </h2>

    <p style="
    color:#5CC8FF;
    margin-top:-5px;
    font-size:14px;
    ">
    Filter and Explore Military Data
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # =====================================================

    search = st.text_input(
        "🔍 Search Country",
        placeholder="Type country..."
    )

    countries = sorted(df["country"].dropna().unique())

    if search:

        countries = [

            c for c in countries

            if search.lower() in c.lower()

        ]

    selected_country = st.multiselect(

        "🌍 Country",

        countries,

        default=countries

    )

    filtered_df = df[
        df["country"].isin(selected_country)
    ]

    continent = sorted(

        filtered_df["continent"].dropna().unique()

    )

    selected_continent = st.multiselect(

        "🌎 Continent",

        continent,

        default=continent

    )

    filtered_df = filtered_df[
        filtered_df["continent"].isin(
            selected_continent
        )
    ]

    region = sorted(

        filtered_df["region"].dropna().unique()

    )

    selected_region = st.multiselect(

        "📍 Region",

        region,

        default=region

    )

    filtered_df = filtered_df[
        filtered_df["region"].isin(
            selected_region
        )
    ]

    st.markdown("### ⭐ Power Index")

    power = st.slider(

        "",

        float(filtered_df["power_index"].min()),

        float(filtered_df["power_index"].max()),

        (

            float(filtered_df["power_index"].min()),

            float(filtered_df["power_index"].max())

        ),

        key="power"

    )

    filtered_df = filtered_df[
        filtered_df["power_index"].between(
            power[0],
            power[1]
        )
    ]

    st.markdown("### 👥 Population")

    population = st.slider(

        "",

        int(filtered_df["total_population"].min()),

        int(filtered_df["total_population"].max()),

        (

            int(filtered_df["total_population"].min()),

            int(filtered_df["total_population"].max())

        ),

        key="population"

    )

    filtered_df = filtered_df[
        filtered_df["total_population"].between(
            population[0],
            population[1]
        )
    ]

    st.markdown("### ✈ Military Aircraft")

    aircraft = st.slider(

        "",

        int(filtered_df["total_military_aircraft"].min()),

        int(filtered_df["total_military_aircraft"].max()),

        (

            int(filtered_df["total_military_aircraft"].min()),

            int(filtered_df["total_military_aircraft"].max())

        ),

        key="aircraft"

    )

    filtered_df = filtered_df[
        filtered_df["total_military_aircraft"].between(
            aircraft[0],
            aircraft[1]
        )
    ]

    st.markdown("### 🛡 Tanks")

    tanks = st.slider(

        "",

        int(filtered_df["tanks"].min()),

        int(filtered_df["tanks"].max()),

        (

            int(filtered_df["tanks"].min()),

            int(filtered_df["tanks"].max())

        ),

        key="tanks"

    )

    filtered_df = filtered_df[
        filtered_df["tanks"].between(
            tanks[0],
            tanks[1]
        )
    ]

    st.markdown("### 🚢 Naval Fleet")

    naval = st.slider(

        "",

        int(filtered_df["total_naval_fleet"].min()),

        int(filtered_df["total_naval_fleet"].max()),

        (

            int(filtered_df["total_naval_fleet"].min()),

            int(filtered_df["total_naval_fleet"].max())

        ),

        key="naval"

    )

    filtered_df = filtered_df[
        filtered_df["total_naval_fleet"].between(
            naval[0],
            naval[1]
        )
    ]

    st.markdown("### 💰 Defense Budget")

    budget = st.slider(

        "",

        float(filtered_df["defense_budget_usd"].min()),

        float(filtered_df["defense_budget_usd"].max()),

        (

            float(filtered_df["defense_budget_usd"].min()),

            float(filtered_df["defense_budget_usd"].max())

        ),

        key="budget"

    )

    filtered_df = filtered_df[
        filtered_df["defense_budget_usd"].between(
            budget[0],
            budget[1]
        )
    ]

    top_n = st.selectbox(

        "🏆 Top Countries",

        [5,10,15,20,25],

        index=1

    )

    st.markdown("---")

    st.metric("Countries", len(filtered_df))

    st.metric(
        "Continents",
        filtered_df["continent"].nunique()
    )

    st.metric(
        "Regions",
        filtered_df["region"].nunique()
    )

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_countries = filtered_df["country"].nunique()

total_population = filtered_df["total_population"].sum()

total_aircraft = filtered_df["total_military_aircraft"].sum()

total_tanks = filtered_df["tanks"].sum()

total_naval = filtered_df["total_naval_fleet"].sum()

total_active = filtered_df["active_personnel"].sum()

# ============================================================
# TITLE
# ============================================================

st.markdown("""

<h1 style="
text-align:center;
color:white;
font-size:42px;
margin-bottom:0px;">

🛡 Unified Military Analytics Dashboard

</h1>

<p style="
text-align:center;
color:#5CC8FF;
font-size:18px;
margin-top:-10px;">

Global Military Intelligence & Comparison Platform

</p>

""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4, c5, c6 = st.columns(6)

cards = [
    ("🌍", "Countries", f"{total_countries}"),
    ("👥", "Population", f"{total_population:,.0f}"),
    ("✈", "Aircraft", f"{total_aircraft:,.0f}"),
    ("🛡", "Tanks", f"{total_tanks:,.0f}"),
    ("🚢", "Naval Fleet", f"{total_naval:,.0f}"),
    ("👨‍✈️", "Personnel", f"{total_active:,.0f}")
]

for col, (icon, title, value) in zip([c1, c2, c3, c4, c5, c6], cards):
    with col:
        st.markdown(
            f"""
<div class="metric-card">
    <div style="font-size:32px;margin-bottom:8px;">{icon}</div>
    <div class="metric-title">{title}</div>
    <div class="metric-value">{value}</div>
</div>
""",
            unsafe_allow_html=True
        )


# ============================================================
# ROW 1
# ============================================================

left_chart, right_chart = st.columns([2, 1])
with left_chart:

    st.markdown("""
    <div class="chart-title">
    ✈ Top Countries by Military Aircraft
    </div>
    """, unsafe_allow_html=True)

    aircraft_df = (
        filtered_df
        .sort_values(
            "total_military_aircraft",
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(

        aircraft_df,

        x="country",

        y="total_military_aircraft",

        color="total_military_aircraft",

        color_continuous_scale="Blues",

        text="total_military_aircraft"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(

        template="plotly_dark",

        height=430,

        xaxis_title="Country",

        yaxis_title="Aircraft",

        coloraxis_showscale=False,

        paper_bgcolor=CARD,

        plot_bgcolor=CARD,

        font=dict(color="white")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right_chart:

    st.markdown("""
    <div class="chart-title">
    🌍 Countries by Continent
    </div>
    """, unsafe_allow_html=True)

    continent_df = (

        filtered_df

        .groupby("continent")

        .size()

        .reset_index(name="Count")

    )

    fig = px.pie(

        continent_df,

        names="continent",

        values="Count",

        hole=0.65,

        color_discrete_sequence=px.colors.sequential.Blues_r

    )

    fig.update_layout(

        template="plotly_dark",

        height=430,

        paper_bgcolor=CARD,

        plot_bgcolor=CARD,

        font=dict(color="white"),

        showlegend=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ============================================================
# ROW 2
# ============================================================

left_chart2, right_chart2 = st.columns(2)

with left_chart2:

    st.markdown("""
    <div class="chart-title">
    💰 Defense Budget vs GDP
    </div>
    """, unsafe_allow_html=True)

    scatter_df = filtered_df.dropna(
        subset=["gdp", "defense_budget_usd"]
    )

    fig = px.scatter(

        scatter_df,

        x="gdp",

        y="defense_budget_usd",

        size="active_personnel",

        color="continent",

        hover_name="country",

        size_max=35

    )

    fig.update_layout(

        template="plotly_dark",

        height=430,

        paper_bgcolor=CARD,

        plot_bgcolor=CARD,

        font=dict(color="white"),

        xaxis_title="GDP (USD)",

        yaxis_title="Defense Budget (USD)"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
with right_chart2:

    st.markdown("""
    <div class="chart-title">
    🌳 Military Aircraft by Continent
    </div>
    """, unsafe_allow_html=True)

    tree_df = filtered_df.copy()

    fig = px.treemap(

        tree_df,

        path=["continent", "country"],

        values="total_military_aircraft",

        color="total_military_aircraft",

        color_continuous_scale="Blues"

    )

    fig.update_layout(

        template="plotly_dark",

        height=430,

        paper_bgcolor=CARD,

        plot_bgcolor=CARD,

        font=dict(color="white"),

        margin=dict(
            l=5,
            r=5,
            t=35,
            b=5
        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# ROW 3
# ============================================================

left_chart3, right_chart3 = st.columns([2, 1])

with left_chart3:

    st.markdown("""
    <div class="chart-title">
    🌍 Global Power Index Map
    </div>
    """, unsafe_allow_html=True)

    map_df = filtered_df.copy()

    fig = px.choropleth(

        map_df,

        locations="country",

        locationmode="country names",

        color="power_index",

        hover_name="country",

        color_continuous_scale="Blues_r",

        projection="natural earth"

    )

    fig.update_layout(

        template="plotly_dark",

        height=500,

        paper_bgcolor=CARD,

        plot_bgcolor=CARD,

        font=dict(color="white"),

        margin=dict(
            l=0,
            r=0,
            t=35,
            b=0
        ),

        coloraxis_colorbar=dict(
            title="Power Index"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right_chart3:

    st.markdown("""
    <div class="chart-title">
    🕸 Military Capability Radar
    </div>
    """, unsafe_allow_html=True)

    radar_df = (
        filtered_df
        .sort_values("power_index")
        .head(1)
    )

    country = radar_df.iloc[0]

    categories = [

        "Aircraft",

        "Tanks",

        "Naval Fleet",

        "Personnel"

    ]

    values = [

        country["total_military_aircraft"],

        country["tanks"],

        country["total_naval_fleet"],

        country["active_personnel"]

    ]

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=values,

            theta=categories,

            fill="toself",

            name=country["country"],

            line=dict(
                color="#42A5F5",
                width=3
            )

        )

    )

    fig.update_layout(

        template="plotly_dark",

        polar=dict(

            bgcolor=CARD,

            radialaxis=dict(

                visible=True,

                gridcolor="gray"

            )

        ),

        paper_bgcolor=CARD,

        height=500,

        font=dict(color="white"),

        showlegend=False

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# ROW 4
# ============================================================

left_chart4, right_chart4 = st.columns(2)

with left_chart4:

    st.markdown("""
    <div class="chart-title">
    🔥 Military Data Correlation
    </div>
    """, unsafe_allow_html=True)

    cols = [

        "power_index",
        "total_population",
        "active_personnel",
        "total_military_aircraft",
        "tanks",
        "total_naval_fleet",
        "defense_budget_usd",
        "gdp"

    ]

    corr = filtered_df[cols].corr(numeric_only=True)

    fig = px.imshow(

        corr,

        text_auto=".2f",

        color_continuous_scale="Blues",

        aspect="auto"

    )

    fig.update_layout(

        template="plotly_dark",

        height=500,

        paper_bgcolor=CARD,

        plot_bgcolor=CARD,

        font=dict(color="white")

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right_chart4:

    st.markdown("""
    <div class="chart-title">
    📊 Continent Military Assets
    </div>
    """, unsafe_allow_html=True)

    continent_summary = (

        filtered_df

        .groupby("continent")[
            [
                "total_military_aircraft",
                "tanks",
                "total_naval_fleet"
            ]
        ]

        .sum()

        .reset_index()

    )

    fig = go.Figure()

    fig.add_bar(

        x=continent_summary["continent"],

        y=continent_summary["total_military_aircraft"],

        name="Aircraft"

    )

    fig.add_bar(

        x=continent_summary["continent"],

        y=continent_summary["tanks"],

        name="Tanks"

    )

    fig.add_bar(

        x=continent_summary["continent"],

        y=continent_summary["total_naval_fleet"],

        name="Naval Fleet"

    )

    fig.update_layout(

        barmode="stack",

        template="plotly_dark",

        height=500,

        paper_bgcolor=CARD,

        plot_bgcolor=CARD,

        font=dict(color="white"),

        xaxis_title="Continent",

        yaxis_title="Military Assets"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# ROW 5
# ============================================================

st.markdown("---")

st.markdown("""
<div class="chart-title">
📋 Military Dataset
</div>
""", unsafe_allow_html=True)

display_columns = [
    "country",
    "continent",
    "region",
    "power_index",
    "total_population",
    "active_personnel",
    "total_military_aircraft",
    "tanks",
    "total_naval_fleet",
    "defense_budget_usd",
    "gdp"
]

available_columns = [
    col for col in display_columns
    if col in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns],
    use_container_width=True,
    height=450
)


st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="chart-title">
📊 Dataset Summary
</div>
""", unsafe_allow_html=True)

st.dataframe(
    filtered_df.describe(),
    use_container_width=True
)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="📥 Download Filtered Dataset",

    data=csv,

    file_name="filtered_military_data.csv",

    mime="text/csv"

)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""

<hr>

<div style="text-align:center;">

<h4 style="color:#5CC8FF;">
🛡 Unified Military Analytics Dashboard
</h4>

<p style="color:white;">

Built using Streamlit • Plotly • Python

</p>

<p style="color:gray;">

Developed by Nagashree K S

</p>

</div>

""", unsafe_allow_html=True)



