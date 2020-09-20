class Note():
    """ Represents a note which was provided as a string in the form <title> | <content>
    """
    title: str
    content: str

    def __init__(self, details: str):
        if "|" in details:
            split = details.split("|")
            self.title = split[0]
            self.content = split[1]
        else:
            self.title = ""
            self.content = details
