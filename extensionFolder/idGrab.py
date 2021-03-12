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
wsh = sh.worksheet("delegateDataV2")


class IDGrab(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("idGrab operational.")

    
    @commands.command()
    @is_owner()
    async def getinfo(self, ctx):
        await ctx.send("Command initiated.")
        
        guildMemberList = ctx.guild.members

        print(guildMemberList)

        for i in range(0, len(guildMemberList)):
            wsh.update_cell(i+3, 2, str(guildMemberList[i].id))
            wsh.update_cell(i+3, 3, guildMemberList[i].name)
            wsh.update_cell(i+3, 4, str(guildMemberList[i].discriminator))
            wsh.update_cell(i+3, 5, guildMemberList[i].display_name)
            
            memeberTopRoleNames = guildMemberList[i].top_role.name.split()
            print(memeberTopRoleNames)

            if "Delegate" in memeberTopRoleNames:
                for a in range(0, len(memeberTopRoleNames)):
                    if memeberTopRoleNames[a].isdigit():
                        classNum = int(memeberTopRoleNames[a])
            else:
                classNum = "X"

            wsh.update_cell(i+3, 6, str(classNum))
            asyncio.sleep(3.1)

        await ctx.send("Compilation complete.")


def setup(client):
    client.add_cog(IDGrab(client))