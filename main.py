import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
import os
import time
from datetime import datetime
import gspread
from discord.ext.commands import has_any_role
from discord.ext.commands import has_role
from discord.ext.commands import has_guild_permissions
from oauth2client.service_account import ServiceAccountCredentials

#All configurations used within this file are listed here:
intents = discord.Intents.default()
intents.members = True
commandPrefix = ("!")
client  = commands.Bot(command_prefix = commandPrefix, case_insensitive= True, intents= intents)
status = cycle(["for '!help'", "over the MUN server."])
botName = "The Executive Assistant"
dir_path = os.path.dirname(os.path.realpath(__file__))
gc = gspread.service_account(filename= f"{dir_path}/extensionFolder/creds.json")
sh = gc.open("Executive Assistant Backend")
registerBackend = sh.worksheet("registerBackend")

#Actual code starts here:

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@client.command(aliases=["cog load"])
@has_any_role("Trainers", "Administrators")
async def load(ctx, extension):
    client.load_extension(f"extensionFolder.{extension}")
    loadEmbed = discord.Embed(
        title= "Extension Loaded Successfully!",
        description= f"The {extension} extension has been loaded successfully. All commands and events within the module have been re-enabled. \n \n To re-disable the extension, please run the `{commandPrefix}unload` command.",
        colour= discord.Colour.green(),
        timestamp= datetime.utcnow()
    )
    
    loadEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

    if extension == "registration":
        registerUserEnabledBoolCell = registerBackend.cell(12, 6)
        registerBackend.update_cell(registerUserEnabledBoolCell.row, registerUserEnabledBoolCell.col, "TRUE")
    await ctx.send(embed= loadEmbed)

@client.command(aliases=["cog unload"])
@has_any_role("Trainers", "Administrators")
async def unload(ctx, extension):
    client.unload_extension(f"extensionFolder.{extension}")
    unloadEmbed = discord.Embed(
        title= "Extension Unloaded Successfully!",
        description= f"The {extension} extension has been unloaded successfully. All commands and events within the module have also been disabled. \n \n To re-enable the extension, please run the `{commandPrefix}load` command.",
        colour= discord.Colour.green(),
        timestamp= datetime.utcnow()
    )
    
    unloadEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

    if extension == "registration":
        registerUserEnabledBoolCell = registerBackend.cell(12, 6)
        registerBackend.update_cell(registerUserEnabledBoolCell.row, registerUserEnabledBoolCell.col, "FALSE")
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
    
    elif isinstance(error, commands.CommandInvokeError):
        if "already loaded" in str(error.__cause__):
            extensionAlreadyLoadedEmbed = discord.Embed(
                title= "That Module is Already Loaded...",
                description= f"{ctx.author.mention}, it looks like the extension / module that you're trying to load is already loaded up. \n \n If you think this error should not be happening, take a screenshot of your command and this message, then contact {khaledUser}.",
                colour= discord.Colour.red(),
                timestamp= datetime.utcnow()
            )
            extensionAlreadyLoadedEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
            await ctx.send(embed= extensionAlreadyLoadedEmbed)

        elif "not been loaded" in str(error.__cause__):
            extensionAlreadyUnloadedEmbed = discord.Embed(
                title= "That Module is Already Unloaded...",
                description= f"{ctx.author.mention}, it looks like the extension / module that you're trying to unload is already unloaded. \n \n If you think this error should not be happening, take a screenshot of your command and this message, then contact {khaledUser}.",
                colour= discord.Colour.red(),
                timestamp= datetime.utcnow()
            )
            extensionAlreadyUnloadedEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
            await ctx.send(embed= extensionAlreadyUnloadedEmbed)

    else:
        generalError = discord.Embed(
            title= "An Unexpected Error Occurred...",
            description= f"Oops... Try rerunning that command again. \n If it doesn't work, then you just found a bug! \n \n Contact {khaledUser} as soon as possible, in that case.",
            coloue= discord.Colour.red(),
            timestamp= datetime.utcnow()
        )
        generalError.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
        await ctx.send(embed= generalError)

@tasks.loop(seconds=60)
async def registration_toggle():

    triggerBoolCell = registerBackend.cell(10, 6)
    triggerBool = bool(triggerBoolCell.value == "TRUE")
    registerModuleEnabledBoolCell = registerBackend.cell(11, 6)
    registerModuleEnabledBool = bool(registerModuleEnabledBoolCell.value == "TRUE")
    registerUserEnabledBoolCell = registerBackend.cell(12, 6)
    registerUserEnabledBool = bool(registerUserEnabledBoolCell.value == "TRUE")
    
    registration1 = client.get_channel(807356010099769404)
    registration2 = client.get_channel(807356094351409214)
    registration3 = client.get_channel(807356191323455518)
    registration4 = client.get_channel(807356327457194027)
    registration5 = client.get_channel(807356553933488199)
    registration6 = client.get_channel(807356728848154664)
    registration7 = client.get_channel(824732506355007509)
    registration8 = client.get_channel(807357006755135548)
    registration9 = client.get_channel(807357166435434516)
    registration10 = client.get_channel(807357262007369759)

    registrationTCList = [registration1, registration2, registration3, registration4, registration5, registration6, registration7, registration8, registration9, registration10]

    onAnnounceEmbed = discord.Embed(
        title= "Registration Module has Been Loaded!",
        description= "Any delegates joining the class VC will be marked present from now on.",
        timestamp= datetime.utcnow()
    )
    onAnnounceEmbed.set_footer(text= "This is an automated process. No one requested it.", icon_url= "https://i.gyazo.com/4d5a4eb13a395edf0cf131efcc37718c.jpg")

    offAnnounceEmbed = discord.Embed(
        title= "Registration Module has Been Unloaded.",
        description= "Any delegates joining the class VC will no longer be marked as present from now on.",
        timestamp= datetime.utcnow()
    )
    offAnnounceEmbed.set_footer(text= "This is an automated process. No one requested it.", icon_url= "https://i.gyazo.com/4d5a4eb13a395edf0cf131efcc37718c.jpg")

    if (triggerBool and (not(registerModuleEnabledBool))):
        client.load_extension("extensionFolder.registration")
        registerBackend.update_cell(registerModuleEnabledBoolCell.row, registerModuleEnabledBoolCell.col, "TRUE")
        for channel in registrationTCList:
            await channel.send(embed= onAnnounceEmbed)

    elif ((not(triggerBool)) and registerModuleEnabledBool):
        client.unload_extension("extensionFolder.registration")
        registerBackend.update_cell(registerModuleEnabledBoolCell.row, registerModuleEnabledBoolCell.col, "FALSE")
        registerBackend.update_cell(registerUserEnabledBoolCell.row, registerUserEnabledBoolCell.col, "FALSE")
        print("registration unoperational.")
        for channel in registrationTCList:
            await channel.send(embed= offAnnounceEmbed)

    elif ((not(triggerBool)) and (not(registerModuleEnabledBool)) and registerUserEnabledBool):
        client.unload_extension("extensionFolder.registration")
        registerBackend.update_cell(registerUserEnabledBoolCell.row, registerUserEnabledBoolCell.col, "FALSE")


@client.event
async def on_ready():
    change_status.start()
    registration_toggle.start()
    registerBackend.update_cell(12, 6, "FALSE")
    print("main operational.")

for filename in os.listdir(f"{dir_path}/extensionFolder"):
    if filename.endswith(".py") and filename[:-3] != "registration":
        client.load_extension(f"extensionFolder.{filename[:-3]}")

client.run(os.environ.get("BOT_TOKEN"))
