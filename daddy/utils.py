from argparse import ArgumentTypeError
from discord.ext import commands
import functools
import os

class BlackHole:
    def __init__(self, msg=""):
        self.__msg = msg

    def __getattr__(self, attr):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __str__(self):
        return self.__msg

def directory(path):
    if not os.path.isdir(path):
        raise ArgumentTypeError("'{}' does not exist.".format(path))
    return path

def cmd_error_handler(cmd):
    @cmd.error
    async def _(self, err, ctx):
        if isinstance(err, (commands.errors.MissingRequiredArgument, commands.errors.BadArgument)):
            await self.bot.say("Usage:\n" + ''.join(self.bot.formatter.format_help_for(ctx, cmd)))
        else:
            await self.bot.say("<{}>: {}".format(type(err).__name__, err))
    return cmd
