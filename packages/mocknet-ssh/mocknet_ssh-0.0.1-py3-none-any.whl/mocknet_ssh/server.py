import asyncio
import asyncssh
import logging
from typing import Callable, Dict, Type

logger = logging.getLogger(__name__)
logger.propagate = True

class BaseSSHServer(asyncssh.SSHServer):
    def __init__(self, users: Dict[str, str]):
        self.users = users

    def connection_made(self, conn):
        logger.info("🔐 SSH connection opened")

    def connection_lost(self, exc):
        logger.info("🔌 SSH connection closed")

    def begin_auth(self, username):
        logger.info(f"[conn=0] Beginning auth for user {username}")
        return True

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        logger.info(f"🧪 Authenticating {username}")
        return self.users.get(username) == password


async def run_ssh_server(
    users: Dict[str, str],
    handler_factory: asyncssh.SSHServerSession,
    host: str = "127.0.0.1",
    port: int = 9999,
    host_key_path: str | asyncssh.SSHKey = "",
):
    if not host_key_path:
        host_key_path = asyncssh.generate_private_key("ssh-rsa")
        logger.info("🗝️ SSH host key generated in memory")

    class SSHServerWithSession(BaseSSHServer):
        def session_requested(self):
            return handler_factory()

    logger.info(f"Creating SSH listener on {host}, port {port}")
    await asyncssh.create_server(
        lambda: SSHServerWithSession(users),
        host,
        port,
        server_host_keys=[host_key_path],
    )
    logger.info(f"🚀 SSH mock server running on {host}:{port}")
    await asyncio.Future()  # run forever
