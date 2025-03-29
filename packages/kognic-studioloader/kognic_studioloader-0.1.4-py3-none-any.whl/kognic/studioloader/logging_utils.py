import logging


def setup_logging():
    TEXT_FORMAT = "%(asctime)-15s %(levelname)-s [%(name)-25s] %(message)s"
    logging.basicConfig(format=TEXT_FORMAT, level="INFO")
