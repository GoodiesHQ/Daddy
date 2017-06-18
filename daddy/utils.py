from argparse import ArgumentTypeError
from discord.ext import commands
import aiohttp
import asyncio
import functools
import os

async def http_get(url, lock=None, timeout=5.0, loop=None, **options):
    loop = loop or asyncio.get_event_loop()
    lock = lock or asyncio.Lock(loop=loop)
    async with lock:
        async with aiohttp.ClientSession(loop=loop) as client:
            async with client.get(url, timeout=timeout) as resp:
                await resp.text()
                return resp

async def http_multiget(*urls, conns=10, timeout=5.0, loop=None, **options):
    loop = loop or asyncio.get_event_loop()
    lock = asyncio.BoundedSemaphore(loop=loop)
    return await asyncio.gather(*[http_get(url, lock, timeout, loop) for url in urls])

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
