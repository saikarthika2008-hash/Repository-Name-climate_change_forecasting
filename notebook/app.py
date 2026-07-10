import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="GHG Trend Analysis",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------------
# DARK THEME
# ---------------------------------------------------------
st.markdown("""
<style>

.stApp{
    background-color:#111827;
    color:white;
}

section[data-testid="stSidebar"]{
    background-color:#1f2937;
}

h1,h2,h3,h4,h5,h6,p,label{
    color:white !important;
}

[data-testid="stMetricValue"]{
    color:white;
}

div[data-baseweb="select"]{
    color:black;
}

</style>
""",unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    hist = pd.read_csv("owid-co2-data.csv")
    scen = pd.read_csv("scenario_projections.csv")
    return hist, scen

df_hist, df_scen = load_data()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🌍 GHG Trend Analysis")
st.sidebar.caption("IDEAS TIH Summer Internship 2026")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Historical Trends",
        "Country Profile",
        "Forecasts",
        "Scenario Comparison",
        "About"
    ]
)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# COMMON DATA
# ---------------------------------------------------------
common = sorted(
    list(
        set(df_hist["country"].unique()).intersection(
            set(df_scen["country"].unique())
        )
    )
)
# ---------------------------------------------------------
# OVERVIEW
# ---------------------------------------------------------
if page == "Overview":

    st.title("🌍 Climate Change Trend Analysis Dashboard")

    selected_countries = st.multiselect(
        "Select Countries",
        common,
        default=["India"]
    )

    metric = st.selectbox(
        "Emission Metric",
        ["CO₂"]
    )

    overview_df = df_hist[
        (df_hist["country"].isin(selected_countries)) &
        (df_hist["year"] >= 1990)
    ]

    latest = overview_df[
        overview_df["country"] == selected_countries[0]
    ].sort_values("year")

    if not latest.empty:

        latest_year = int(latest["year"].max())
        latest_value = latest.iloc[-1]["co2"]

        c1, c2 = st.columns(2)

        c1.metric(
            "Latest CO₂",
            f"{latest_value:,.2f} Mt"
        )

        c2.metric(
            "Latest Year",
            latest_year
        )

    fig = px.line(
        overview_df,
        x="year",
        y="co2",
        color="country",
        title="Historical CO₂ Emissions (1990 Onwards)"
    )

    st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------
# HISTORICAL
# ---------------------------------------------------------
elif page == "Historical Trends":

    st.title("Historical Trends")

    country = st.selectbox(
        "Select Country",
        common,
        key="history"
    )

    history_df = df_hist[
        (df_hist["country"] == country) &
        (df_hist["year"] >= 1990)
    ]

    fig = px.line(
        history_df,
        x="year",
        y="co2",
        title=f"{country} CO₂ Emissions (1990 Onwards)"
    )

    st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------
# COUNTRY PROFILE
# ---------------------------------------------------------
elif page == "Country Profile":

    st.title("Country Profile")

    country = st.selectbox(
        "Choose Country",
        common,
        key="profile"
    )

    data = df_hist[
        df_hist["country"] == country
    ].sort_values("year")

    latest = data.iloc[-1]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Latest Year",
        int(latest["year"])
    )

    c2.metric(
        "Latest CO₂",
        f"{latest['co2']:.2f} Mt"
    )

    if "population" in data.columns:
        c3.metric(
            "Population",
            f"{latest['population']:,.0f}"
        )

    st.subheader("Historical CO₂ Trend")

    profile_df = data[data["year"] >= 1990]

    fig = px.line(
        profile_df,
        x="year",
        y="co2",
        title=f"{country} CO₂ Emissions (1990 Onwards)"
    )

    st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------
# FORECASTS
# ---------------------------------------------------------
elif page=="Forecasts":

    st.title("Forecast Analysis")

    country=st.selectbox(
        "Country",
        common
    )

    c=df_scen[df_scen.country==country]

    fig=px.line(
        c,
        x="year",
        y="co2_projected",
        color="scenario",
        title=f"Forecast Scenarios for {country}"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------------
# SCENARIO COMPARISON
# ---------------------------------------------------------
elif page=="Scenario Comparison":

    st.title("Scenario Comparison")

    country=st.selectbox(
        "Country",
        common
    )

    c=df_scen[df_scen.country==country]

    fig=px.line(
        c,
        x="year",
        y="co2_projected",
        color="scenario",
        markers=True
    )

    st.plotly_chart(fig,use_container_width=True)

    st.dataframe(c)

# ---------------------------------------------------------
# ABOUT
# ---------------------------------------------------------
elif page=="About":

    st.title("About")

    st.markdown("""
### 🌍 GHG Trend Analysis

This dashboard was developed for the **IDEAS TIH Summer Internship 2026**.

### Features

- Historical CO₂ Emission Trends
- Country-wise Analysis
- Forecasting (2025–2044)
- Scenario Comparison
- Interactive Plotly Charts
***Mentor: Sauparna Sarkar***
""")