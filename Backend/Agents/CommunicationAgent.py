from uagents import Agent, Bureau, Context, Model


class Location(Model):
    location: str


TemperatureAgent = Agent(name="TemperatureAgent", seed="Temperature Agent secret phrase")
GroundwaterAgent = Agent(name="GroundwaterAgent", seed="Groundwater Agent secret phrase")


@TemperatureAgent.on_interval(period=3.0)
async def send_message(ctx: Context):
    await ctx.send(GroundwaterAgent.address, Location(Location="hello there slaanesh"))


@TemperatureAgent.on_message(model=Location)
async def TemperatureAgent_message_handler(ctx: Context, sender: str, msg: Location):
    ctx.logger.info(f"Received message from {sender}: {msg.Location}")


@GroundwaterAgent.on_message(model=Location)
async def GroundwaterAgent_message_handler(ctx: Context, sender: str, msg: Location):
    ctx.logger.info(f"Received message from {sender}: {msg.Location}")
    await ctx.send(TemperatureAgent.address, Location(Location="hello there sigmar"))


bureau = Bureau()
bureau.add(TemperatureAgent)
bureau.add(GroundwaterAgent)

if __name__ == "__main__":
    bureau.run()