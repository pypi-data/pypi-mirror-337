import asyncio
import logging
from typing import Dict
from mocknet_ssh.server import run_ssh_server
import asyncssh
from pathlib import Path
from importlib.resources import files
from importlib.resources.readers import MultiplexedPath

logger = logging.getLogger(__name__)
logger.propagate = True

COMMANDDIR = "mocknet_ssh.handlers.command_output.fortinet"
OS = "fortinet"


class FortinetHandler(asyncssh.SSHServerSession):
    def __init__(self) -> None:
        self._chan: asyncssh.SSHServerChannel | None = None
        self._buffer: str = ""
        self.mode: str = "exec"
        self.dynamic_commands: Dict[str, MultiplexedPath] = {}

        # Fixed directory path for command files
        command_dir = files(COMMANDDIR)
        self._load_dynamic_commands(command_dir)

    def _load_dynamic_commands(self, command_dir: MultiplexedPath) -> None:
        """Load commands from files in the given directory."""
        if not command_dir.is_dir():
            logger.warning(
                f"Command directory {command_dir} does not exist or is not a directory."
            )
            return

        for file in command_dir.iterdir():
            if file.is_file():
                # Convert filename to command (replace underscores with spaces)
                command = file.stem.removeprefix(f"{OS}_").replace("_", " ")
                self.dynamic_commands[command] = file
                logger.info(f"Loaded dynamic command: '{command}' from file: {file}")

    def connection_made(self, chan: asyncssh.SSHServerChannel) -> None:
        self._chan = chan
        logger.info("📡 Fortinet SSH session opened")

    def shell_requested(self) -> bool:
        return True

    def session_started(self) -> None:
        logger.info("🚪 Fortinet session started")
        if self._chan:
            self._chan.write("Welcome to Fortinet\n")
            self._chan.write(self._prompt())

    def data_received(self, data: str, datatype: asyncssh.DataType) -> None:
        self._buffer += data
        if "\n" in self._buffer:
            lines = self._buffer.split("\n")
            for line in lines[:-1]:
                self._handle_command(line.strip())
            self._buffer = lines[-1]

    def _handle_command(self, cmd: str) -> None:
        logger.info(f"🔧 Received command: {cmd}")

        if not self._chan:
            return

        if cmd == "config system global":
            self.mode = "config"
            self._chan.write("Entering configuration mode\n")
        elif cmd == "end":
            if self.mode == "config":
                self.mode = "exec"
                self._chan.write("Exiting configuration mode\n")
            else:
                self._chan.write("Invalid command\n")
        elif cmd in self.dynamic_commands and self.mode == "exec":
            # Dynamically loaded commands
            file_path = self.dynamic_commands[cmd]
            try:
                content = file_path.read_text()
                self._chan.write(content + "\n")
            except Exception as e:
                self._chan.write(f"Error reading file for command '{cmd}': {e}\n")
        else:
            self._chan.write(f"Invalid command: {cmd}\n")

        self._chan.write(self._prompt())

    def _prompt(self) -> str:
        return "FGT# " if self.mode == "config" else "FGT> "


def main() -> None:
    users: Dict[str, str] = {"admin": "password"}
    asyncio.run(run_ssh_server(users, handler_factory=FortinetHandler))


if __name__ == "__main__":
    main()
