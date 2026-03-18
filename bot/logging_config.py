import logging


def setup_logger():
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # File handler (logs everything including debug payloads)
    fh = logging.FileHandler("bot.log")
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


logger = setup_logger()
