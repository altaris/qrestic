"""
Restic subprocess handler module. The `Restic` class should be instanciated
anew for every command. When running a command, say `shapshots`, connect a
callback to the `readyRead` signal:

```py
app = QCoreApplication(sys.argv)
configuration = Configuration.parse_file(...)
restic = Restic(configuration)
restic.readyRead.connect(callback)
restic.finished.connect(app.quit)
restic.snapshots()
sys.exit(app.exec())
```

In the callback (which should have access to the `restic` variable), you can
access the latest output items (parsed lines) using `get_items`. This method
returns a list of either a string or an output line model, see
`qrestic.restic.models`.
"""
__docformat__ = "google"

import json
import logging
from typing import List, Optional, Sequence, Type, Union

from pydantic import BaseModel
from PySide6.QtCore import (
    QIODeviceBase,
    QObject,
    QProcess,
    QProcessEnvironment,
)
from qrestic.configuration import Configuration


class Restic(QProcess):
    """Restic process handler"""

    _command: str

    def __init__(
        self,
        configuration: Configuration,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        repo_conf, restic_conf = configuration.repository, configuration.restic
        environment = QProcessEnvironment.systemEnvironment()
        environment.insert("AWS_ACCESS_KEY_ID", repo_conf.access_key)
        environment.insert(
            "AWS_SECRET_ACCESS_KEY", repo_conf.secret_key.get_secret_value()
        )
        environment.insert("RESTIC_REPOSITORY", "s3:" + repo_conf.url)
        environment.insert(
            "RESTIC_PASSWORD", repo_conf.password.get_secret_value()
        )
        self.setProcessEnvironment(environment)
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.setProgram(str(restic_conf.path))
        self.setArguments(["--verbose=3", "--json"])

    def __str__(self) -> str:
        return f"Restic ({self._command})"

    def _start(self, command: str, *args) -> None:
        """Initializes and starts the restic process"""
        self._command = command
        self.setArguments(self.arguments() + [command, *args])
        logging.info("%s: starting with arguments %s", self, args)
        self.start(QIODeviceBase.OpenModeFlag.ReadOnly)

    def backup(self, path: str) -> None:
        """Calls the `backup` command"""
        self._start("backup", path)

    def get_items(
        self, ModelClass: Optional[Type[BaseModel]] = None
    ) -> Sequence[Union[str, BaseModel]]:
        """
        Parses and returns the latest output lines as a list of either strings
        or `ModelClass`. Each line is parsed to fit in a `ModelClass`. If the
        parsing is unsuccessful, or if `ModelClass` is left to `None`, the line
        is left as is. If no line was read form the process, an empty list is
        returned.

        The `Sequence` return type is used for covariance.
        """
        lines: Sequence[str] = self.readAll().toStdString().split("\n")
        lines = [x for x in lines if x]
        if not lines:
            logging.warning(
                "%s get_item: process didn't output any line", self
            )
            return []
        items: List[Union[str, BaseModel]] = []
        if ModelClass is None:
            items = lines  # type: ignore
        else:
            for line in lines:
                try:
                    document = json.loads(line)
                    if isinstance(document, list):
                        items += list(map(ModelClass.parse_obj, document))
                    else:
                        items.append(ModelClass.parse_obj(document))
                except Exception as e:  # pylint: disable=broad-except
                    logging.debug(
                        "%s get_item: output parsing error: %s", self, e
                    )
                    if line:
                        items.append(line)
        for item in items:
            logging.debug("%s get_item: %s", self, item)
        return items

    def init(self) -> None:
        """Calls the `init` command"""
        self._start("init")

    def restore(self, snapshot_id: str, target: str) -> None:
        """Calls the `restore` command"""
        self._start("restore", snapshot_id, "--target", target)

    def snapshots(self) -> None:
        """Calls the `shapshots` command"""
        self._start("snapshots")
