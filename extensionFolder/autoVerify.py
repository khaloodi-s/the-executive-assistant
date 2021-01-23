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
delegateData = sh.worksheet("delegateData")

class AutoVerify(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("autoVerify operational.")

    @commands.command()
    async def testGspread(self, ctx):
        printedB1 = discord.Embed(
            title= "Print of Cell B1, just testing...",
            description= f"Cell B1 holds value {delegateData.acell('B2').value}.",
            colour= discord.Colour.purple(),
            timestamp= datetime.utcnow(),
        )

        printedB1.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

        await ctx.send(embed= printedB1)

    @commands.command()
    async def verify(self, ctx):
        khaledUser = "<@187181902011170816>"
        verifierMention = ctx.author.mention
        positiveMark = "<:checkmark:802168750190755860>"
        negativeMark = "<:crossmark:802168043056529408>"
        positiveConfirmation = bool(False)
        negativeConfirmation = bool(False)

        notFoundEmbed = discord.Embed(
            title= "Error 404...",
            description= f"It's a classic error. Try the following, then re-run the command: \n - If have changed your username after you've sent it through the application form, try reverting it back. \n - If you have discord nitro, and changed your discriminator (the 4 digits after your username), change 'em back. \n - If you're an administrator or trainer, then this would be expected, contact the executive team. \n - If all of the above fail, or do not apply to you, contact {khaledUser}, or a member of the executive team.",
            colour= discord.Colour.red(),
            timestamp= datetime.utcnow()
        )
        notFoundEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

        try:
            userCell = delegateData.find(ctx.author.name + "#" + ctx.author.discriminator, in_column= 2)
            userNick = str(delegateData.cell(userCell.row, 3).value)
            classNum = str(delegateData.cell(userCell.row, 4).value)
            userRole = discord.utils.get(ctx.guild.roles, name= f"Delegate Class {classNum}")
        except gspread.exceptions.CellNotFound:
            await ctx.send(f"{ctx.author.mention}", embed= notFoundEmbed)
        else:
            confirmEmbed = discord.Embed(
                title= "Identity Confirmation",
                description= f"{verifierMention}, you're registered as {userNick}. \n \n If that's correct, click or press the {positiveMark} button under this message. \n If that's incorrect, click or press the {negativeMark} button under this message.",
                colour= discord.Colour.orange(),
                timestamp= datetime.utcnow()
            )
            confirmEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
            confirmationPrompt = await ctx.send(f"{ctx.author.mention}", embed= confirmEmbed)
            await confirmationPrompt.add_reaction(positiveMark)
            await confirmationPrompt.add_reaction(negativeMark)

            timeoutEmbed = discord.Embed(
                title= "Verification Process Failed",
                description= f"A timeout error has occurred. {verifierMention} took more than 20 seconds to complete the identity confirmation stage. \n Please try again, and be a litte quicker.",
                colour= discord.Colour.red(),
                timestamp= datetime.utcnow()
            )
            timeoutEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

            positiveFinalEmbed = discord.Embed(
                title= "Verification Successful!",
                description= f"Your verification has been successfully completed, {verifierMention}!\n You will be assigned to class {classNum}. \n \n You should be automatically roled in 10 seconds. Welcome to the club.",
                colour= discord.Colour.green(),
                timestamp= datetime.utcnow()
            )
            positiveFinalEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

            negativeFinalEmbed = discord.Embed(
                title= "Verification Unsuccessful",
                description= f"Your verification has failed, {verifierMention}.\n \n Please retry the verification process, or contact {khaledUser} as soon as possible.",
                colour= discord.Colour.red(),
                timestamp= datetime.utcnow()
            )
            negativeFinalEmbed.set_footer(text= f"Requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)

            def userCheck(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == positiveMark or str(reaction.emoji) == negativeMark)

            try:
                reaction, user = await self.client.wait_for("reaction_add", check= userCheck, timeout= 20.0)
                if str(reaction.emoji) == positiveMark:
                    positiveConfirmation = True
                elif str(reaction.emoji) == negativeMark:
                    negativeConfirmation = True
            except asyncio.TimeoutError:
                await confirmationPrompt.clear_reactions()
                await confirmationPrompt.edit(embed= timeoutEmbed)
            else:
                await confirmationPrompt.clear_reactions()
                if positiveConfirmation:
                    await confirmationPrompt.edit(embed= positiveFinalEmbed)
                    time.sleep(10)
                    await ctx.author.edit(nick= userNick, roles= [userRole])
                elif negativeConfirmation:
                    await confirmationPrompt.edit(embed= negativeFinalEmbed)

        

def setup(client):
    client.add_cog(AutoVerify(client))