"""
Entry point
"""
__docformat__ = "google"


import logging
import os
import sys

from PySide6.QtWidgets import QApplication

from qrestic.ui import MainWidget


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
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=logging_levels.get(logging_level.lower(), logging.INFO),
    )


def main():
    """Entrypoint."""
    _setup_logging(os.getenv("LOGGING_LEVEL", "info"))
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
