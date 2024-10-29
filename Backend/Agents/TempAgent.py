import requests
import os
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class WeatherRequest(Model):
    location: str


class TemperatureResponse(Model):
    location: str
    time: str
    temperature: float
    condition: str
    humidity: int
    cloud: int
    wind_speed: float
    aqi: float


class ErrorResponse(Model):
    error: str




WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

TemperatureAgent = Agent(
    name="TemperatureAgent",
    port=8000,
    seed="Temperature Agent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(TemperatureAgent.wallet.address())


async def fetch_weather_data(location):
    try:
        print(f"Fetching weather data for {location}")
        url = f"http://api.weatherapi.com/v1/current.json?key=WEATHER_API_KEY&q={location}&aqi=yes"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return {
            "status": True,
            "time": data['location']['localtime'],
            "temp": data['current']['temp_c'],
            "condition": data['current']['condition']['text'],
            "humidity": data['current']['humidity'],
            "cloud": data['current']['cloud'],
            "wind_speed": data['current']['wind_mph'],
            "aqi": data['current']['air_quality']['pm2_5']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"status": False, "error": str(e)}

@TemperatureAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Temperature Agent Address: {TemperatureAgent.address}')


@TemperatureAgent.on_query(model=WeatherRequest, replies={TemperatureResponse, ErrorResponse})
async def query_handler(ctx: Context, sender: str, msg: WeatherRequest):
    ctx.logger.info(f"Received weather query for location: {msg.location}")
    ctx.logger.info(f"Sender: {sender}")
    print(msg.location)

    weather_data = await fetch_weather_data(msg.location)

    if weather_data["status"]:
        ctx.logger.info(f"Weather data retrieved successfully: {weather_data}")
        await ctx.send(
            sender,
            TemperatureResponse(
                location=msg.location,
                time=weather_data["time"],
                temperature=weather_data["temp"],
                condition=weather_data["condition"],
                humidity=weather_data["humidity"],
                cloud=weather_data["cloud"],
                wind_speed=weather_data["wind_speed"],
                aqi=weather_data["aqi"]
            )
        )
    else:
        ctx.logger.error(f"Failed to retrieve weather data: {weather_data['error']}")
        await ctx.send(sender, ErrorResponse(error="Failed to retrieve weather data."))


if __name__ == "__main__":
    TemperatureAgent.run()
