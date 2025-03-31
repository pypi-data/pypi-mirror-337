"""
Data structures and functions used for ingesting and exporting KISS frames.
"""

import logging
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass

from pax25.ax25.exceptions import DisassemblyError
from pax25.ax25.frame import Frame
from pax25.ax25.protocols import Assembler
from pax25.interfaces.kiss.constants import (
    KISS_CMD_DATA,
    KISS_ENDIAN,
    KISS_ESCAPED_FEND,
    KISS_ESCAPED_FESC,
    KISS_FEND,
    KISS_FESC,
    KISS_SHIFT_PORT,
    KISS_TFEND,
    KISS_TFESC,
)

logger = logging.getLogger(__name__)


@dataclass
class ReaderState:
    """
    Dataclass for keeping track of KISS frame ingestion.
    """

    packet: bytes = b""
    command: bytes = b""
    packet_started: bool = False
    reading: bool = False
    escaped: bool = False
    ready: bool = False


ReaderUpdater = Callable[[bytes, ReaderState], None]


def requires_read(func: ReaderUpdater) -> ReaderUpdater:
    """
    Makes a function inert if the 'reading' state isn't set
    to true.
    """

    def wrapped(byte: bytes, state: ReaderState) -> None:
        if not state.reading:
            return
        func(byte, state)

    return wrapped


def handle_f_end(_byte: bytes, state: ReaderState) -> None:
    """
    Handle an f-end marker.
    """
    if not state.packet:
        state.packet_started = True
        return
    state.reading = False
    state.ready = True
    return


@requires_read
def handle_tf_esc(byte: bytes, state: ReaderState) -> None:
    """
    Handle a tf escape.
    """
    if state.escaped:
        state.packet += KISS_FESC
        state.escaped = False
        return
    # Just a normal byte if we're not escaped.
    state.packet += byte


@requires_read
def handle_f_esc(_byte: bytes, state: ReaderState) -> None:
    """
    Handle an f escape.
    """
    if state.escaped:
        # This is an error. Continue.
        state.escaped = False
        return
    state.escaped = True


@requires_read
def handle_tf_end(byte: bytes, state: ReaderState) -> None:
    """
    Handle a tf_end.
    """
    if state.escaped:
        state.packet += KISS_FEND
        state.escaped = False
        return
    # Not in escaped mode, so this is the actual byte.
    state.packet += byte


@requires_read
def handle_new_char(byte: bytes, state: ReaderState) -> None:
    """
    Handle any other byte character that's part of the KISS frame.
    """
    state.packet += byte


COMMAND_FUNCS: dict[bytes, ReaderUpdater] = {
    KISS_FEND: handle_f_end,
    KISS_FESC: handle_f_esc,
    KISS_TFEND: handle_tf_end,
    KISS_TFESC: handle_tf_esc,
}


def kiss_command(command: int, port: int, value: bytes) -> bytes:
    """
    Format a kiss command for transmission.
    """
    cmd_byte = port
    cmd_byte <<= KISS_SHIFT_PORT
    cmd_byte |= command
    value = value.replace(KISS_FESC, KISS_ESCAPED_FESC)
    value = value.replace(KISS_FEND, KISS_ESCAPED_FEND)
    return KISS_FEND + cmd_byte.to_bytes(1, KISS_ENDIAN) + value + KISS_FEND


# If we ever need new frame command types for some reason, we can register them here.
KISS_FRAME_DISASSEMBLERS: dict[bytes, type[Assembler]] = {
    KISS_CMD_DATA.to_bytes(1, KISS_ENDIAN): Frame
}


async def ax25_frames_from_kiss(
    read_byte: Callable[[], Awaitable[bytes]],
) -> AsyncIterator[Frame]:
    """
    Generator loop for reading KISS from a source. Drops all frames except for AX.25
    frames.
    """
    async for _, frame in read_from_kiss(read_byte):
        match frame:
            case Frame():
                yield frame


async def read_from_kiss(
    read_byte: Callable[[], Awaitable[bytes]],
) -> AsyncIterator[tuple[int, Assembler]]:
    """
    Generator loop for reading KISS frames from a source.
    """
    state = ReaderState()
    while byte := await read_byte():
        if state.packet_started and not state.reading and byte != KISS_FEND:
            # This is the command byte.
            state.command = byte
            state.reading = True
            continue
        modifier: ReaderUpdater = COMMAND_FUNCS.get(byte, handle_new_char)
        modifier(byte, state)
        if state.ready:
            try:
                disassembler = KISS_FRAME_DISASSEMBLERS.get(state.command, None)
                if disassembler is None:
                    raise DisassemblyError(
                        "No existing frame disassembler for this command."
                    )
                frame = disassembler.disassemble(state.packet)
                yield int.from_bytes(state.command, KISS_ENDIAN), frame
            except Exception as err:
                logger.debug("Packet decoding error: %s", (err,))
            state = ReaderState()
