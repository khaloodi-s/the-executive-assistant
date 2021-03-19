import discord
from discord.ext import commands
from discord.ext import tasks
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
from discord.ext.commands import has_role
from discord.ext.commands import has_any_role
from discord.ext.commands import is_owner
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
        self.class1IDs = registerClass1Sheet.col_values(2)
        self.class2IDs = registerClass2Sheet.col_values(2)
        self.class3IDs = registerClass3Sheet.col_values(2)
        self.class4IDs = registerClass4Sheet.col_values(2)
        self.class5IDs = registerClass5Sheet.col_values(2)
        self.class6IDs = registerClass6Sheet.col_values(2)
        self.class7IDs = registerClass7Sheet.col_values(2)
        self.class8IDs = registerClass8Sheet.col_values(2)
        self.class9IDs = registerClass9Sheet.col_values(2)
        print("registration operational.")


    @commands.command()
    @is_owner()
    async def refreshDB(self, ctx):
        self.class1IDs = registerClass1Sheet.col_values(2)
        self.class2IDs = registerClass2Sheet.col_values(2)
        self.class3IDs = registerClass3Sheet.col_values(2)
        self.class4IDs = registerClass4Sheet.col_values(2)
        self.class5IDs = registerClass5Sheet.col_values(2)
        self.class6IDs = registerClass6Sheet.col_values(2)
        self.class7IDs = registerClass7Sheet.col_values(2)
        self.class8IDs = registerClass8Sheet.col_values(2)
        self.class9IDs = registerClass9Sheet.col_values(2)
        await ctx.send("Local database updated.")


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        serverGuild = member.guild
        memberID = str(member.id)
        khaledUser = "<@187181902011170816>"

        delegateClass1Role = discord.utils.get(serverGuild.roles, name= "Arab League")
        delegateClass1VC = discord.utils.get(serverGuild.voice_channels, name= "Arab League")
        registration1TC = discord.utils.get(serverGuild.text_channels, name= "arab-league-registration-1")

        delegateClass2Role = discord.utils.get(serverGuild.roles, name= "CIA")
        delegateClass2VC = discord.utils.get(serverGuild.voice_channels, name= "CIA")
        registration2TC = discord.utils.get(serverGuild.text_channels, name= "cia-registration-2")

        delegateClass3Role = discord.utils.get(serverGuild.roles, name= "Security Council")
        delegateClass3VC = discord.utils.get(serverGuild.voice_channels, name= "Security Council")
        registration3TC = discord.utils.get(serverGuild.text_channels, name= "security-council-registration-3")

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
            description= f"{member.mention} has been marked as present.",
            colour= discord.Colour.green(),
            timestamp= datetime.utcnow()
        )
        presentConfirmationEmbed.set_footer(text= f"Triggered by {member}", icon_url= member.avatar_url)

        userNotFoundEmbed = discord.Embed(
            title= "Error 404...",
            description= f"{member.mention} joined the voice channel, but was not found on the register. \n Please take a screenshot of this message and contact {khaledUser}.",
            colour= discord.Colour.red(),
            timestamp= datetime.utcnow()
        )
        userNotFoundEmbed.set_footer(text= f"Triggered by {member}", icon_url= member.avatar_url)

        if (delegateClass1Role in member.roles) and ((after.channel == delegateClass1VC) or (after.channel in otherVCList)): 
            try:
                rowNum = self.class1IDs.index(memberID) + 1
            except ValueError:
                await registration1TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass1Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass1Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration1TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass2Role in member.roles) and ((after.channel == delegateClass2VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class2IDs.index(memberID) + 1
            except ValueError:
                await registration2TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass2Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass1Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration2TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass3Role in member.roles) and ((after.channel == delegateClass3VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class3IDs.index(memberID) + 1
            except ValueError:
                await registration3TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass3Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass3Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration3TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass4Role in member.roles) and ((after.channel == delegateClass4VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class4IDs.index(memberID) + 1
            except ValueError:
                await registration4TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass4Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass4Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration4TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass5Role in member.roles) and ((after.channel == delegateClass5VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class5IDs.index(memberID) + 1
            except ValueError:
                await registration5TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass5Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass5Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration5TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass6Role in member.roles) and ((after.channel == delegateClass6VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class6IDs.index(memberID) + 1
            except ValueError:
                await registration6TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass6Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass6Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration6TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass7Role in member.roles) and ((after.channel == delegateClass7VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class7IDs.index(memberID) + 1
            except ValueError:
                await registration7TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass7Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass7Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration7TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass8Role in member.roles) and ((after.channel == delegateClass8VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class8IDs.index(memberID) + 1
            except ValueError:
                await registration8TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass8Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass8Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration8TC.send(embed= presentConfirmationEmbed)

        elif (delegateClass9Role in member.roles) and ((after.channel == delegateClass9VC) or (after.channel in otherVCList)):
            try:
                rowNum = self.class9IDs.index(memberID) + 1
            except ValueError:
                await registration9TC.send(embed= userNotFoundEmbed)
            else:
                if str(registerClass9Sheet.cell(rowNum, (4 + weekNum)).value) == "FALSE":
                    registerClass9Sheet.update_cell(rowNum, (4 + weekNum), "TRUE")
                    await registration9TC.send(embed= presentConfirmationEmbed)

                    
def setup(client):
    client.add_cog(Registration(client))