import logging


def get_logger(name: str) -> logging.Logger:
    """ Get a standard logger, at DEBUG level

    Args:
        name (str): The name of the logger

    Returns:
        logging.Logger: The logger to use in the module
    """
    # file_handler = logging.FileHandler(
    #     filename="discord.log", encoding="utf-8", mode="a")
    # file_handler.setFormatter(logging.Formatter(
    #     "%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    logger = logging.getLogger(name)
    # logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)

    return logger
