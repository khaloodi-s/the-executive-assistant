import discord
from discord.ext import commands

client  = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Bot online.")

client.run("ODAxODcwNDgwNjYyNTkzNTk3.YAm-FA.HKdYLtTkla4R5GYABNfhK5IGZO0")