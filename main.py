import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
import os
import time
from datetime import datetime

#All configurations used within this file are listed here:
commandPrefix = ("!")
client  = commands.Bot(command_prefix = commandPrefix, case_insensitive= True)
status = cycle(["for '!help'", "over the MUN server.", "little delegates play around."])
botName = "botName placeholder"

#Actual code starts here:

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@client.command(aliases=["cog load"])
async def load(ctx, extension):
    client.load_extension(f"extensionFolder.{extension}")
    loadEmbed = discord.Embed(
        title= "Extension Loaded Successfully",
        description= f"The {extension} extension has been loaded successfully. All commands and events within the module have been re-enabled. \n \n To re-disable the extension, please run the `!unload` command.",
        colour= discord.Colour.green(),
        timestamp= datetime.utcnow()
    )
    
    loadEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

    await ctx.send(embed= loadEmbed)

@client.command(aliases=["cog unload"])
async def unload(ctx, extension):
    client.unload_extension(f"extensionFolder.{extension}")
    unloadEmbed = discord.Embed(
        title= "Extension Unloaded Successfully",
        description= f"The {extension} extension has been unloaded successfully. All commands and events within the module have also been disabled. \n \n To re-enable the extension, please run the `!load` command.",
        colour= discord.Colour.green(),
        timestamp= datetime.utcnow()
    )
    
    unloadEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

    await ctx.send(embed= unloadEmbed)

@client.command(aliases=["latency"])
async def ping(ctx):
    if round(client.latency * 1000) < 150:
        pingEmbedColour = discord.Colour.green()
    elif round(client.latency * 1000) < 300:
        pingEmbedColour = discord.Colour.orange()
    else:
        pingEmbedColour = discord.Colour.red()

    pingResponse = discord.Embed(
        title= ":ping_pong: Pong!",
        description= f"It takes {round(client.latency * 1000)}ms for me to respond!",
        colour= pingEmbedColour,
        timestamp= datetime.utcnow(),
    )

    pingResponse.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

    await ctx.send(embed= pingResponse)

@client.event
async def on_command_error(ctx, error):
    khaledUser = "<@187181902011170816>"
    if isinstance(error, commands.MissingRequiredArgument):
        incompleteError = discord.Embed(
            title= "Oops, Something Went Wrong...",
           description= f"{ctx.author.mention}, the command that you have tried to run is potentially incomplete. Please double-check your command, and try running it again. \n \n If this error persists, take a screenshot and contact {khaledUser}.",
           colour= discord.Colour.red(),
           timestamp= datetime.utcnow()
        )
        incompleteError.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
        await ctx.send(embed= incompleteError)

    elif isinstance(error, commands.MissingAnyRole):
        roleError = discord.Embed(
            title= "Oops, Something Went Wrong...",
           description= f"{ctx.author.mention}, you're missing a role required to run that command. Please double-check your roles, and retry running this command. \n \n If this error persists, take a screenshot and contact {khaledUser}.",
           colour= discord.Colour.red(),
           timestamp= datetime.utcnow()
        )
        roleError.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
        await ctx.send(embed= roleError)
        pass
    
    elif isinstance(error, commands.MissingRole):
        roleError = discord.Embed(
            title= "Oops, Something Went Wrong...",
           description= f"{ctx.author.mention}, you're missing a role required to run that command. Please double-check your roles, and retry running this command. \n \n If this error persists, take a screenshot and contact {khaledUser}.",
           colour= discord.Colour.red(),
           timestamp= datetime.utcnow()
        )
        roleError.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
        await ctx.send(embed= roleError)
        pass

    elif isinstance(error, commands.MissingPermissions):
        permError = discord.Embed(
            title= "Oops, Something Went Wrong...",
            description= f"{ctx.author.mention}, you're missing a permission required to run that command. Please double-check you permissions, and retry running this command. \n \n If this error persists, take a screenshot and contact {khaledUser}.",
            colour= discord.Colour.red(),
            timestamp= datetime.utcnow()
        )
        permError.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
        await ctx.send(embed= permError)

    elif isinstance(error, commands.CommandNotFound):
        invalidCommandEmbed = discord.Embed(
            title= "That Doesn't Look Like a Valid Command...",
            description= f"{ctx.author}, the command that you ran doesn't look like a... command? In short, you must've mistyped something. Double-check your spelling, run the help command, and run that command again. \n \n If you think this error shouldn't be happening, contact {khaledUser}.",
            colour= discord.Colour.red(),
            timestamp= datetime.utcnow()
        )
        invalidCommandEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
        await ctx.send(embed= invalidCommandEmbed)
    
    else:
        generalError = discord.Embed(
            title= "An Unexpected Error Occurred...",
            description= f"Oops... Try rerunning that command again. \n If it doesn't work, then you just found a bug! \n \n Contact {khaledUser} as soon as possible, in that case.",
            coloue= discord.Colour.red(),
            timestamp= datetime.utcnow()
        )
        generalError.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)


@client.event
async def on_ready():
    change_status.start()
    print("main operational.")

dir_path = os.path.dirname(os.path.realpath(__file__))

for filename in os.listdir(f"{dir_path}/extensionFolder"):
    if filename.endswith(".py"):
        client.load_extension(f"extensionFolder.{filename[:-3]}")

client.run("ODAxODcwNDgwNjYyNTkzNTk3.YAm-FA.SEGJw_6LSiejarqQ0q4HIQhBlH0")