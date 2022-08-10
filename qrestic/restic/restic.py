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

In the callback (which should have access to the `restic` variable), you
can access the latest output line using `get_line`. This method returns
either a string or an output line model (or a list thereof), see
`qrestic.restic.models`.
"""
__docformat__ = "google"

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Type, Union

from pydantic import BaseModel
from PySide6.QtCore import QObject, QProcess, QProcessEnvironment
from qrestic.configuration import Configuration
from qrestic.restic.models import SnapshotsOutput


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
        environment.insert("AWS_SECRET_ACCESS_KEY", repo_conf.secret_key)
        environment.insert("RESTIC_REPOSITORY", "s3:" + repo_conf.url)
        environment.insert("RESTIC_PASSWORD", repo_conf.password)
        self.setProcessEnvironment(environment)
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.setProgram(str(restic_conf.path))
        self.setArguments(["--verbose=3", "--json"])

    def _start(self, command: str, *args) -> None:
        """Initializes and starts the restic process"""
        self._command = command
        self.setArguments(self.arguments() + [command, *args])
        self.start()

    def backup(self, path: Path) -> None:
        """Calls the `backup` command"""
        self._start("backup", str(path))

    def get_line(self, ModelClass: Optional[Type[BaseModel]] = None) -> Union[str, BaseModel, List[BaseModel]]:
        """
        Parses and returns the latest output line. If a parsing error occured,
        or if `ModelClass` is left to `None`, returns the raw output string
        instead.
        """
        line = self.readLine().toStdString()
        if not line:
            raise RuntimeError("restic process didn't output a line")
        if ModelClass is None:
            return line
        try:
            document = json.loads(line)
            if isinstance(document, list):
                return list(map(ModelClass.parse_obj, document))
            return ModelClass.parse_obj(document)
        except Exception as e:  # pylint: disable=broad-except
            logging.debug(
                "Parsing error for command '%s': '%s'", self._command, e
            )
            return line

    def init(self) -> None:
        """Calls the `init` command"""
        self._start("init")

    def restore(self, snapshot_id: str, target: Path) -> None:
        """Calls the `restore` command"""
        self._start("restore", snapshot_id, str(target))

    def snapshots(self) -> None:
        """Calls the `shapshots` command"""
        self._start("snapshots")
