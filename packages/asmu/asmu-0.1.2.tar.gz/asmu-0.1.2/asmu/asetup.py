import json
import pathlib
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .interface import Interface

logger = logging.getLogger(__name__)


class ASetup:
    def __init__(self, path: str, ) -> None:
        """The ASetup class handles .asmu JSON files, which store general Interface settings, IInput/IOutput configuration and calibration values. 

        Args:
            path: Path to .asmu file.
        """
        self.path = pathlib.Path(path)
        self.interface: "Interface" = None
        # add time/date and other info here
        now = datetime.now()
        self.date = now.strftime("%Y-%m-%dT%H:%M:%S%z") # ISO 8601


    def __del__(self):
        if self.interface is not None:
            self.interface.asetup = None

    def load(self):
        """Load setup data from given path.
        This is typically called by the interface, if you specify the `asetup` at initialization.
        When the `asetup` is specified at a later point, this method can be called manually to load the settings.

        Raises:
            ValueError: No associated Interface to load to.
        """
        if self.interface is None:
            raise ValueError("No associated Interface to load to.")
        with open(self.path, "r", encoding="utf-8") as asetup:
            self.deserialize(json.load(asetup))

    def save(self, path: Optional[str] = None):
        """Save setup data to given path.

        Args:
            path: When given, the setup is saved to this path instead. (Save Copy As)

        Raises:
            ValueError: No associated Interface to save from.
        """
        if self.interface is None:
            raise ValueError("No associated Interface to save from.")

        if path is not None:
            path = pathlib.Path(path)
        else:
            path = self.path

        with open(path, "w", encoding="utf-8") as asetup:
            asetup.write(json.dumps(self.serialize(), sort_keys=True, indent=4, separators=(',', ': ')))

    def serialize(self):
        data = self.interface.serialize()
        data["created"] = self.date
        return data

    def deserialize(self, data: dict):
        self.date = data["created"]
        self.interface.deserialize(data)
