# ---------------------------------------------------------------------
# Gufo Traceroute: Whois client
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Whois client impementation."""

# Python modules
import asyncio


class WhoisError(Exception):
    """Whois error base class."""


class WhoisConnectionError(Exception):
    """Cannot connect to whois server."""


class WhoisClient(object):
    """
    Asynchorous whois client.

    Args:
        addr: Whois server address or FQDN.
        port: Whois server port.
        timeout: Request timeout.
    """

    def __init__(
        self: "WhoisClient", addr: str, port: int = 43, timeout: float = 5.0
    ) -> None:
        self.addr = addr
        self.port = port
        self.timeout = timeout

    async def resolve_as(self: "WhoisClient", addr: str) -> int:
        """
        Resolve IP address and return the AS.

        Args:
            addr: IPv4/IPv6 address

        Returns:
            AS number.

        Raises:
            WhoisConnectionError: If failed to connect to whois server.
            WhoisError: On resolution error.
        """
        return await asyncio.wait_for(self._resolve_as(addr), self.timeout)

    async def _resolve_as(self: "WhoisClient", addr: str) -> int:
        """
        Interenal implementation for `resolve_as`.

        Args:
            addr: IPv4/IPv6 address

        Returns:
            AS number.

        Raises:
            WhoisConnectionError: If failed to connect to whois server.
            WhoisError: On resolution error.
        """
        try:
            reader, writer = await asyncio.open_connection(
                self.addr, self.port
            )
        except ConnectionRefusedError as e:
            msg = "Connection refused"
            raise WhoisConnectionError(msg) from e
        # Send request
        plen = 128 if ":" in addr else 32
        req = f"!r{addr}/{plen},l\n"
        writer.write(req.encode())
        # Wait for reply
        data = await reader.read(4096)
        writer.close()
        await writer.wait_closed()
        # Parse data
        resp = data.decode()
        if resp[0] != "A":
            msg = f"Whois error: {resp}"
            raise WhoisError(msg)
        for line in resp.splitlines():
            if line.startswith("origin:"):
                return int(line[7:].strip()[2:])
        msg = "No origin found"
        raise WhoisError(msg)
