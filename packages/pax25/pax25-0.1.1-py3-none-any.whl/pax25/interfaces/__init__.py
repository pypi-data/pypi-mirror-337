"""
This module contains the different interfaces which are included with pax25.
"""

from .dummy import DummyInterface
from .file import FileInterface
from .serial import SerialInterface
from .types import Interface
from .udp import UDPInterface

INTERFACE_TYPES = {
    "file": FileInterface,
    "dummy": DummyInterface,
    "serial": SerialInterface,
    "udp": UDPInterface,
}

__all__ = [
    "FileInterface",
    "Interface",
    "SerialInterface",
    "DummyInterface",
    "UDPInterface",
    "INTERFACE_TYPES",
]
