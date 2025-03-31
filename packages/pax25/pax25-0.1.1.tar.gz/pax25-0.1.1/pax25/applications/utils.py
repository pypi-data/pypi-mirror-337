"""
Helper utilities for application building.
"""

from pax25.services.connection.connection import Connection


def send_message(
    connection: Connection, message: str, append_newline: bool = True
) -> None:
    """
    Send a message string to a particular connection.
    """
    if append_newline:
        message += "\r"
    connection.send_bytes(message.encode("utf-8"))
