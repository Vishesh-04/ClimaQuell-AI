# ClimaQuell

## Project Overview

In today’s rapidly changing world, access to real-time environmental data is essential for decision-making in agriculture, urban planning, and resource management. **ClimaQuell** is an AI-powered chatbot providing users with timely weather and groundwater insights across regions in India, with plans for global expansion. This platform is designed to support users such as farmers, policy-makers, researchers, and tourists with essential environmental information.

## Problem Statement

### Weather Monitoring

Accurate and timely weather data is critical for industries like agriculture, tourism, and logistics. Many platforms offer only basic weather insights, often lacking the depth needed for informed decision-making.

### Groundwater Insights

Groundwater is a vital resource, especially in areas with irregular rainfall. Accessing reliable data on groundwater levels and quality is often challenging, particularly in rural regions.

## Solution Overview

ClimaQuell addresses these challenges by providing real-time weather and groundwater data, including:

- Temperature, humidity, and wind data for any specified region.
- Groundwater details, such as water table depth and quality metrics.

## Key Use Cases

1. **Farmers**  
   Plan irrigation and crop scheduling based on current weather and groundwater conditions.

2. **Government Agencies**  
   Monitor groundwater levels and climate conditions for efficient resource management.

3. **Tourists**  
   Access weather forecasts and local water data for informed travel planning.

---

## Features

### 1. District-Based Groundwater Query
   - Retrieve detailed groundwater statistics by inputting the district name.
   - Provides statistics like annual groundwater draft, replenishable resources, and projected future demand.

### 2. Weather Monitoring
   - Offers real-time weather updates for specific locations, including temperature, humidity, and wind data.

### 3. Error Handling
   - Notifies users if any data retrieval fails, ensuring a reliable user experience.

---

## Technical Details

- **Frontend**: Built with React.js.
- **Backend**: Flask for communication between the frontend and agents.
- **Agent**: Developed using the Fetch.AI uAgents library.
- **Data Sources**:
  - Groundwater data sourced from government websites using web scraping.
  - Weather data retrieved from integrated APIs.
- **Protocols**: Custom protocols to manage queries and responses for weather and groundwater data.
- **Data Handling**: Processes data to provide users with real-time environmental insights.

---

## Future Enhancements

- **Historical Data**: Display trends over previous years to aid in long-term planning.
- **Predictive Analytics**: Integrate ML models to predict future groundwater and weather conditions.
- **Web Interface**: Develop a web interface for an interactive user experience.
- **Localization**: Support multiple languages to serve a global audience.

---

## Mentorship and Collaboration

This project was developed with support from the **Fetch.AI Innovation Lab** at Meerut Institute of Engineering and Technology (MIET), Meerut, Uttar Pradesh, India. Special thanks to **Dev Chauhan** and **Gautam Manak** for their valuable mentorship and guidance throughout the project.

---

## How to Run the Project

1. **Fork the Repo and Clone the Repo**.
2. **Run the Frontend**: Navigate to the `Frontend` folder, which contains all necessary files for the frontend.
3. **Run the Backend**: The `Backend` folder holds all Flask backend files.
4. **Set API Keys**: Get your API keys for Gemini and Weather API and set them in a `.env` file.

---
