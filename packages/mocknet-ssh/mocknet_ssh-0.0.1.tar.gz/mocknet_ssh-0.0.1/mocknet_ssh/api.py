import logging
import asyncio
from typing import Type, Dict
import asyncssh

from mocknet_ssh.server import run_ssh_server
from mocknet_ssh.handlers.cisco_ios import CiscoIOSHandler
from mocknet_ssh.handlers.cisco_nxos import CiscoNXOSHandler
from mocknet_ssh.handlers.cisco_asa import CiscoASAHandler
from mocknet_ssh.handlers.palo_alto_panos import PaloAltoPANOSHandler
from mocknet_ssh.handlers.fortinet import FortinetHandler

# Centralized logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

PLATFORM_HANDLERS: dict[str, Type[asyncssh.SSHServerSession]] = {
    "cisco_ios": CiscoIOSHandler,
    "cisco_nxos": CiscoNXOSHandler,
    "cisco_asa": CiscoASAHandler,
    "palo_alto_panos": PaloAltoPANOSHandler,
    "fortinet": FortinetHandler,
}


def start_mock_server(platform: str, username: str, password: str, port: int = 9999):
    handler_cls = PLATFORM_HANDLERS.get(platform)
    if not handler_cls:
        raise ValueError(f"Unknown platform: {platform}") 
    users: Dict[str, str] = {username: password}

    try:
        asyncio.run(run_ssh_server(users, handler_factory=handler_cls))
    except (OSError, asyncssh.Error) as exc:
        logging.error(f"❌ Failed to start server: {exc}")
