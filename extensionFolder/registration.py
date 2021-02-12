import discord
from discord.ext import commands
from discord.ext import tasks
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
from discord.ext.commands import has_role
from discord.ext.commands import has_any_role
import asyncio
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
gc = gspread.service_account(filename= f"{dir_path}/creds.json")
sh = gc.open("Executive Assistant Backend")
registerClass1Sheet = sh.worksheet("registerClass1")
registerClass2Sheet = sh.worksheet("registerClass2")
registerClass3Sheet = sh.worksheet("registerClass3")
registerClass4Sheet = sh.worksheet("registerClass4")
registerClass5Sheet = sh.worksheet("registerClass5")
registerClass6Sheet = sh.worksheet("registerClass6")
registerClass7Sheet = sh.worksheet("registerClass7")
registerClass8Sheet = sh.worksheet("registerClass8")
registerClass9Sheet = sh.worksheet("registerClass9")
registerBackend = sh.worksheet("registerBackend")
weekNum = int(registerBackend.cell(5, 3).value)

class Registration(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("registration operational.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        serverGuild = member.guild

        khaledUser = "<@187181902011170816>"

        delegateClass1Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 1")
        delegateClass1VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 1")
        registration1TC = discord.utils.get(serverGuild.text_channels, name= "registration-1")

        delegateClass2Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 2")
        delegateClass2VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 2")
        registration2TC = discord.utils.get(serverGuild.text_channels, name= "registration-2")

        delegateClass3Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 3")
        delegateClass3VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 3")
        registration3TC = discord.utils.get(serverGuild.text_channels, name= "registration-3")

        delegateClass4Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 4")
        delegateClass4VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 4")
        registration4TC = discord.utils.get(serverGuild.text_channels, name= "registration-4")

        delegateClass5Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 5")
        delegateClass5VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 5")
        registration5TC = discord.utils.get(serverGuild.text_channels, name= "registration-5")

        delegateClass6Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 6")
        delegateClass6VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 6")
        registration6TC = discord.utils.get(serverGuild.text_channels, name= "registration-6")

        delegateClass7Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 7")
        delegateClass7VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 7")
        registration7TC = discord.utils.get(serverGuild.text_channels, name= "registration-7")

        delegateClass8Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 8")
        delegateClass8VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 8")
        registration8TC = discord.utils.get(serverGuild.text_channels, name= "registration-8")

        delegateClass9Role = discord.utils.get(serverGuild.roles, name= "Delegate Class 9")
        delegateClass9VC = discord.utils.get(serverGuild.voice_channels, name= "Delegate Class 9")
        registration9TC = discord.utils.get(serverGuild.text_channels, name= "registration-9")

        otherVCList = [discord.utils.get(serverGuild.voice_channels, name= "Plenary Class"), discord.utils.get(serverGuild.voice_channels, name= "Assembly Room")]

        presentConfirmationEmbed = discord.Embed(
            title= "Registration Successful!",
            description= f"{member.mention} has been marked as present. \n \n If you think this was not supposed to happen, screenshot this and contact {khaledUser}.",
            colour= discord.Colour.green(),
            timestamp= datetime.utcnow()
        )
        presentConfirmationEmbed.set_footer(text= f"Requested by {member}", icon_url= member.avatar_url)

        userNotFoundEmbed = discord.Embed(
            title= "Error 404...",
            description= f"Delegate {member.mention} joined the voice channel, but was not found on the register. \n \n Please take a screenshot of this message and contact {khaledUser}.",
            colour= discord.Colour.red(),
            timestamp= datetime.utcnow()
        )
        userNotFoundEmbed.set_footer(text= f"Requested by {member}", icon_url= member.avatar_url)

        if (delegateClass1Role in member.roles) and ((after.channel == delegateClass1VC) or (after.channel in otherVCList)): 
            try:
                usernameCell = registerClass1Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration1TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass1Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass1Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration1TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass2Role in member.roles) and ((after.channel == delegateClass2VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass2Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration2TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass2Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass2Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration2TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass3Role in member.roles) and ((after.channel == delegateClass3VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass3Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration3TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass3Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass3Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration3TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass4Role in member.roles) and ((after.channel == delegateClass4VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass4Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration4TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass4Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass4Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration4TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass5Role in member.roles) and ((after.channel == delegateClass5VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass5Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration5TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass5Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass5Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration5TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass6Role in member.roles) and ((after.channel == delegateClass6VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass6Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration6TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass6Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass6Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration6TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass7Role in member.roles) and ((after.channel == delegateClass7VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass7Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration7TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass7Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass7Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration7TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass8Role in member.roles) and ((after.channel == delegateClass8VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass8Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration8TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass8Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass8Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration8TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass9Role in member.roles) and ((after.channel == delegateClass9VC) or (after.channel in otherVCList)):
            try:
                usernameCell = registerClass9Sheet.find(member.name + "#" + member.discriminator, in_column= 2)
            except gspread.exceptions.CellNotFound:
                registration9TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass9Sheet.cell(usernameCell.row, (3 + weekNum)).value) == "FALSE":
                    registerClass9Sheet.update_cell(usernameCell.row, (3 + weekNum), "TRUE")
                    await registration9TC.send(embed= presentConfirmationEmbed)

                    
def setup(client):
    client.add_cog(Registration(client))