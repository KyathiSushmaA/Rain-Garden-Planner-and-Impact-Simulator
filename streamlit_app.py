import streamlit as st
import geopandas as gpd
import rasterio
import pandas as pd
from rasterio.plot import show
#import matplotlib.pyplot as plt
import numpy as np
import requests
#import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from datetime import datetime

# ------------------------------------
# Title for the app
# ------------------------------------
st.title("Rain Garden Planner and Impact Simulator")

# ------------------------------------
# Load GIS Data: MS4 Service Areas
# ------------------------------------
# Download the file from Google Drive
url = "https://drive.google.com/uc?id=1Tfp6WNg2i6E7BkAWYSKwcIP0zTCUVzMx&export=download"
response = requests.get(url)

# Save it locally
with open("Hampton_Roads_MS4_Service_Areas.geojson", "wb") as f:
    f.write(response.content)

# Read the local file with GeoPandas
ms4_areas = gpd.read_file("Hampton_Roads_MS4_Service_Areas.geojson")

# ------------------------------------
# Create Folium Map and Display Maps
# ------------------------------------
# CSS to remove unnecessary padding between elements
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        margin: 0;
    }
    .element-container {
        margin-bottom: 0rem;
        padding: 0rem;
        margin: 0rem;
    }
    .stApp {
        overflow: hidden;
    }
    .main {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create the Folium Map centered on Norfolk, VA
center = [36.8508, -76.2859]
m = folium.Map(location=center, zoom_start=10)

# Add the MS4 GeoJSON layer
folium.GeoJson(
    ms4_areas,
    name="MS4 Service Areas",
    tooltip=folium.GeoJsonTooltip(fields=["LOCALITY"], aliases=["Locality:"]),
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Use Streamlit container to display the map without gaps
with st.container():
    st.write("Hampton Roads MS4 Service Areas")
    st_folium(m, width=800, height=600)
  
# ------------------------------------
# User Input: Rain Garden Size and Soil Type
# ------------------------------------
st.subheader("Rain Garden Size and Soil Type")
rain_garden_size = st.slider("Select Rain Garden Size (sq ft)", 50, 500, 100)
soil_type = st.selectbox("Select Soil Type", ["Clay", "Sandy", "Loamy"])

# Calculate Runoff Reduction
absorption_rate = {"Clay": 0.2, "Sandy": 0.5, "Loamy": 0.7}
runoff_reduction = absorption_rate[soil_type] * rain_garden_size
st.write(f"Estimated Runoff Reduction: {runoff_reduction:.2f} gallons")

# ------------------------------------
# Load Storm Event Data
# ------------------------------------
st.subheader("Storm Data")
storm_data = pd.read_csv('StormEvents_locations-ftp_v1.0_d2024_c20241017.csv')
storm_data['storm_label'] = (
        storm_data['EVENT_ID'].astype(str) +
        " - " + storm_data['LOCATION'] +
        " (" + storm_data['YEARMONTH'].astype(str) + ")"
)

# Extract relevant columns: Latitude, Longitude, and an optional weight (e.g., storm intensity)
storm_locations = storm_data[['LATITUDE', 'LONGITUDE']]
storm_locations = storm_locations.dropna()  # Drop rows with missing values

# Initialize Folium map centered at Norfolk, VA
m = folium.Map(location=[36.8508, -76.2859], zoom_start=8)

# Create Heat Map Layer
heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in storm_locations.iterrows()]
HeatMap(heat_data, radius=10).add_to(m)

# Display Heat Map in Streamlit
st.write("Storm Event Heat Map")
st_folium(m, width=800, height=600)

# Select Storm by Location
sorted_locations = sorted(storm_data['LOCATION'].unique(), key=lambda x: x.lower())
storm_location = st.selectbox("Select Storm Location", sorted_locations)
selected_event = storm_data[storm_data['LOCATION'] == storm_location]
st.write(f"Simulating Storm at: {storm_location}")
st.dataframe(selected_event)

# Filter storm data based on the selected location
filtered_storms = storm_data[storm_data['LOCATION'] == storm_location]

# Display events for the selected location
if not filtered_storms.empty:
    # Dropdown for Event ID and YEARMONTH related to the selected location
    event_label = st.selectbox(
        "Select Event (ID - YEARMONTH)",
        filtered_storms['storm_label'].values
    )

    # Extract the selected EVENT_ID from the dropdown
    selected_event_id = filtered_storms[filtered_storms['storm_label'] == event_label]['EVENT_ID'].values[0]

    # Display selected event ID and its data
    st.write(f"Simulating Storm Event ID: {selected_event_id}")
    st.dataframe(filtered_storms[filtered_storms['EVENT_ID'] == selected_event_id])
else:
    st.write("No events available for this location.")

# ------------------------------------
# Fetch Weather Data from OpenWeatherMap API
# ------------------------------------
api_key = "4e5b8d95f2caf58c830f77c801239677"  # Replace with your API key
api_url = f"https://api.openweathermap.org/data/2.5/weather?q=Norfolk&appid={api_key}&units=metric"

response = requests.get(api_url)

if response.status_code == 200:
    weather_data = response.json()

    # Extracting Weather Information
    city_name = weather_data.get('name', 'N/A')
    country = weather_data['sys'].get('country', 'N/A')
    temperature = weather_data['main'].get('temp', 'N/A')
    humidity = weather_data['main'].get('humidity', 'N/A')
    weather_desc = weather_data['weather'][0].get('description', 'N/A').title()
    wind_speed = weather_data['wind'].get('speed', 'N/A')
    sunrise = weather_data['sys'].get('sunrise')
    sunset = weather_data['sys'].get('sunset')

    # Convert Unix Timestamps to Readable Time
    sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
    sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M:%S')

    # Display Weather Information
    st.subheader(f"Weather in {city_name}, {country}")
    st.write(f"**Temperature:** {temperature} °C")
    st.write(f"**Humidity:** {humidity}%")
    st.write(f"**Condition:** {weather_desc}")
    st.write(f"**Wind Speed:** {wind_speed} m/s")
    st.write(f"**Sunrise:** {sunrise_time}")
    st.write(f"**Sunset:** {sunset_time}")

else:
    st.error(f"Error fetching weather data: {response.status_code}")
