from discord import ChannelType
from discord.ext import commands

from util.logger import get_logger

logger = get_logger(__name__)


def is_admin():
    """ Check that returns True if invoking user is admin in invoking guild"""
    def predicate(ctx):
        if ctx.channel.type == ChannelType.private:
            return False
        else:
            return ctx.message.author.guild_permissions.administrator

    return commands.check(predicate)
