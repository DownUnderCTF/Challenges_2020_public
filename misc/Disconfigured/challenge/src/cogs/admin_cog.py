from __future__ import annotations

from datetime import datetime

from os import environ

from discord.ext import commands
from discord import Message

from util import db
from util.logger import get_logger
from util.util import is_admin

logger = get_logger(__name__)


class Admin(commands.Cog):
    """ Admin cog containing functionality for server admins """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_admin()
    async def get_server_notes(self, ctx: commands.Context):
        """ Returns all of the notes affiliated with this server
        Requires server admin perms

        Args:
            ctx (commands.Context): Invoking context
        """
        # try:
        #     await ctx.message.delete()
        # except Exception:
        #     logger.exception(
        #         "Couldn't delete message in guild %s: %s", ctx.guild.id, ctx.guild.name)

        notes = db.get_guild_notes(guild_id=ctx.guild.id)

        await ctx.send("```"
                       f"{str(notes)[:1500]}"
                       "```")

    @commands.command()
    @is_admin()
    async def run_query(self, ctx: commands.Context, query: str, collection: str):
        """Run a query in the given collection

        Args:
            ctx (commands.Context): Invoking context
            query (str): The query to run, json form
            collection (str): The name of the collection to run the query in.
            It must already exist in the db.
        """
        # try:
        #     await ctx.message.delete()
        # except Exception:
        #     logger.exception(
        #         "Couldn't delete message in guild %s: %s", ctx.guild.id, ctx.guild.name)

        try:
            res = db.run_query(query, collection)
        except Exception:
            await ctx.send("Invalid query")
            return

        await ctx.send("```"
                       f"{str(res)[:1500]}"
                       "```")
