"""
UDP Interface for AX25 frames/connections.
"""

import asyncio
import itertools
import logging
import socket
from asyncio import DatagramTransport, Queue, Task
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pax25.ax25.address import Address
from pax25.ax25.frame import Frame
from pax25.interfaces.types import Interface, UDPSettings
from pax25.utils import cancel_all

if TYPE_CHECKING:  # pragma: no cover
    from pax25.station import Station


logger = logging.getLogger(__name__)

DEFAULT_PORT = 7773
DEFAULT_ADDRESS = "0.0.0.0"


@dataclass
class LoopSpec:
    """
    Dataclass for tracking a particular connection point.
    """

    write_loop: Task[None]
    send_queue: Queue[Frame]


@dataclass(kw_only=True, frozen=True)
class ResolvedConnectionSpec:
    """
    Variant of ConnectionSpec where we've resolved the values to addresses and ports.
    """

    ip_address: str
    port: int


class UDPInterface(Interface[UDPSettings]):
    """
    Interface for UDP Connections between stations. This interface allows you to
    bridge packet networks through the Internet. Note that you are responsible for
    making sure that all connected systems are controlled by a licenced operator.

    That means configuring your firewall properly to not allow datagrams from untrusted
    sources. Note that if you just open your firewall on a specific port, anyone will
    be able to send packets to you just like they can over the air. The Internet is a
    much larger place than the airwaves.

    Packets are sent to ALL specified connections, regardless of address, to emulate
    a broadcast domain.
    """

    def __init__(self, name: str, settings: UDPSettings, station: "Station") -> None:
        self.name = name
        self.settings = settings
        self.connections: set[ResolvedConnectionSpec] = {
            ResolvedConnectionSpec(
                ip_address=value["ip_address"],
                port=value.get("port", DEFAULT_PORT),
            )
            for value in self.settings["connections"]
        }
        self.station = station
        self.transport: DatagramTransport | None = None
        self.read_queue: Queue[Frame] = Queue()
        self.send_queue: Queue[Frame] = Queue()
        self.gateway = settings.get("gateway", False)
        self._loops: list[LoopSpec] = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @property
    def listening(self) -> bool:
        """
        Returns if the interface is currently listening.
        """
        if self.transport:
            return not self.transport.is_closing()
        return False

    def is_preferred_address(self, address: Address) -> bool:
        """
        See if any of the specified addresses are ones we know about.
        """
        return address in set(
            itertools.chain(
                *(
                    Address.from_pattern_string(string)
                    for string in self.settings.get("known_addresses", [])
                )
            )
        )

    async def build_read_transport(self) -> None:
        """
        Build the read transport.
        """
        loop = asyncio.get_event_loop()
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: _Ax25UDPProtocol(
                station=self.station,
                interface=self,
            ),
            local_addr=(
                self.settings.get("listening_address", DEFAULT_ADDRESS),
                self.settings.get("listening_port", DEFAULT_PORT),
            ),
        )

    async def write_loop_for(
        self, entry: ResolvedConnectionSpec, queue: Queue[Frame]
    ) -> None:
        """
        Given a queue of Frames, loop over sending the frames.
        """
        while frame := await queue.get():
            try:
                self.sock.sendto(frame.assemble(), (entry.ip_address, entry.port))
            except Exception as err:
                logger.warning(
                    "Error sending frame to %s: %s",
                    ((entry.ip_address, entry.port), err),
                )

    def build_write_loops(self) -> None:
        """
        Build all the write loops for the specified connections.
        """
        for entry in self.connections:
            queue: Queue[Frame] = Queue()
            loop = asyncio.ensure_future(self.write_loop_for(entry, queue))
            self._loops.append(LoopSpec(send_queue=queue, write_loop=loop))

    def start(self) -> None:
        """
        Start the loops.
        """
        asyncio.ensure_future(self.build_read_transport())
        self.build_write_loops()

    def send_frame(self, frame: Frame) -> None:
        """
        Send frame to all write addresses.
        """
        for spec in self._loops:
            spec.send_queue.put_nowait(frame)

    async def shutdown(self) -> None:
        """
        Shut down all the listeners for UDP.
        """
        if self.transport:
            self.transport.close()
        await cancel_all(spec.write_loop for spec in self._loops)


class _Ax25UDPProtocol(asyncio.DatagramProtocol):
    """
    Datagram Protocol used by the UDP Interface to handle incoming packets.
    """

    def __init__(
        self,
        station: "Station",
        interface: UDPInterface,
    ):
        self.station = station
        self.interface = interface

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        """
        Handle the received datagram, disassembling the packet and sending it to
        the read queue.
        """
        try:
            frame = Frame.disassemble(data)
        except Exception as err:
            logger.info(
                "Dropping invalid frame from %s: %s",
                (addr, err),
            )
            return
        self.station.frame_router.process_frame(self.interface, frame)
