# ----------------------------------------------------------------------
# Gufo Traceroute: tests
# ----------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# See LICENSE.md for details
# ----------------------------------------------------------------------

# Python modules
import asyncio
import socket
from typing import List

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.traceroute import HopInfo, Traceroute


def _check_permissions() -> bool:
    try:
        socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        return True
    except PermissionError:
        return False


HAS_PERMISSIONS = _check_permissions()


@pytest.mark.skipif(not HAS_PERMISSIONS, reason="Permission denied")
def test_traceroute_ipv4() -> None:
    async def inner() -> List[HopInfo]:
        hops = []
        async with Traceroute() as tr:
            async for hop in tr.traceroute("127.0.0.1", tries=3):
                hops.append(hop)
        return hops

    r = asyncio.run(inner())
    assert len(r) == 1
    assert r[0].ttl == 1
    assert len(r[0].hops) == 3
    for hop in r[0].hops:
        assert hop
        assert hop.addr == "127.0.0.1"


@pytest.mark.skipif(not HAS_PERMISSIONS, reason="Permission denied")
def test_traceroute_ipv6() -> None:
    async def inner() -> List[HopInfo]:
        hops = []
        async with Traceroute() as tr:
            async for hop in tr.traceroute("::1", tries=3):
                hops.append(hop)
        return hops

    with pytest.raises(NotImplementedError):
        asyncio.run(inner())


@pytest.mark.skipif(not HAS_PERMISSIONS, reason="Permission denied")
def test_tos() -> None:
    async def inner() -> None:
        async with Traceroute(tos=1) as tr:
            async for _ in tr.traceroute("127.0.0.1", tries=3):
                break

    asyncio.run(inner())
