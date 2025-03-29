# ---------------------------------------------------------------------
# Gufo Traceroute: Python Traceroute Library
# ---------------------------------------------------------------------
# Copyright (C) 2022-25, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Traceroute implementation."""

# Python modules
import asyncio
import socket
import sys
import time
from dataclasses import dataclass
from types import TracebackType
from typing import (
    AsyncIterable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
)

# Gufo Labs modules
from .whois import WhoisClient, WhoisError

HAS_LOOP_SENDTO = sys.version_info >= (3, 11)
IS_LINUX = sys.platform == "linux"
IS_DARWIN = sys.platform == "darwin"
HAS_BPF = IS_LINUX
PROTO_ICMP = 1
PROTO_UDP = 17
ICMP_UNREACH = 3
ICMP_TTL_EXCEEDED = 11
ACCEPTABLE_ICMP = (ICMP_UNREACH, ICMP_TTL_EXCEEDED)


if HAS_BPF:
    from .bpffilter import apply_ipv4_filter
else:

    def apply_ipv4_filter(
        sock: socket.socket, dst_addr: str, src_port: int, dst_port: int
    ) -> None:
        """
        Stub for apply_ipv4_filter.

        Does nothing.
        """


@dataclass
class Hop(object):
    """
    Single hop information.

    Args:
        addr: Hop address.
        rtt: Round-trip time in seconds.
        asn: Autonoumous System number,
            if as resolution is enabled.
    """

    addr: str
    rtt: float
    asn: int


@dataclass
class HopInfo(object):
    """
    Path hop information.

    Args:
        ttl: Current TTL.
        hops:
            List of hops.
            Items are either Hop or None in case of timeout.
    """

    ttl: int
    hops: List[Optional[Hop]]


class Traceroute(object):
    """
    Asynchronous traceroute.

    Args:
        max_hops: Limit of the hops to trace.
        src_addr: Source address of the UDP packet.
            Detect automatically if not set.
        src_port: Source port for UDP packet.
            `0` - get ephemeric port automatically.
        dst_port: Destination UDP port.
        timeout: Hop timeout.
        tos: DSCP/ToS mark for egress packets.
        min_ttl: Minimum TTL to start with.
        whois_addr: Whois server address or FQDN
            for authonomous system resolution.
        whois_port: Whois server port.
        resolve_as: Fill Hop.asn with the hop's autonomuous
            system number.

    Note:
        `resolve_as` option implies the requests to the
        external whois server. Requests may take additional
        time or may be blocked in closed environments.
    """

    def __init__(
        self: "Traceroute",
        max_hops: int = 30,
        src_addr: Optional[str] = None,
        src_port: int = 0,
        dst_port: int = 33434,
        timeout: float = 1.0,
        tos: int = 0,
        min_ttl: int = 1,
        whois_addr: str = "whois.radb.net",
        whois_port: int = 43,
        resolve_as: bool = False,
    ) -> None:
        self.max_hops = max_hops
        self.src_addr = src_addr
        self.src_port = src_port
        self.dst_port = dst_port
        self.timeout = timeout
        self.min_ttl = min_ttl
        self.tos = tos
        self._whois: Optional[WhoisClient] = None
        self._whois_cache: Dict[str, int] = {}
        if resolve_as:
            self._whois = WhoisClient(whois_addr, whois_port)

    async def __aenter__(self: "Traceroute") -> "Traceroute":
        """Asynchronous context manager entry."""
        return self

    async def __aexit__(
        self: "Traceroute",
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Asynchronous context manager exit."""

    async def traceroute(
        self: "Traceroute",
        addr: str,
        tries: int = 3,
        min_ttl: Optional[int] = None,
    ) -> AsyncIterable[HopInfo]:
        """
        Perform traceroute to address.

        Args:
            addr: Destination address.
            tries: Number of tries.
            min_ttl: Minimum TTL to start with.

        Returns:
            Iterable of HopInfo.

        Example:
            ``` python
            async with Traceroute() as tr:
                async for hop in tr.traceroute("127.0.0.1"):
                    print(hop)
            ```
        """
        if ":" in addr:
            # IPv6
            msg = "IPv6 is not implemented still"
            raise NotImplementedError(msg)
        else:
            # IPv4
            async for hop in self._traceroute_ipv4(
                addr, tries=tries, min_ttl=min_ttl
            ):
                yield hop

    async def _traceroute_ipv4(
        self: "Traceroute",
        addr: str,
        tries: int = 3,
        min_ttl: Optional[int] = None,
    ) -> AsyncIterable[HopInfo]:
        """
        Perform traceroute to address for IPv4.

        Args:
            addr: Destination address.
            tries: Number of tries.
            min_ttl: Minimum TTL to start with.

        Returns:
            Iterable of HopInfo.
        """
        # UDP socket to send requests
        send_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        if self.tos:
            send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, self.tos)
        send_socket.setblocking(False)
        # Bind UDP socket to acquire the source port
        send_socket.bind(
            (
                self.src_addr if self.src_addr else "0.0.0.0",  # noqa: S104
                self.src_port,
            )
        )
        src_port = send_socket.getsockname()[1]
        # Raw socket to receive the response
        recv_socket = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
        )
        apply_ipv4_filter(
            recv_socket,
            dst_addr=addr,
            src_port=src_port,
            dst_port=self.dst_port,
        )
        recv_socket.setblocking(False)
        # Calculate minimal TTL to start with
        min_ttl = max(self.min_ttl if min_ttl is None else min_ttl, 1)
        # Vary TTL in range min_ttl..max_hops
        for ttl in range(min_ttl, self.max_hops + 1):
            # Adjust egress packet TTL
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            hops: List[Optional[Hop]] = []
            for _ in range(tries):
                # Send UDP packet
                await self._sendto(send_socket, payload=b"", addr=addr)
                # Wait response or timeout
                try:
                    hop = await asyncio.wait_for(
                        self._get_hop_ipv4(
                            recv_socket, dst_addr=addr, src_port=src_port
                        ),
                        self.timeout,
                    )
                except TimeoutError:
                    hop = None
                hops.append(hop)
            yield HopInfo(ttl=ttl, hops=hops)
            if any(True for h in hops if h is not None and h.addr == addr):
                break

    if HAS_LOOP_SENDTO:

        async def _sendto(
            self: "Traceroute", sock: socket.socket, payload: bytes, addr: str
        ) -> None:
            """
            Send payload to addr.

            Python 3.11+ version.

            Args:
                sock: Socket instance.
                payload: Packet payload
                addr: destiation address
            """
            loop = asyncio.get_running_loop()
            await loop.sock_sendto(sock, payload, (addr, self.dst_port))

        async def _recvfrom(
            self: "Traceroute", sock: socket.socket
        ) -> Tuple[bytes, Tuple[str, int]]:
            """
            Receive packet from socket.

            Python 3.11+ version.

            Args:
                sock: Socket instance.

            Returns:
                Tuple of (data, (addr, port))
            """
            loop = asyncio.get_running_loop()
            return await loop.sock_recvfrom(sock, 4096)

    else:

        async def _sendto(
            self: "Traceroute", sock: socket.socket, payload: bytes, addr: str
        ) -> None:
            """
            Send payload to addr.

            Backport from Python 3.11 to the prior versions.

            Args:
                sock: Socket instance.
                payload: Packet payload
                addr: destiation address
            """

            def callback() -> None:
                if fut.done():
                    return  # Cancelled
                try:
                    sock.sendto(payload, (addr, self.dst_port))
                except (BlockingIOError, InterruptedError):
                    return
                except (SystemExit, KeyboardInterrupt):
                    raise
                except BaseException as exc:  # noqa: BLE001
                    fut.set_exception(exc)
                else:
                    fut.set_result(None)

            def done(_fut: asyncio.Future[None]) -> None:
                if handle is None or not handle.cancelled():
                    loop.remove_writer(fd)

            try:
                sock.sendto(payload, (addr, self.dst_port))
                return
            except (BlockingIOError, InterruptedError):
                pass
            loop = asyncio.get_running_loop()
            fut = loop.create_future()
            fd = sock.fileno()
            handle = loop.add_writer(fd, callback=callback)
            fut.add_done_callback(done)
            await fut

        async def _recvfrom(
            self: "Traceroute", sock: socket.socket
        ) -> Tuple[bytes, Tuple[str, int]]:
            """
            Receive packet from socket. Prior to Python 3.11 version.

            Args:
                sock: Socket instance.

            Returns:
                Tuple of (data, (addr, port))
            """

            def callback() -> None:
                if fut.done():
                    return  # Cancelled
                try:
                    data, addr = sock.recvfrom(SIZE)
                except (BlockingIOError, InterruptedError):
                    return
                except (SystemExit, KeyboardInterrupt):
                    raise
                except BaseException as exc:  # noqa: BLE001
                    fut.set_exception(exc)
                else:
                    fut.set_result((data, addr))

            def done(
                _fut: asyncio.Future[Tuple[bytes, Tuple[str, int]]],
            ) -> None:
                if handle is None or not handle.cancelled():
                    loop.remove_reader(fd)

            SIZE = 4096
            try:
                return sock.recvfrom(SIZE)
            except (BlockingIOError, InterruptedError):
                pass
            loop = asyncio.get_running_loop()
            fut = loop.create_future()
            fd = sock.fileno()

            handle = loop.add_reader(fd, callback=callback)
            fut.add_done_callback(done)
            return await fut  # type:ignore[no-any-return]

    async def _get_hop_ipv4(
        self: "Traceroute", sock: socket.socket, dst_addr: str, src_port: int
    ) -> Hop:
        """
        Get next hop informatio from the raw socket.

        Read the raw socket until the next-hop information
        is revealed.

        Args:
            sock: Socket instance.
            dst_addr: Destination address.
            src_port: Source port.
        """

        def is_matched(msg: bytes) -> bool:
            proto = msg[9]
            if proto != PROTO_ICMP:
                return False
            icmp_type = msg[20]
            if icmp_type not in ACCEPTABLE_ICMP:
                return False
            orig = msg[28:]  # Original header
            orig_proto = orig[9]
            if orig_proto != PROTO_UDP:
                return False  # Not UDP
            orig_dst_ip = f"{orig[16]}.{orig[17]}.{orig[18]}.{orig[19]}"
            if orig_dst_ip != dst_addr:
                return False  # Destination address mismatch
            orig_src_port = (orig[20] << 8) + orig[21]
            if src_port != orig_src_port:
                return False  # Source port mismatch
            orig_dst_port = (orig[22] << 8) + orig[23]
            return self.dst_port == orig_dst_port

        t0 = time.perf_counter_ns()
        while True:
            # Python 3.9-3.10 leak CancelledError here
            try:
                data, (addr, _) = await self._recvfrom(sock)
            except asyncio.CancelledError as e:
                raise TimeoutError from e
            if is_matched(data):
                rtt_ns = time.perf_counter_ns() - t0
                # Resolve AS number
                asn = await self._resolve_as(addr)
                return Hop(
                    addr=addr, rtt=float(rtt_ns) / 1_000_000_000.0, asn=asn
                )

    async def _resolve_as(self: "Traceroute", addr: str) -> int:
        """
        Get AS for IP address.

        Args:
            addr: IP address.

        Returns:
            AS number of `0` if not found.
        """
        if not self._whois:
            return 0
        asn = self._whois_cache.get(addr)
        if asn is None:
            try:
                asn = await self._whois.resolve_as(addr)
            except WhoisError:
                asn = 0
        self._whois_cache[addr] = asn
        return asn
