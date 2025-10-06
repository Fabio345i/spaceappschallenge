# WeatherMellon 🌍

**NASA Earth Observation Weather System**

A modern weather platform combining 20+ years of satellite data with machine learning to deliver accurate predictions, disaster alerts, and interactive climate analysis.

---

## What Is WeatherMellon?

WeatherMellon is a comprehensive weather forecasting application that goes beyond simple temperature readings. It analyzes decades of NASA satellite data to predict future weather patterns, tracks natural disasters in real-time, and presents everything on an interactive 3D globe.

**Key Features:**
- Interactive 3D globe with location search
- Historical weather data from 1981 to present
- Machine learning-based weather predictions
- Hourly precipitation forecasts
- Real-time natural disaster alerts
- Save favorite locations
- Generate downloadable PDF reports

---

## Core Features

### 🌐 Interactive 3D Globe

Powered by [CesiumJS](https://cesium.com/learn/cesiumjs-learn/), the globe lets you explore weather data anywhere on Earth. Search for cities, view precise administrative boundaries, and navigate smoothly between locations. Click on disaster alerts to instantly fly to affected areas.

### 📈 Historical Climate Data

Access over 40 years of weather records from [NASA's POWER API](https://power.larc.nasa.gov/). View temperature trends, precipitation patterns, humidity levels, wind speeds, and atmospheric pressure for any location worldwide.

### 🔮 Predictive Weather Models

Machine learning algorithms analyze historical patterns to forecast future conditions. The system examines 20 years of data for similar dates, calculates climate trends, and predicts weather with measurable confidence scores:

### 🌧️ Hourly Precipitation Breakdown

Get detailed rainfall predictions for four time periods:
- **Night** (00:00 - 06:00)
- **Morning** (06:00 - 12:00)
- **Afternoon** (12:00 - 18:00)
- **Evening** (18:00 - 00:00)

### 🚨 Real-Time Disaster Monitoring

Live ticker displaying global natural disasters from [NASA's EONET](https://eonet.gsfc.nasa.gov/) database:
- Earthquakes with magnitude and location
- Hurricanes and tropical storms
- Wildfires and affected areas
- Floods, droughts, and severe weather

Click any alert to navigate directly to the disaster location on the globe.

### ⭐ User Favorites

Create an account to save your favorite locations. Quick access to places you monitor regularly with visual indicators (filled star) for saved locations.

### 📄 Weather Reports

Generate comprehensive PDF reports including:
- Complete meteorological data
- Weather forecasts and summaries
- Activity recommendations
- Preparation checklists
- Data sources and confidence scores

---

## Technology Stack

### Frontend
- **[Vue 3](https://vuejs.org/)** - Reactive framework with Composition API
- **[TailwindCSS](https://tailwindcss.com/)** - Utility-first styling with custom dark theme
- **[CesiumJS](https://cesium.com/learn/cesiumjs-learn/)** - 3D globe visualization
- **[Recharts](https://recharts.org/)** - Weather data charts
- **[Axios](https://axios-http.com/)** - API communication
- **[jsPDF](https://github.com/parallax/jsPDF)** - Report generation

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance Python API framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Database ORM
- **[JWT Authentication](https://jwt.io/)** - Secure user sessions
- **[Bcrypt](https://github.com/pyca/bcrypt/)** - Password hashing

### Data Sources & APIs
- **[NASA POWER API](https://power.larc.nasa.gov/)** - Historical climate data (1981-present)
- **[NLDAS2](https://ldas.gsfc.nasa.gov/nldas)** - High-resolution precipitation data
- **[Open-Meteo](https://open-meteo.com/)** - Real-time weather and forecasts
- **[Nominatim](https://nominatim.org/)** - Location geocoding (OpenStreetMap)
- **[OSM Boundaries API](https://osm-boundaries.com/)** - Administrative boundary data (GeoJSON)
- **[Overpass API](https://overpass-api.de/)** - OpenStreetMap data queries (fallback)
- **[EONET](https://eonet.gsfc.nasa.gov/)** - Natural disaster tracking

---

## How Predictions Work

### Temperature Forecasting

1. **Historical Analysis**: Gather 41 years of data for the target date (with configurable day window)
2. **Trend Calculation**: Compare recent years vs. historical average to identify climate trends
3. **Future Adjustment**: Apply trend to predict future temperatures
4. **Confidence Scoring**: Calculate reliability using exponential decay formula

```
confidence = 80 × exp(-0.001 × days_into_future)
```

### Precipitation Distribution

Hourly rainfall predictions use historical time-of-day patterns:
1. Calculate predicted daily total
2. Analyze historical distribution across time periods
3. Apply proportional distribution to predicted total
4. Add natural variability based on historical patterns

---

## Design System

### Color Palette

**Backgrounds:**
- Primary: `#000000` (Black)
- Secondary: `#111827` (Gray-900)
- Elevated: `#1F2937` (Gray-800)
- Transparent: `rgba(17, 24, 39, 0.95)` (Gray-900/95)

**Borders:**
- Primary: `#1F2937` (Gray-800)
- Secondary: `#374151` (Gray-700)

**Text:**
- Primary: `#F3F4F6` (Gray-100)
- Headings: `#FFFFFF` (White)
- Secondary: `#D1D5DB` (Gray-300)
- Muted: `#9CA3AF` (Gray-400)
- Disabled: `#6B7280` (Gray-500)

**Functional:**
- Success: Green-900 background / Green-400 text
- Error: Red-900 background / Red-400 text
- Warning: Yellow-500
- Accent: Blue-500

**Effects:**
- Backdrop blur: `backdrop-blur-sm`
- Dark transparency: `bg-black/40`
- Hover: Smooth transition from gray-300 to white

---

## API Endpoints

### Disasters
```
GET /disasters/headlines - Current natural disaster alerts
```

---

## Use Cases

**Weather Enthusiasts**: Track climate trends and explore historical weather patterns globally

**Trip Planning**: Get accurate forecasts with confidence scores for better travel decisions

**Emergency Planning**: Monitor real-time disasters and access detailed weather predictions

**Research**: Download comprehensive weather reports with historical data and trend analysis

**Agriculture**: Plan farming activities with hourly precipitation forecasts

**Outdoor Events**: Make informed decisions based on time-of-day weather predictions

---

## Team

**Space Golmons** - NASA Space Apps Challenge 2025

---

## License

MIT License

---

## Acknowledgments

- [NASA POWER API](https://power.larc.nasa.gov/) for comprehensive climate data
- [NOAA NLDAS2](https://ldas.gsfc.nasa.gov/nldas) for precipitation measurements
- [OpenStreetMap](https://www.openstreetmap.org/) for geocoding and boundaries
- [Cesium](https://cesium.com/) for 3D globe visualization
- [FastAPI](https://fastapi.tiangolo.com/) and [Vue.js](https://vuejs.org/) communities

---

Built with dedication for NASA Space Apps Challenge 2025 by **Space Golmons**
