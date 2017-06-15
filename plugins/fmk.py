from daddy import utils
from discord.ext import commands
import discord

class FMK():
    """Fuck/Marry/Kill plugin for Daddy"""
    FMK_STR = ("fuck", "marry", "kill")
    BH = utils.BlackHole("Nobody Yet!")

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def fmk_error(fuck, marry, kill):
        if fuck and kill and fuck == kill:
            return "You cannot fuck a corpse, you degenerate."
        if fuck and marry and fuck == marry:
            return "You're already married to them."
        if marry and kill and marry == kill:
            return "You cannot be married to a corpse."
        return None

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    async def fmk(self, ctx, member:discord.Member=None):
        if ctx.invoked_subcommand:
            return

        # target is either user-defined or the author of the message
        target = member or ctx.message.author
        user = await self.bot.get_user(target.id, ctx.message.server.id)

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
        user_id, guild_id = ctx.message.author.id, ctx.message.server.id
        user = await self.bot.get_user(user_id, guild_id)
        msg = self.fmk_error(int(member.id), user.get("marry", None), user.get("kill", None))
        if msg:
            await self.bot.say(msg)
        else:
            await self.bot.set_user(user_id, guild_id, fuck=int(member.id))
            await self.bot.say("{} you'd fuck {}".format(ctx.message.author.mention, member.display_name))

    @utils.cmd_error_handler
    @fmk.command(pass_context=True)
    async def marry(self, ctx, member:discord.Member):
        user_id, guild_id = ctx.message.author.id, ctx.message.server.id
        user = await self.bot.get_user(user_id, guild_id)
        msg = self.fmk_error(user.get("fuck", None), int(member.id), user.get("kill", None))
        if msg:
            await self.bot.say(msg)
        else:
            await self.bot.set_user(user_id, guild_id, marry=int(member.id))
            await self.bot.say("{} you'd marry {}".format(ctx.message.author.mention, member.display_name))

    @utils.cmd_error_handler
    @fmk.command(pass_context=True)
    async def kill(self, ctx, member:discord.Member):
        user_id, guild_id = ctx.message.author.id, ctx.message.server.id
        user = await self.bot.get_user(user_id, guild_id)
        msg = self.fmk_error(user.get("fuck", None), user.get("marry", None), int(member.id))
        if msg:
            await self.bot.say(msg)
        else:
            await self.bot.set_user(user_id, guild_id, kill=int(member.id))
            await self.bot.say("{} you'd kill {}".format(ctx.message.author.mention, member.display_name))

def setup(bot):
    bot.add_cog(FMK(bot))
