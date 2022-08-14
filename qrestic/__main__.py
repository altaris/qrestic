"""
Entry point
"""
__docformat__ = "google"


import logging
import logging.handlers
import os
import sys

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication, QStyleFactory

from qrestic.ui import MainWidget

VERSION = "0.1"


def _setup_logging(logging_level: str) -> None:
    """
    Sets logging format and level. The format is

        %(asctime)s [%(levelname)-8s] %(message)s

    e.g.

        2022-02-01 10:41:43,797 [INFO    ] Hello world
        2022-02-01 10:42:12,488 [CRITICAL] We're out of beans!

    Args:
        logging_level (str): Either 'critical', 'debug', 'error', 'info', or
            'warning', case insensitive. If invalid, defaults to 'info'.
    """
    logging_levels = {
        "critical": logging.CRITICAL,
        "debug": logging.DEBUG,
        "error": logging.ERROR,
        "info": logging.INFO,
        "warning": logging.WARNING,
    }
    logging_format = "%(asctime)s [%(levelname)-8s] %(message)s"
    logging.basicConfig(
        format=logging_format,
        level=logging_levels.get(logging_level.lower(), logging.INFO),
    )
    file_handler = logging.handlers.RotatingFileHandler("qrestic.log")
    file_handler.setFormatter(logging.Formatter(logging_format))
    logging.getLogger().addHandler(file_handler)


def main():
    """Entrypoint."""
    _setup_logging(os.getenv("LOGGING_LEVEL", "debug"))
    logging.info("Starting qrestic %s", VERSION)
    logging.info("System arguments: %s", sys.argv)
    app = QApplication(sys.argv)
    app.setApplicationName("qrestic")
    app.setApplicationVersion(VERSION)
    if "Fusion" in QStyleFactory.keys():
        app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator(app)
    if translator.load("qrestic/translations/translations_fr.qm"):
        app.installTranslator(translator)
        logging.info("Installed french translation")
    widget = MainWidget()
    widget.show()
    status = app.exec()
    logging.info("Exiting with status %d", status)
    sys.exit(status)


if __name__ == "__main__":
    main()
