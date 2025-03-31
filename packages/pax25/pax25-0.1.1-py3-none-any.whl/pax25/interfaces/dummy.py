"""
Dummy interface. No configuration, ignores everything. Used for tests.
"""

import asyncio
from asyncio import Queue, Task
from typing import TYPE_CHECKING

from ..ax25.address import Address
from ..ax25.frame import Frame
from ..utils import cancel
from .types import DummySettings, Interface

if TYPE_CHECKING:  # pragma: no cover
    from ..station import Station


class DummyInterface(Interface[DummySettings]):
    """
    Dummy interface for testing. Allows you to check the precise frames received and
    send exact frames as needed.
    """

    def __init__(self, name: str, settings: DummySettings, station: "Station"):
        """
        Just stash the args but don't do anything with them.
        """
        self.name = name
        self.known_addresses = settings.get("known_stations", [])
        self.settings = settings
        self.station = station
        self.gateway = settings.get("gateway", False)
        self.sent_frames: Queue[Frame] = Queue()
        self.queue: Queue[Frame] = Queue()
        self._loop: Task[None] | None = None

    @property
    def listening(self) -> bool:
        """
        Returns a bool indicating whether the interface is listening.
        """
        if not self._loop:
            return False
        return not self._loop.done()

    def is_preferred_address(self, address: Address) -> bool:
        """
        Determines whether the address we're contacting is a 'known address', allowing
        us to determine that this is the interface to use if one is not specified.
        """
        return str(address) in self.known_addresses

    def send_frame(self, frame: Frame) -> None:
        """
        Dummy send frame function.
        """
        self.sent_frames.put_nowait(frame)

    def start(self) -> None:
        """
        Starts the read loop.
        """
        self._loop = asyncio.ensure_future(self.read_loop())

    async def read_loop(self) -> None:
        """
        Dummy read loop function. Probably won't be an issue if it just returns
        immediately.
        """
        while True:
            frame = await self.queue.get()
            self.station.frame_router.process_frame(self, frame)
            self.queue.task_done()

    async def shutdown(self) -> None:
        """
        Dummy shut down function.
        """
        if self._loop:
            await cancel(self._loop)
            self._loop = None
