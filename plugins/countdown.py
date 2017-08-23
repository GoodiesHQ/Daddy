from daddy import utils
from discord.ext import commands
import aiohttp
import discord
import json

class Countdown():
    """Crypto exchange API for Daddy"""

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_url(src, dst):
        return Exchange.API_URL.format(src, dst)

    # @utils.cmd_error_handler
    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    async def crypto(self, ctx, src:str=None, dst:str=None):
        await self.bot.send_typing(ctx.message.channel)
        embed = discord.Embed(title="", color=discord.Color(0x41f498))
        exch = self.DEFAULT_EXCH
        send = False

        if dst is None and src:
            exch = [(src, self.DEFAULT_DST)]
        if dst and src:
            exch = [(src, dst)]

        urls = [self.create_url(s, d) for s, d in exch]
        responses = await utils.http_multiget(*urls, loop=self.bot.loop)

        for ((s, d), response) in zip(exch, responses):
            if response.status != 200:
                continue
            try:
                resp = json.loads(await response.text())
            except:
                continue
            if resp["success"] != True:
                continue
            send = True
            embed.add_field(name="{}".format(s.upper()), value="{:0.3f} {}".format(float(resp["ticker"]["price"]), d.upper()))

        if send:
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Countdown(bot))
