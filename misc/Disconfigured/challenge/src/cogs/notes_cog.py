from __future__ import annotations

from datetime import datetime

from os import environ

from discord import ChannelType, Embed, Message
from discord.ext import commands, menus

from models.note import Note
from util import db
from util.logger import get_logger

logger = get_logger(__name__)

MAX_ALLOWED_NOTES = int(environ["MAX_ALLOWED_NOTES"])


class Notes(commands.Cog):
    """ Functionality relating to adding and retrieving notes """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """ Runs every time a message is sent

        Args:
            message (discord.Message): The message that triggered the invokation
        """
        if message.author.bot:
            return

        logger.debug(
            "%s#%s: %s", message.author.name, message.author.discriminator, message.clean_content)

        # Private message
        if message.channel.type == ChannelType.private:

            waiting_user = db.get_creating_note_user(message.author)

            if not waiting_user:
                return

            note = message.clean_content
            if not note:
                await message.channel.send("Your note must contain text.")
                return
            if len(note) >= 100:
                await message.channel.send("Notes must be less than 200 characters in length")
                return

            # If its not a self note
            if waiting_user.note_type == "guild_user":
                cleared_notes = db.add_guild_note(note, waiting_user)

                if cleared_notes:
                    await message.channel.send(
                        f"Saved your note for {waiting_user.guild_name} and cleared "
                        f"the rest. You are only allowed up to {MAX_ALLOWED_NOTES} notes.")
                else:
                    await message.channel.send(
                        f"Saved your note for {waiting_user.guild_name}!")
            elif waiting_user.note_type == "dm_user" and message.id != waiting_user.command_message_id:
                cleared_notes = db.add_self_note(note, waiting_user)
                if cleared_notes:
                    await message.channel.send(
                        "Saved your personal note and cleared the rest. You are "
                        f"only allowed up to {MAX_ALLOWED_NOTES} notes.")
                else:
                    await message.channel.send("Saved your personal note!")

    @commands.command()
    async def note(self, ctx: commands.Context):
        """ Start the creation of a new note. Be careful what you note - server admins can see all 👀

        Args:
            ctx (commands.Context): The invoking context
        """
        dm = ctx.author.dm_channel or await ctx.author.create_dm()

        if ctx.channel.type == ChannelType.private:
            db.add_creating_self_note_user(ctx.author, ctx.message.id)

            await dm.send("Please enter your personal note to save.\n"
                          "The format of a note is ```<title> | <contents>```")
        else:
            db.add_creating_note_user(ctx.author, ctx.guild)

            # try:
            #     await ctx.message.delete()
            # except Exception:
            #     logger.exception(
            #         "Couldn't delete message in guild %s: %s", ctx.guild.id, ctx.guild.name)

            await dm.send(f"Please enter your note to savein {ctx.guild.name}.\n"
                          "The format of a note is ```<title> | <contents>```")

    @commands.command()
    async def notes(self, ctx: commands.Context):
        """ Retrieve previously saved notes

        Args:
            ctx (commands.Context): The invoking context
        """
        dm = ctx.author.dm_channel or await ctx.author.create_dm()

        if ctx.channel.type == ChannelType.private:
            db.delete_from_waiting(user_id=ctx.author.id)
            notes = db.get_self_notes(ctx.author)

            if not notes:
                await dm.send(f"You have no DM notes saved!")
                return
        else:
            # try:
            #     await ctx.message.delete()
            # except Exception:
            #     logger.exception(
            #         "Couldn't delete message in guild %s: %s", ctx.guild.id, ctx.guild.name)

            db.delete_from_waiting(user_id=ctx.author.id)
            notes = db.get_member_notes(ctx.author, ctx.guild)

            if not notes:
                await dm.send(f"You have no notes saved in {ctx.guild.name}!")
                return

        pages = menus.MenuPages(source=NotesSource(
            notes), clear_reactions_after=True, timeout=15)
        await pages.start(ctx, channel=dm)

    @commands.command()
    async def clear(self, ctx: commands.Context):
        """ Clear a users notes

        Args:
            ctx (commands.Context): The invoking context
        """
        dm = ctx.author.dm_channel or await ctx.author.create_dm()

        if ctx.channel.type == ChannelType.private:
            db.clear_dm_notes(ctx.author.id)
            await dm.send("Cleared your DM notes!")
        else:
            db.clear_guild_notes(ctx.author.id, ctx.guild.id)

            # try:
            #     await ctx.message.delete()
            # except Exception:
            #     logger.exception(
            #         "Couldn't delete message in guild %s: %s", ctx.guild.id, ctx.guild.name)

            await dm.send(f"Cleared your notes for {ctx.guild.name}!")


class NotesSource(menus.ListPageSource):
    """ A source used to generate note info for the paginated displaying
    of stored notes """

    def __init__(self, notes: [Note]):
        super().__init__(notes, per_page=10)

    async def format_page(self, menu, notes: [Note]) -> Embed:
        """ Determine which notes to display in the embed and return the embed

        Args:
            menu ([type]): [description]
            notes ([Note]): The notes that are able to be displayed

        Returns:
            [discord.Embed]: The paginating embed that will be sent to the user
        """
        offset = menu.current_page * self.per_page
        fields = []

        for i, note in enumerate(notes, start=offset):
            value = ""
            if not note.content:
                value = "no content"
            else:
                value = note.content

            fields.append({
                'name': f'{i+1}. {note.title}',
                'value': value+"."
            })

        embed = Embed.from_dict({
            'title': 'Your Notes',
            'type': 'rich',
            'fields': fields,
            'color': 0x89c6f6
        })

        return embed
