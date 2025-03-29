import logging


logger = logging.getLogger(__name__)

fmt = "%(asctime)s -- %(name)s -- [%(levelname)s] -- %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)
