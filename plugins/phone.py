from daddy import utils
from discord.ext import commands
from urllib import parse
import aiohttp
import discord
import hashlib
import json
import re

class Phone():
    """Geolocation plugin for Daddy"""

    API_BASE = "https://numverify.com"
    API_URL = "https://numverify.com/php_helper_scripts/phone_api.php?secret_key={key}&number={num}"
    FIELDS = ("location", "country_name", "line_type", "carrier",)
    TITLES = ("City", "Country", "Type", "Carrier",)

    PATTERN = re.compile(r"<input.*name=['\"]scl_request_secret['\"].*value=['\"](.*)['\"]")
    HEADERS = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
    }


    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_url(number, scl_request_secret):
        md5 = hashlib.md5()
        data = number + scl_request_secret
        md5.update(data.encode() if isinstance(data, str) else data)
        return Phone.API_URL.format(key=md5.hexdigest(), num=number)

    @staticmethod
    def get_key(content):
        keysearch = Phone.PATTERN.search(content)
        if keysearch is None:
            return ""
        return keysearch.groups()[0]

    @utils.cmd_error_handler
    @commands.command(pass_context=True, no_pm=True)
    async def phone(self, ctx, number:str):
        await self.bot.send_typing(ctx.message.channel)
        response = await utils.http_get(self.API_BASE, timeout=7.0)
        key = self.get_key(await response.text())
        url = self.create_url(number, key)
        response = await utils.http_get(url)
        try:
            resp = json.loads(await response.text())
        except Exception as e:
            resp = {"valid": False}

        embed = discord.Embed(title="{}".format(number), color=discord.Color(0x31b438))
        if response.status != 200:
            embed.add_field(name="Failure", value="Status Code: {}".format(status))
        elif resp["valid"] != True:
            embed.add_field(name="Failure", value="Invalid phone number. Try prepending the country code!")
        else:
            for field, title in zip(self.FIELDS, self.TITLES):
                try:
                    value = resp[field]
                except KeyError as e:
                    value = "N/A"
                finally:
                    value = value or "Unknown"
                embed.add_field(name=title, value=value)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Phone(bot))
