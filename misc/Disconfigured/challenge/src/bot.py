from __future__ import annotations

from os import environ

from datetime import datetime

from discord import Game, Status, ChannelType
from discord.ext import commands

from cogs.admin_cog import Admin
from cogs.notes_cog import Notes
from cogs.error_handler_cog import CommandErrorHandler
from util.flag_handler import add_flag, add_dummy_notes
from util.logger import get_logger

logger = get_logger(__name__)

bot = commands.Bot(environ["BOT_PREFIX"],
                   help_command=commands.DefaultHelpCommand(dm_help=True))


@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')
    game = Game('DUCTF')
    await bot.change_presence(status=Status.online, activity=game)


@bot.event
async def on_message(message):
    if message.channel.id == int(environ["CHALLENGE_CHANNEL_ID"]):
        try:
            await message.delete()
        except Exception:
            logger.exception(
                "Couldn't delete message in guild %s: %s", message.guild.id, message.guild.name)

    await bot.process_commands(message)


@bot.check_once
async def check_ctf_started(ctx):
    if ctx.author.bot:
        return

    passed = await ctf_started(ctx)
    if not passed:
        # CommandFailer exceptions handled in error_handler_cog.py
        dm = ctx.author.dm_channel or await ctx.author.create_dm()

        await dm.send("Come back when the CTF starts :)")
        return False
    else:
        return True


async def ctf_started(ctx):
    if datetime.utcnow() > datetime.fromisoformat(environ["CTF_START_TIME_UTC"]):
        return True
    else:
        return False


@bot.check_once
async def in_challenge_channel(ctx):
    challenge_guild_id = int(environ["CHALLENGE_SERVER_ID"])
    challenge_channel_id = int(environ["CHALLENGE_CHANNEL_ID"])

    if ctx.channel.type == ChannelType.private:
        return True

    if ctx.guild.id == challenge_guild_id and ctx.channel.id != challenge_channel_id:
        dm = ctx.author.dm_channel or await ctx.author.create_dm()
        channel = bot.get_channel(int(environ["CHALLENGE_CHANNEL_ID"]))
        await dm.send(f"Please use the correct server challenge channel - {channel.mention}")
        return False
    else:
        return True


with open("dummy_notes.json") as f:
    add_dummy_notes(f)

with open("flag.txt") as f:
    flag = f.readline()
    add_flag(flag)

bot.add_cog(Notes(bot))
bot.add_cog(Admin(bot))
bot.add_cog(CommandErrorHandler(bot))
bot.run(environ['DISCORD_TOKEN'])
