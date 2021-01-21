import discord
from discord.ext import commands

client  = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Bot online.")

client.run("ODAxODcwNDgwNjYyNTkzNTk3.YAm-FA.OH28Ishz_VT7I_fAJql69qCsD9M")