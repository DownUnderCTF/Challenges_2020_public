class WaitingUser():
    """Holds state for users we are waiting on to send a note to save"""
    user_id: int
    note_type: str

    def __init__(self, user_id: int, note_type: str):
        self.user_id = user_id
        self.note_type = note_type


class WaitingGuildUser(WaitingUser):
    """Holds state for users we are waiting on to send a note to save"""
    guild_id: int
    guild_name: str

    def __init__(self, user_id: int, guild_id: int, guild_name: str):
        super().__init__(user_id=user_id, note_type="guild_user")
        self.guild_id = guild_id
        self.guild_name = guild_name

    def to_dict(self) -> dict:
        """ Returns the note as a dict

        Returns:
            dict: The dict containing instance vars as keys with their values as
            the instance vars values
        """
        return {
            "user_id": self.user_id,
            "note_type": self.note_type,
            "guild_id": self.guild_id,
            "guild_name": self.guild_name
        }


class WaitingDMUser(WaitingUser):
    """Holds state for users we are waiting on to send a note to save"""
    command_message_id: int

    def __init__(self, user_id: int, command_message_id: int):
        super().__init__(user_id=user_id, note_type="dm_user")
        self.command_message_id = command_message_id

    def to_dict(self) -> dict:
        """ Returns the note as a dict

        Returns:
            dict: The dict containing instance vars as keys with their values as
            the instance vars values
        """
        return {
            "user_id": self.user_id,
            "note_type": self.note_type,
            "command_message_id": self.command_message_id
        }
