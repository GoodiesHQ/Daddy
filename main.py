#!/usr/bin/env python3
from argparse import ArgumentParser
from daddy import utils
from daddy.bot import MongoBot
from motor.motor_asyncio import AsyncIOMotorClient
import os
import sys

try:
    import asyncio
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Daddy likes uvloop")

def main():
    ap = ArgumentParser()
    ap.add_argument("--plugins", "-p", type=utils.directory, default=utils.directory("plugins"))
    args = ap.parse_args()

    mtr = AsyncIOMotorClient()
    bot = MongoBot(command_prefix=">", database=mtr.daddy)

    cogs = ["{}.{}".format(args.plugins, os.path.splitext(filename)[0]) \
            for filename in next(os.walk(args.plugins))[2] \
            if not filename.startswith("_") \
            and filename.endswith(".py")
    ]

    plugins_loaded = len(cogs)

    @bot.event
    async def on_ready():
        print("Logged in as {} ({} plugins loaded)".format(bot.user.name, plugins_loaded))

    for cog in cogs:
        try:
            bot.load_extension(cog)
            print("{}: Loaded!".format(cog))
        except Exception as e:
            plugins_loaded -= 1
            print("{}: <{}> {}".format(cog, type(e).__name__, e), file=sys.stderr)

    bot.run("TOKEN")

if __name__ == "__main__":
    main()
    exit(0)

