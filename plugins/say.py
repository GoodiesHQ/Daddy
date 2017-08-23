from daddy import utils
from discord.ext import commands
from urllib import parse
import aiohttp
import discord
import json

class Say():
    """Echo plugin for Daddy"""

    ALLOWED = {
        "143653620200505344",
    }

    def __init__(self, bot):
        self.bot = bot

    @utils.cmd_error_handler
    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *, msg:str):
        if ctx.message.author.id not in self.ALLOWED:
            return
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Say(bot))
