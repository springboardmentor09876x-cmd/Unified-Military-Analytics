import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Unified Military Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_excel("military_final.xlsx")

df = load_data()

# ----------------------------------------------------
# DARK THEME CSS
# ----------------------------------------------------

st.markdown("""
<style>

html,body,[class*="css"]{
    background:#071B33;
    color:white;
    font-family:'Segoe UI';
}

.stApp{
    background:#071B33;
}

section[data-testid="stSidebar"]{
    background:#0B2447;
}

section[data-testid="stSidebar"] *{
    color:white;
}

.block-container{
    padding-top:1rem;
    padding-left:3rem;
    padding-right:3rem;
}



.hero{
    background:#14345D;
    border-radius:18px;
    padding:28px 40px;
    margin-bottom:25px;
    box-shadow:0 8px 20px rgba(0,0,0,.35);
}

.hero-title{
    color:#FFFFFF !important;
    font-size:52px !important;
    font-weight:800 !important;
    margin:0;
}

.hero-subtitle{
    color:#3FA9F5 !important;
    font-size:24px !important;
    font-weight:700;
    margin-top:15px;
    margin-bottom:25px;
}

.hero-text{
    color:#F8FAFC !important;
    font-size:18px !important;
    line-height:1.8;
    font-weight:400;
}

.metric-card{

background:#102D52;

padding:25px;

border-radius:18px;

text-align:center;

box-shadow:0 0 15px rgba(0,0,0,.20);

}

.metric-card:hover{

transform:translateY(-4px);

transition:.3s;

}

.metric-title{

font-size:22px;

font-weight:bold;

color:white;

}

.metric-value{

font-size:45px;

font-weight:700;

color:#58B4FF;

}
.metric-card{
    color:white !important;
}

.metric-card div{
    color:white !important;
}

.chart-card{

background:#102D52;

padding:20px;

border-radius:18px;

margin-bottom:20px;

box-shadow:0 0 15px rgba(0,0,0,.20);

}
/* ---------- Fix Streamlit Info/Success/Warning Cards ---------- */

div[data-testid="stAlert"]{
    background:#102D52 !important;
    border:1px solid #2E6FB3 !important;
    border-radius:15px !important;
}

div[data-testid="stAlert"] *{
    color:white !important;
    opacity:1 !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div,
div[data-testid="stAlert"] strong,
div[data-testid="stAlert"] h1,
div[data-testid="stAlert"] h2,
div[data-testid="stAlert"] h3,
div[data-testid="stAlert"] h4{
    color:white !important;
}

/* ---------- General Text ---------- */

h1,h2,h3,h4,h5,h6{
    color:white !important;
}

p{
    color:#E5E7EB !important;
}

label{
    color:white !important;
}

span{
    color:white !important;
}

.stMarkdown{
    color:white !important;
}

</style>

""",unsafe_allow_html=True)

# ----------------------------------------------------
# HERO SECTION
# ----------------------------------------------------

st.markdown("""
<div class="hero">

<div class="hero-title">
🛡️ Unified Military Analytics
</div>

<div class="hero-subtitle">
Global Defense Intelligence Dashboard
</div>

<div class="hero-text">
Real-time comparison of military strength, defense spending, air power,
land forces, naval assets and strategic capabilities across nations.
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("---")
# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown("# 🎯 Dashboard Filters")
st.sidebar.markdown("Filter and Explore Military Data")
st.sidebar.markdown("---")

# ---------------- Search Country ----------------

search = st.sidebar.text_input(
    "🔍 Search Country",
    placeholder="Type country..."
)

if search:
    df = df[df["country"].str.contains(search, case=False)]

# ---------------- Country Filter ----------------

countries = st.sidebar.multiselect(
    "🌍 Country",
    sorted(df["country"].unique()),
    default=[]
)

if countries:
    df = df[df["country"].isin(countries)]

# ---------------- Continent ----------------

if "continent" in df.columns:

    continents = st.sidebar.multiselect(
        "🌎 Continent",
        sorted(df["continent"].dropna().unique()),
        default=sorted(df["continent"].dropna().unique())
    )

    df = df[df["continent"].isin(continents)]

# ---------------- Region ----------------

if "region" in df.columns:

    regions = st.sidebar.multiselect(
        "📍 Region",
        sorted(df["region"].dropna().unique()),
        default=sorted(df["region"].dropna().unique())
    )

    df = df[df["region"].isin(regions)]

# ---------------- Alliance ----------------

if "alliance" in df.columns:

    alliances = st.sidebar.multiselect(
        "🤝 Alliance",
        sorted(df["alliance"].dropna().unique()),
        default=sorted(df["alliance"].dropna().unique())
    )

    df = df[df["alliance"].isin(alliances)]

# ---------------- Power Index ----------------

if "power_index" in df.columns:

    pmin = float(df["power_index"].min())
    pmax = float(df["power_index"].max())

    power = st.sidebar.slider(
        "⭐ Power Index",
        pmin,
        pmax,
        (pmin, pmax)
    )

    df = df[
        (df.power_index >= power[0]) &
        (df.power_index <= power[1])
    ]

# ---------------- Population ----------------

if "total_population" in df.columns:

    pop = st.sidebar.slider(
        "👥 Population",
        int(df.total_population.min()),
        int(df.total_population.max()),
        (
            int(df.total_population.min()),
            int(df.total_population.max())
        )
    )

    df = df[
        (df.total_population >= pop[0]) &
        (df.total_population <= pop[1])
    ]

# ---------------- Aircraft ----------------

if "total_military_aircraft" in df.columns:

    air = st.sidebar.slider(
        "✈️ Military Aircraft",
        int(df.total_military_aircraft.min()),
        int(df.total_military_aircraft.max()),
        (
            int(df.total_military_aircraft.min()),
            int(df.total_military_aircraft.max())
        )
    )

    df = df[
        (df.total_military_aircraft >= air[0]) &
        (df.total_military_aircraft <= air[1])
    ]

# ---------------- Tanks ----------------

if "tanks" in df.columns:

    tank = st.sidebar.slider(
        "🛡 Tanks",
        int(df.tanks.min()),
        int(df.tanks.max()),
        (
            int(df.tanks.min()),
            int(df.tanks.max())
        )
    )

    df = df[
        (df.tanks >= tank[0]) &
        (df.tanks <= tank[1])
    ]

st.sidebar.markdown("---")
st.sidebar.success(f"Countries Selected : {len(df)}")
# ==========================================================
# KPI SECTION
# ==========================================================

st.markdown("## 🛡 Unified Military Analytics Dashboard")
st.markdown("### Global Military Intelligence & Comparison Platform")

st.write("")

# ---------------- KPI Calculations ----------------

countries = len(df)

population = df["total_population"].sum() \
    if "total_population" in df.columns else 0

aircraft = df["total_military_aircraft"].sum() \
    if "total_military_aircraft" in df.columns else 0

tanks = df["tanks"].sum() \
    if "tanks" in df.columns else 0

navy = df["total_naval_assets"].sum() \
    if "total_naval_assets" in df.columns else (
        df["naval_assets"].sum()
        if "naval_assets" in df.columns else 0
    )

personnel = df["active_personnel"].sum() \
    if "active_personnel" in df.columns else 0

# ---------------- KPI Cards ----------------

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""
    <div class="metric-card">
    <div style="font-size:45px;">🌍</div>
    <div class="metric-title">Countries</div>
    <div class="metric-value">{countries}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
    <div style="font-size:45px;">👥</div>
    <div class="metric-title">Population</div>
    <div class="metric-value">{population:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
    <div style="font-size:45px;">✈️</div>
    <div class="metric-title">Aircraft</div>
    <div class="metric-value">{aircraft:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
    <div style="font-size:45px;">🛡️</div>
    <div class="metric-title">Tanks</div>
    <div class="metric-value">{tanks:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card">
    <div style="font-size:45px;">🚢</div>
    <div class="metric-title">Naval Fleet</div>
    <div class="metric-value">{navy:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class="metric-card">
    <div style="font-size:45px;">👨‍✈️</div>
    <div class="metric-title">Personnel</div>
    <div class="metric-value">{personnel:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")
# ==========================================================
# CHARTS SECTION
# ==========================================================

st.markdown("## 📊 Global Military Statistics")

left, right = st.columns(2)

# ==========================================================
# TOP 10 COUNTRIES BY POWER INDEX
# ==========================================================

with left:

    st.markdown("### 🏆 Top 10 Countries by Power Index")

    if "power_index" in df.columns:

        top10 = df.sort_values(
            by="power_index",
            ascending=True
        ).head(10)

        fig = px.bar(
            top10,
            x="country",
            y="power_index",
            color="power_index",
            text="power_index",
            template="plotly_dark"
        )

        fig.update_layout(

            paper_bgcolor="#102D52",
            plot_bgcolor="#102D52",

            font_color="white",

            xaxis_title="Country",

            yaxis_title="Power Index",

            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================================================
# CONTINENT DISTRIBUTION
# ==========================================================

with right:

    st.markdown("### 🌎 Countries by Continent")

    if "continent" in df.columns:

        continent = (
            df.groupby("continent")
            .size()
            .reset_index(name="Countries")
        )

        fig = px.pie(

            continent,

            names="continent",

            values="Countries",

            hole=.60,

            template="plotly_dark"
        )

        fig.update_layout(

            paper_bgcolor="#102D52",

            plot_bgcolor="#102D52",

            font_color="white",

            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.write("")

# ==========================================================
# SECOND ROW
# ==========================================================

left2, right2 = st.columns(2)

# ==========================================================
# DEFENSE BUDGET
# ==========================================================

with left2:

    if "defense_budget" in df.columns:

        st.markdown("### 💰 Top Defense Budgets")

        budget = df.sort_values(
            by="defense_budget",
            ascending=False
        ).head(10)

        fig = px.bar(

            budget,

            x="country",

            y="defense_budget",

            color="country",

            template="plotly_dark"
        )

        fig.update_layout(

            paper_bgcolor="#102D52",

            plot_bgcolor="#102D52",

            font_color="white",

            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================================================
# ACTIVE PERSONNEL
# ==========================================================

with right2:

    if "active_personnel" in df.columns:

        st.markdown("### 👨‍✈️ Active Military Personnel")

        personnel = df.sort_values(
            by="active_personnel",
            ascending=False
        ).head(10)

        fig = px.bar(

            personnel,

            x="country",

            y="active_personnel",

            color="country",

            template="plotly_dark"
        )

        fig.update_layout(

            paper_bgcolor="#102D52",

            plot_bgcolor="#102D52",

            font_color="white",

            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.markdown("---")
# ==========================================================
# NATION OVERVIEW
# ==========================================================

st.markdown("## 🌍 Nation Overview")
st.markdown("Select any country to view its military profile.")

country = st.selectbox(
    "🌎 Select Country",
    sorted(df["country"].unique())
)

nation = df[df["country"] == country].iloc[0]

st.write("")

# ==========================================================
# COUNTRY INFORMATION CARDS
# ==========================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.info(f"""
### 📍 Country

**{country}**

**Continent:** {nation.get("continent","N/A")}

**Region:** {nation.get("region","N/A")}

**Power Index:** {nation.get("power_index","N/A")}
""")

with c2:

    st.success(f"""
### 👥 Population

**Population:** {nation.get("total_population",0):,}

**Active Personnel:** {nation.get("active_personnel",0):,}

**Reserve Personnel:** {nation.get("reserve_personnel",0):,}
""")

with c3:

    st.warning(f"""
### 💰 Economy

**Defense Budget**

${nation.get("defense_budget",0):,}

**Budget/GDP Ratio**

{nation.get("budget_to_gdp_ratio","N/A")}
""")

st.markdown("---")

# ==========================================================
# BAR CHART
# ==========================================================

metrics = []

columns = [

("Aircraft","total_military_aircraft"),

("Tanks","tanks"),

("Naval Assets","total_naval_assets"),

("Personnel","active_personnel"),

("Helicopters","total_military_helicopters")

]

for name,col in columns:

    if col in nation.index:

        metrics.append([name,nation[col]])

metric_df = pd.DataFrame(

metrics,

columns=["Metric","Value"]

)

left,right = st.columns(2)

with left:

    st.subheader("📊 Military Capability")

    fig = px.bar(

        metric_df,

        x="Metric",

        y="Value",

        color="Metric",

        template="plotly_dark",

        text="Value"

    )

    fig.update_layout(

        paper_bgcolor="#102D52",

        plot_bgcolor="#102D52",

        font_color="white",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# RADAR CHART
# ==========================================================

with right:

    st.subheader("🛰 Military Strength Radar")

    radar = go.Figure()

    radar.add_trace(

        go.Scatterpolar(

            r=metric_df["Value"],

            theta=metric_df["Metric"],

            fill="toself",

            name=country

        )

    )

    radar.update_layout(

        template="plotly_dark",

        paper_bgcolor="#102D52",

        polar=dict(

            radialaxis=dict(

                visible=True

            )

        ),

        height=500

    )

    st.plotly_chart(

        radar,

        use_container_width=True

    )

st.markdown("---")

# ==========================================================
# COUNTRY DATA
# ==========================================================

st.subheader("📄 Complete Country Information")

st.dataframe(

nation.to_frame(),

use_container_width=True,

height=650

)

st.markdown("---")

# ==========================================================
# DOWNLOAD BUTTON
# ==========================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(

label="📥 Download Filtered Dataset",

data=csv,

file_name="filtered_military_data.csv",

mime="text/csv"

)

st.markdown("---")

st.caption("© 2026 Unified Military Analytics Dashboard | Module 5")
