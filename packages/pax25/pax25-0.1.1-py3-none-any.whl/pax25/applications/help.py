"""
Help command and utils.
"""

from pax25.applications.router import CommandContext, CommandRouter, CommandSpec
from pax25.applications.utils import send_message
from pax25.services.connection.connection import Connection


def build_help_entry(spec: CommandSpec) -> str:
    """
    Build a help entry from a spec.
    """
    entry = f"Topic: {spec.command}\r"
    if spec.aliases:
        entry += f"Aliases: {','.join(spec.aliases)}\r"
    return entry + "\r" + spec.help


def build_columns(entries_list: list[str]) -> list[str]:
    """
    Build lines of help topic columns.
    """
    topic_sets = []
    current_set = []
    for entry in entries_list:
        current_set.append(entry)
        if len(current_set) == 6:
            topic_sets.append(current_set)
            current_set = []
    if current_set:
        topic_sets.append(current_set)
    # This might truncate some commands, but since there's autocomplete, it's
    # unlikely to matter.
    lines = []
    for topic_set in topic_sets:
        string = ""
        for entry in topic_set:
            string += entry[:10].ljust(10)
        string = string.rstrip()
        lines.append(string)
    return lines


class Help:
    """
    Help system. Initiate it with your command router to automatically build a help
    index for all commands.
    """

    def __init__(self, command_router: CommandRouter) -> None:
        """
        Initialize the help system.
        """
        self.command_router = command_router

    def send_index(self, connection: Connection) -> None:
        """
        Send an index of all commands and topics.
        """
        command_list: list[str] = []
        header = "Type 'help topic' where topic is one of:\r"
        for command in sorted(self.command_router.command_set):
            [entry] = self.command_router.command_store[command]
            [_key, spec] = entry
            command_list.append(spec.command)
        send_message(connection, header + "\r".join(build_columns(command_list)))

    def run_help(self, connection: Connection, context: CommandContext) -> None:
        """
        Runs the 'help' command. Executed by the command router if we added the spec
        to it.
        """
        lookup = context.args_string.upper()
        if not lookup:
            self.send_index(connection)
            return
        try:
            candidates = self.command_router.command_store[lookup]
        except KeyError:
            send_message(
                connection,
                f"No help entry found for {repr(context.args_string)}. Type "
                "'help' for a list of entries.",
            )
            return
        if len(candidates) > 1:
            possibilities = sorted(entry[1].command for entry in candidates)
            send_message(
                connection,
                "Ambiguous topic. "
                f"Did you mean one of these?: {', '.join(possibilities)}",
            )
            return
        [entry] = candidates
        [_key, spec] = entry
        send_message(connection, build_help_entry(spec))

    @property
    def spec(self) -> CommandSpec:
        """
        A CommandSpec that can be
        :return:
        """
        return CommandSpec(
            command="help",
            aliases=("?",),
            function=self.run_help,
            help="Provides information on various commands. Type 'help' on "
            "its own to get a listing of commands, or 'help command' where command "
            "is a command to get help on.",
        )
