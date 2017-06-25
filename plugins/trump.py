from daddy import utils
from discord.ext import commands
from urllib import parse
import aiohttp
import discord
import json

class Trump():
    """Trump tweet plugin for Daddy"""

    API_GET = "https://trumpsalad.com/"
    API_POST = "https://trumpsalad.com/Quotes/GetQuote/"
    AVATAR_URL="http://i.imgur.com/OlL66s1.jpg"

    def __init__(self, bot):
        self.bot = bot

    @utils.cmd_error_handler
    @commands.command(pass_context=True, no_pm=True)
    async def trump(self, ctx):
        author = ctx.message.author
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_GET) as resp:
                await resp.text()
            async with session.post(self.API_POST) as resp:
                data = await resp.text()
        data = json.loads(data)
        embed = discord.Embed(title="Source", color=discord.Color(0xf4b042), url=data.get("Url", None))
        embed.set_thumbnail(url=self.AVATAR_URL)
        embed.add_field(name="Quote:", value=data.get("Quote"))
        embed.set_footer(text="Requested by: {}".format(author.display_name), icon_url=author.avatar_url)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Trump(bot))
