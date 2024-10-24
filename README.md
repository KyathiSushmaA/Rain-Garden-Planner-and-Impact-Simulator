# 🌧️ Rain Garden Planner and Impact Simulator

## Description
This interactive web application helps users plan rain gardens by simulating storm events and providing insights based on GIS data. It integrates elevation data, weather forecasts, and environmental datasets to assess the impact of rain gardens in mitigating runoff.

---

## **Features**
- **MS4 Service Areas Visualization:** Explore municipal separate storm sewer systems (MS4) boundaries on an interactive map.
- **Elevation Data Analysis:** View and analyze elevation data to plan effective garden placement.
- **Storm Event Simulation:** Visualize past storm events in a specific location and assess their impact.
- **Weather Integration:** Get real-time weather data through OpenWeatherMap API to assist in planning.
- **Heat Map:** Display storm event density through an interactive heatmap.

---

## **Technologies Used**
- **Python**: Backend logic and data processing.
- **Streamlit**: Web framework for building the interactive interface.
- **Folium**: Interactive mapping tool for GIS data visualization.
- **Pandas**: Data manipulation and analysis.
- **OpenWeatherMap API**: Fetch real-time weather information.

---

## **Setup and Installation**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/YourRepository.git
   ```
2. **Navigate into the project directory:**
   ```bash
   cd Rain-Garden-Planner-and-Impact-Simulator
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## **Usage**
1. **Select a Location:** Explore MS4 service areas using the map.
2. **Plan Rain Gardens:** Input garden size and soil type to calculate runoff reduction.
3. **Simulate Storms:** Select a location and view past storm events.
4. **Check Weather:** Use the integrated weather widget to view real-time weather conditions.
5. **Explore Heat Map:** Visualize storm event density across the region.

---

## **How to Deploy on Streamlit Cloud**
1. **Push your code to a public GitHub repository.**
2. **Visit [Streamlit Community Cloud](https://streamlit.io/cloud).**
3. **Create a new app**: Connect your GitHub repository and select the branch.
4. **Click 'Deploy'** to launch your app.

---

## **Contributing**
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## **Acknowledgments**
- **OpenWeatherMap** for weather data.
- **Streamlit** for providing the web interface framework.
- **Folium** for map visualizations.

---
