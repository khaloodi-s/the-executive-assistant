import discord
from discord.ext import commands

client  = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Bot online.")

client.run("ODAxODU0MDc4MjIwNTAxMDAz.YAmuzQ.VU5GfK-2UO6Jt1FEOZdyw2Rmpqs")