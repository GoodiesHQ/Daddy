from daddy import utils
from discord.ext import commands
from urllib import parse
import discord
import json

class Urban():
    """Urban Dictionary API plugin for Daddy"""

    API_URL = "http://api.urbandictionary.com/v0/define?term={}"

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_url(term):
        return Urban.API_URL.format(parse.quote(term))

    @utils.cmd_error_handler
    @commands.command(pass_context=True, no_pm=True)
    async def ud(self, ctx, *, term:str=None):
        num = 0

        if term is None:
            await self.bot.say("No term was provided.")
            return

        await self.bot.send_typing(ctx.message.channel)

        embed = discord.Embed(title=term, color=discord.Color(0x41f498))
        url = self.create_url(term)
        response = await utils.http_get(url, loop=self.bot.loop)

        info = json.loads(await response.text())["list"]
        try:
            info = info[num]
        except IndexError:
            await self.bot.say("Definition does not exist.")
            return

        author = ctx.message.author

        embed.add_field(name="Definition", value=info["definition"], inline=False)
        embed.add_field(name="Example", value=info["example"], inline=False)
        embed.add_field(name="Upvotes", value=str(info["thumbs_up"]), inline=True)
        embed.add_field(name="Downvotes", value=str(info["thumbs_down"]), inline=True)
        embed.set_footer(text="Requested by: {}".format(author.display_name), icon_url=author.avatar_url)

        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Urban(bot))
