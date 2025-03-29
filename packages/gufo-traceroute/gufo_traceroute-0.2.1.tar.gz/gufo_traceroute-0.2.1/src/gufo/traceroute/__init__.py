# ---------------------------------------------------------------------
# Gufo Traceroute: Python Traceroute Library
# ---------------------------------------------------------------------
# Copyright (C) 2022-25, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""
Python asyncio traceroute library.

Attributes:
    __version__: Current version.
"""

from .traceroute import Hop, HopInfo, Traceroute

__version__: str = "0.2.1"
__all__ = ["Hop", "HopInfo", "Traceroute", "__version__"]
