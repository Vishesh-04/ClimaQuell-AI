# ClimaQuell

## Project Overview

In today’s rapidly changing world, access to real-time environmental data is essential for decision-making in agriculture, urban planning, and resource management. This AI chatbot provides users with timely weather and groundwater insights for regions across India, with plans to expand globally. The platform is designed to support users such as farmers, policy-makers, researchers, and tourists with essential environmental insights.

## Problem Statement

### Weather Monitoring

Accurate and timely weather data is crucial for industries like agriculture, tourism, and logistics. Many platforms only provide basic weather insights, which may lack the detail needed for informed decisions.

### Groundwater Insights

Groundwater is a vital resource, especially in regions with irregular rainfall. However, accessing reliable data on groundwater levels and quality remains challenging, particularly in rural areas.

## Solution Overview

Our AI chatbot addresses these challenges by offering real-time weather and groundwater data, including:

- Temperature, humidity, and wind data for any region.
- Groundwater details such as water table depth and quality metrics.

## Key Use Cases

### 1. Farmers

Plan irrigation and crop scheduling based on current weather and groundwater conditions.

### 2. Government Agencies

Monitor groundwater levels and climate conditions for efficient resource management.

### 3. Tourists

Access weather forecasts and local water data for informed travel planning.

---

## Features

### 1. District-Based Groundwater Query

- Input district name to retrieve detailed groundwater statistics.
- Displays statistics like annual groundwater draft, replenishable resources, and projected future demand.

### 2. Weather Monitoring

- Real-time weather updates for specific locations, including temperature, humidity, and wind data.

### 3. Error Handling

- Notifies users if any data retrieval fails, ensuring reliable user experience.

---

## Technical Details

- **Frontend**: Frontend is made up of React JS.
- **Backend**: Backend is made up of Flask to communicate between Frontend and Agents.

- **Agent**: Developed using the Fetch.AI uAgents library.
- **Data Sources**:
  - Groundwater data is extracted from Government Websites using Web Scraping.
  - Weather data from integrated APIs.
- **Protocols**: Custom protocols manage queries and responses for both weather and groundwater data.
- **Data Handling**: Processes data to provide users with real-time environmental insights.

## Future Enhancements

- **Historical Data**: Display trends over previous years to aid in long-term planning.
- **Predictive Analytics**: Integrate ML models to predict future groundwater and weather conditions.
- **Web Interface**: Develop a web interface for an interactive user experience.
- **Localization**: Support multiple languages to serve a global audience.

---

## How to Run the Project

1. **Fork the Repo and Clone the Repo**.
2. **Run the Frontend**: The Folder named Frontend contains all the filess required for frontend.
3. **Run the Backend**: All the Flask Backend Files are stored in Backend Folder.
4. **Get your API Key for Gemini and Weather API and set them in .env folder**.

---

## Collaboration

This project was developed with support from Fetch.ai Innovation Lab at Meerut Institute of Engineering and Technology (MIET), Meerut, Uttar Pradesh, India.
