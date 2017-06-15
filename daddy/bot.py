#!/usr/bin/env python3
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import discord

class MongoBot(commands.Bot):
    def __init__(self, command_prefix, database, formatter=None, description=None, pm_help=False, **options):
        super().__init__(command_prefix, formatter, description, pm_help, **options)
        self.db = database

    @staticmethod
    def handle_errors(cmd):
        @cmd.error
        async def cmd_error(error, ctx):
            if isinstance(error, (commands.errors.MissingRequiredArgument, commands.errors.BadArgument)):
                await bot.say("Usage:\n" + ''.join( bot.formatter.format_help_for(ctx, cmd)))
            else:
                await bot.say("<{}>: {}".format(type(error).__name__, error))
        return cmd

    async def get_user(self, user_id, guild_id):
        user = {}
        try:
            user = await self.db.data.find_one({"user_id": int(user_id), "guild_id": int(guild_id)})
        except Exception as e:
            print(e)
        finally:
            return user

    async def set_user(self, user_id, guild_id, **kwargs):
        if not kwargs:
            return True
        try:
            user = await self.get_user(user_id, guild_id)
            if user is None:
                await self.db.data.insert_one({"user_id": int(user_id), "guild_id": int(guild_id), **kwargs})
            else:
                await self.db.data.update_one(user, {"$set": kwargs})
            return True
        except Exception as e:
            print(e)
            return False
