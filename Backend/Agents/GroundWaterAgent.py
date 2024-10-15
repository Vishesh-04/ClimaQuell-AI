from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from pydantic import Field
import requests
import os

# Define Request and Response Models
class GroundwaterRequest(Model):
    location: str


class GroundWaterResponse(Model):
    location: str
    district_name: str
    annual_domestic_industrial_draft: float
    annual_irrigation_draft: float
    annual_groundwater_draft_total: float
    annual_replenishable_groundwater_resources: float
    natural_discharge_during_non_monsoon: float
    net_groundwater_availability: float
    projected_demand_upto_2025: float
    groundwater_availability_for_irrigation: float
    stage_of_groundwater_development: float


class ErrorResponse(Model):
    error: str


# Create an instance of the Agent class
GroundwaterAgent = Agent(
    name="GroundwaterAgent",
    port=8001,
    seed="Groundwater Agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Fund the agent if it's low on funds
fund_agent_if_low(GroundwaterAgent.wallet.address())


# Function to fetch groundwater data from a predefined JSON dataset (stored in context storage)

def fetch_groundwater_data(location):
    try:
        print(f"Fetching groundwater data for {location}")
        # Replace 'location' with 'district' in the API call
        url = f"http://localhost:8080/get/{location}"
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()

        # Return groundwater data in structured format
        return {
            "status": True,
            "district_name": data['district_name'],
            "annual_domestic_industrial_draft": data['annual_domestic_industrial_draft'],
            "annual_irrigation_draft": data['annual_irrigation_draft'],
            "annual_groundwater_draft_total": data['annual_groundwater_draft_total'],
            "annual_replenishable_groundwater_resources": data['annual_replenishable_groundwater_resources'],
            "natural_discharge_during_non_monsoon": data['natural_discharge_during_non_monsoon'],
            "net_groundwater_availability": data['net_groundwater_availability'],
            "projected_demand_upto_2025": data['projected_demand_upto_2025'],
            "groundwater_availability_for_irrigation": data['groundwater_availability_for_irrigation'],
            "stage_of_groundwater_development": data['stage_of_groundwater_development']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching groundwater data: {e}")
        return {"status": False, "error": str(e)}



# On agent startup, log the agent's details
@GroundwaterAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Groundwater Agent Address: {GroundwaterAgent.address}')


# Query handler for groundwater requests
@GroundwaterAgent.on_query(model=GroundwaterRequest, replies={GroundWaterResponse, ErrorResponse})
async def query_handler(ctx: Context, sender: str, msg: GroundwaterRequest):
    ctx.logger.info(f"Received groundwater query for location: {msg.location}")
    ctx.logger.info(f"Sender: {sender}")
    print(msg.location)

    # Fetch the groundwater data for the requested location asynchronously
    groundwater_data = fetch_groundwater_data(msg.location)

    if groundwater_data["status"]:
        # Send the groundwater data as a response
        ctx.logger.info(f"Weather data retrieved successfully: {groundwater_data}")
        await ctx.send(
            sender,
            GroundWaterResponse(
                location=msg.location,
                district_name=groundwater_data["district_name"],
                annual_domestic_industrial_draft=groundwater_data["annual_domestic_industrial_draft"],
                annual_irrigation_draft=groundwater_data["annual_irrigation_draft"],
                annual_groundwater_draft_total=groundwater_data["annual_groundwater_draft_total"],
                annual_replenishable_groundwater_resources=groundwater_data["annual_replenishable_groundwater_resources"],
                natural_discharge_during_non_monsoon=groundwater_data["natural_discharge_during_non_monsoon"],
                net_groundwater_availability=groundwater_data["net_groundwater_availability"],
                projected_demand_upto_2025=groundwater_data["projected_demand_upto_2025"],
                groundwater_availability_for_irrigation=groundwater_data["groundwater_availability_for_irrigation"],
                stage_of_groundwater_development=groundwater_data["stage_of_groundwater_development"]
            )
        )
    else:
        # Send an error response if fetching groundwater data failed
        await ctx.send(sender, ErrorResponse(error=groundwater_data["error"]))



if __name__ == "__main__":
    GroundwaterAgent.run()
