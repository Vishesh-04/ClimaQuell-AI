from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
import re
import json
import asyncio
from uagents.query import query
from uagents import Model


# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enables CORS for all domains on all routes


# Define Request Data Model classes for interacting with agents
class WeatherRequest(Model):
    location: str


class GroundwaterRequest(Model):
    location: str


# Define agent addresses (replace with actual agent addresses)
weather_agent_address = 'agent1qvdk03p35yxstdc36xfk0a6zt8tncv45ky9d2hc5mvujhrtha5y573f8ylk'
groundwater_agent_address = "agent1qfrn3f60f85m37fushp4eg2u6luevadfv7gtrsfh88taycdk6qsjseytxau"

# Placeholder API key for the Gemini API (replace with your actual Gemini API key)
gemini_api_key = os.getenv('gemini_api_key')


def contains_greeting(user_input):
    # List of common greetings
    greetings = ["hello", "hi", "hey", "greetings", "what's up", "howdy", "welcome", "good morning", "good afternoon", "good evening"]
    # Check if any greeting is in the user input
    return any(greet in user_input.lower() for greet in greetings)

# Helper function to extract data type and location from Gemini's response
def extract_type_and_location(api_response):
    try:
        response_text = api_response['candidates'][0]['content']['parts'][0]['text']
        data_type_pattern = r"(\bweather\b|\bgroundwater\b|\bboth\b)"
        location_pattern = r"location is \*\*(\w+)\*\*"
        data_type_match = re.search(data_type_pattern, response_text, re.IGNORECASE)
        location_match = re.search(location_pattern, response_text, re.IGNORECASE)
        if data_type_match and location_match:
            return data_type_match.group(1), location_match.group(1)
        else:
            return None, None
    except (KeyError, TypeError) as e:
        print(f"Error extracting data from Gemini response: {e}")
        return None, None


# Endpoint to handle user prompts
@app.route('/query', methods=['POST'])
def handle_query():
    user_input = request.json.get('prompt')
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400

    gemini_prompt = {
        "contents": [{"parts": [{"text": f"Classify the user's request as weather, groundwater, or both, and extract the location from the query:  \"{user_input}\""}]}]
    }
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}'

    try:
        gemini_response = requests.post(url, headers={'Content-Type': 'application/json'}, json=gemini_prompt)

        if gemini_response.status_code != 200:
            return jsonify({"error": f"Failed to reach Gemini API: {gemini_response.status_code}"}), 500

        api_response = gemini_response.json()
        data_type, location = extract_type_and_location(api_response)

        weather_data, groundwater_data = None, None

        if data_type == 'both':
            weather_data = asyncio.run(query_weather(location))
            groundwater_data = asyncio.run(query_ground(location))  # Placeholder, implement actual query if needed
            return jsonify({
                "weather_data": weather_data,
                "groundwater_data": groundwater_data
            })
        elif data_type == 'weather':
            weather_data = asyncio.run(query_weather(location))
            return jsonify({
                "weather_data": weather_data
            })
        elif data_type == 'groundwater':
            groundwater_data = asyncio.run(query_ground(location))  # Placeholder, implement actual query if needed
            return jsonify({
                "groundwater_data": groundwater_data
            })
        elif contains_greeting(user_input):
            return jsonify({"response": "Hello! How can I assist you today?"}), 200
        else:
            fallback_prompt = {
                "contents": [{"parts": [{"text": f"The user's input does not clearly specify a request for weather, groundwater, or both, nor does it include a location. Please analyze the input and generate a valid response based on the context of: \"{user_input}\"."}]}]
            }
            url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}'

            try:
                gemini_response = requests.post(url, headers={'Content-Type': 'application/json'}, json=fallback_prompt)

                if gemini_response.status_code != 200:
                    return jsonify({"error": f"Failed to reach Gemini API: {gemini_response.status_code}"}), 500

                api_response = gemini_response.json()
                valid_response = api_response.get('content', 'No valid response received.')

                return jsonify({"response": valid_response}), 200  # Return the valid response in JSON format
            except Exception as e:
                return jsonify({"error": str(e)}), 500


    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Helper function to run weather query asynchronously
async def query_weather(location):
    try:
        print(f"Querying weather for location: {location}")

        # Send the query
        weather_data = await query(destination=weather_agent_address, message=WeatherRequest(location=location), timeout=30.0)

        if weather_data is None:
            raise ValueError("Received no response from the agent. The weather agent might be down.")

        # Decode payload
        decoded_payload = weather_data.decode_payload()
        if not decoded_payload:
            raise ValueError("The decoded payload is empty or invalid.")

        print(f"Raw weather data response: {decoded_payload}")
        return json.loads(decoded_payload)

    except Exception as e:
        print(f"Error during weather query: {e}")
        return {"error": "Failed to fetch weather data"}


async def query_ground(location):
    try:
        print(f"Querying Ground for location: {location}")

        # Send the query
        groundwater_data = await query(destination=groundwater_agent_address, message=GroundwaterRequest(location=location), timeout=30.0)

        if groundwater_data is None:
            raise ValueError("Received no response from the agent. The groundwater agent might be down.")

        # Decode payload
        decoded_payload = groundwater_data.decode_payload()
        if not decoded_payload:
            raise ValueError("The decoded payload is empty or invalid.")

        print(f"Raw GroundWater data response: {decoded_payload}")
        return json.loads(decoded_payload)

    except Exception as e:
        print(f"Error during GroundWater query: {e}")
        return {"error": "Failed to fetch GroundWater data"}


if __name__ == "__main__":
    app.run(debug=True)
