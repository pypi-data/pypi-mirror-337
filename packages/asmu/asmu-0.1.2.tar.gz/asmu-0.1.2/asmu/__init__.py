"""Welcome to the API of the asmu module!

To get started, navigate through the submodules on the right.

!!! info
    The [asmu.io][] is rarely used directly, but can be usefull to access the paramteres of audio interface IO.
    [asmu.processor][] and [asmu.acore][] are used for custum devices, that should probabpy be implemented in the package source code directly.
"""
# enable sounddevice ASIO
import os
os.environ["SD_ENABLE_ASIO"] = "1"

from .afile import AFile
from .asetup import ASetup
from .interface import Interface
from . import io
from . import generator
from . import effect
from . import analyzer

__all__ = ["Interface", "ASetup", "AFile"]

# enable logging
import logging
logging.getLogger("asmu").addHandler(logging.NullHandler())

def query_devices(device = None, kind = None):
    import sounddevice as sd
    return sd.query_devices(device, kind)
