import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GHG Forecasting Dashboard", layout="wide")

st.title("🌍 Climate Change Trend Analysis & Scenario Forecasting Dashboard")
st.markdown("---")

# Load compiled assets safely from your local directory
@st.cache_data
def load_internal_data():
    hist = pd.read_csv("owid-co2-data.csv")
    scen = pd.read_csv("scenario_projections.csv")
    return hist, scen

df_hist, df_scen = load_internal_data()

# Metric sidebar controls
st.sidebar.header("Navigation & Filters")
# Find the intersection of countries present in both datasets to prevent errors
countries_in_hist = set(df_hist['country'].unique())
countries_in_scen = set(df_scen['country'].unique())
common_countries = countries_in_hist.intersection(countries_in_scen)

target_countries = sorted(list(common_countries))
selected_country = st.sidebar.selectbox("Select Target Country Focus", target_countries)

# Section 1: Key Performance Indicators
st.subheader(f"📊 Macro Metrics Profile: {selected_country}")
c_hist = df_hist[df_hist['country'] == selected_country].sort_values('year')

# Dynamic Forecast Horizon calculations
min_forecast_year = int(df_scen['year'].min())
max_forecast_year = int(df_scen['year'].max())

# Safety check for historical CO2 values
if not c_hist.empty:
    latest_year = int(c_hist['year'].max())
    latest_co2_series = c_hist[c_hist['year'] == latest_year]['co2']
    
    if not latest_co2_series.empty and pd.notna(latest_co2_series.values[0]):
        latest_co2_val = latest_co2_series.values[0]
        latest_co2_str = f"{latest_co2_val:,.2f} MtCO₂"
    else:
        latest_co2_str = "Data N/A"
else:
    latest_year = "N/A"
    latest_co2_str = "Data N/A"

kpi1, kpi2 = st.columns(2)
kpi1.metric(label=f"Historical CO2 Emissions ({latest_year})", value=latest_co2_str)
kpi2.metric(label="Forecast Window Horizon", value=f"{min_forecast_year} — {max_forecast_year}")

# Section 2: Projections Plotting Frame
st.subheader("🔮 What-If Mitigation Pathways (2025–2044)")
c_scen = df_scen[df_scen['country'] == selected_country]

fig = px.line(c_scen, x='year', y='co2_projected', color='scenario',
              labels={'co2_projected': 'CO₂ Emissions (Mt)', 'year': 'Timeline Year'},
              title=f"Forecast Scenarios Comparison Vector for {selected_country}")
st.plotly_chart(fig, use_container_width=True)

st.markdown("🔒 *Dashboard successfully configured and running locally via VS Code terminal.*")