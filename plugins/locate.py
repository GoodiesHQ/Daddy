from daddy import utils
from discord.ext import commands
from urllib import parse
import aiohttp
import discord
import json

class Locate():
    """Geolocation plugin for Daddy"""

    API_URL = "http://ip-api.com/json/{}"
    FIELDS = ("as", "isp", "country", "city", "regionName", "zip", "timezone")
    TITLES = ("ASN", "ISP", "Country", "City", "Region", "Zip", "Time Zone")

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_url(host):
        return Locate.API_URL.format(parse.quote(host))

    @utils.cmd_error_handler
    @commands.command(pass_context=True, no_pm=True)
    async def locate(self, ctx, host:str):
        await self.bot.send_typing(ctx.message.channel)
        response = await utils.http_get(self.create_url(host), timeout=10.0)
        resp = json.loads(await response.text())
        embed = discord.Embed(title="Geolocation for {}".format(host), color=discord.Color(0x31b438))

        if response.status != 200:
            embed.add_field(name="Failure", value="Status Code: {}".format(status))
        elif resp["status"] == "failure" or resp["status"] == "fail":
            embed.add_field(name="Failure", value=resp["message"])
        else:
            for field, title in zip(self.FIELDS, self.TITLES):
                try:
                    value = resp[field]
                except KeyError as e:
                    value = "N/A"
                embed.add_field(name=title, value=resp[field])
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Locate(bot))
