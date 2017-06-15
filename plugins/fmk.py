from daddy import utils
from discord.ext import commands
import discord

class FMK():
    """Fuck/Marry/Kill plugin for Daddy"""
    FMK_STR = ("fuck", "marry", "kill")
    BH = utils.BlackHole("Nobody Yet!")

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    async def fmk(self, ctx, member:discord.Member=None):
        if ctx.invoked_subcommand:
            return

        # target is either user-defined or the author of the message
        target = member or ctx.message.author
        user = await self.bot.get_user(target.id, ctx.message.server.id) or dict()

        # create the embedded data
        embed = discord.Embed(title=target.display_name, color=discord.Color(0xCF7F07))
        embed.set_thumbnail(url=target.avatar_url)

        for attrib in self.FMK_STR:
            tmp = ctx.message.server.get_member(str(user.get(attrib))) or self.BH
            embed.add_field(name=attrib.title(), value=tmp.mention, inline=False)

        await self.bot.say(embed=embed)

    @utils.cmd_error_handler
    @fmk.command(pass_context=True, invoke_without_command=True)
    async def fuck(self, ctx, member:discord.Member):
        await self,bot.set_user(ctx.message.author.id, ctx.message.server.id, fuck=int(member.id))

    @utils.cmd_error_handler
    @fmk.command(pass_context=True)
    async def marry(self, ctx, member:discord.Member):
        await self.bot.set_user(ctx.message.author.id, ctx.message.server.id, marry=int(member.id))

    @utils.cmd_error_handler
    @fmk.command(pass_context=True)
    async def kill(self, ctx, member:discord.Member):
        await self.bot.set_user(ctx.message.author.id, ctx.message.server.id, kill=int(member.id))

def setup(bot):
    bot.add_cog(FMK(bot))
