@bot.group(invoke_without_command = True)
async def weather(ctx):
    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find("Southborough Massachusetts")
    em = discord.Embed(
        title="Weather of Southborough, MA",
        description=f"```As of {date.today()}```",
        color=discord.Color.blue())
    em.add_field(name="Temperature", value=str(weather.current.temperature)+ "° F") 
    for forecast in weather.forecasts:
        em.add_field(name=str(forecast.date)[0:10], value=f"{str(forecast.sky_text)}: {str(forecast.temperature)}° F")
    await client.close()
    await ctx.send(embed=em)
