# ---------------------------------------------------------------------
# Gufo Traceroute: BPF primitives test
# ---------------------------------------------------------------------
# Copyright (C) 2022-23, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from typing import List

# Third-party modules
import pytest

# Gufo Labs modules
from gufo.traceroute.bpf import (
    Op,
    ja,
    jeq,
    jne,
    ld,
    ldb,
    ldh,
    preprocess_bpf,
    ret,
)


def test_compile_jt_fail() -> None:
    op = Op(0, "test", 0, 0)
    with pytest.raises(ValueError):
        op.encode()


def test_compile_jf_fail() -> None:
    op = Op(0, 0, "test", 0)
    with pytest.raises(ValueError):
        op.encode()


def test_compile_k_fail() -> None:
    op = Op(0, 0, 0, "test")
    with pytest.raises(ValueError):
        op.encode()


def test_backref() -> None:
    prog = [ldb(10, label="start"), ja("start")]
    with pytest.raises(ValueError):
        preprocess_bpf(prog)


@pytest.mark.parametrize(
    ("op", "exp"),
    [
        (ldb(20), Op(0x30, 0, 0, 20)),
        (ldh(30), Op(0x28, 0, 0, 30)),
        (ld(28), Op(0x20, 0, 0, 28)),
    ],
)
def test_op(op: Op, exp: Op) -> None:
    assert op == exp


@pytest.mark.parametrize(
    ("prog", "exp"),
    [
        (
            [
                Op(0x30, 0, 0, 0x00000014),  # ldb [20]
                Op(0x15, 0, "drop", 11),  # jne 11, drop
                Op(0x20, 0, 0, 0x0000001C),  # ld [28]
                Op(0x15, 0, "drop", 0x01020304),  # jne #sig1, drop
                Op(0x20, 0, 0, 0x00000020),  # ld [32]
                Op(0x15, 0, "drop", 0x05060708),  # jne #sig2, drop
                Op(0x06, 0, 0, 0xFFFFFFFF),  # ret #-1
                Op(0x06, 0, 0, 0, label="drop"),  # ret #0
            ],
            [
                Op(code=0x30, jt=0, jf=0, k=20),
                Op(code=0x15, jt=0, jf=5, k=11),
                Op(code=0x20, jt=0, jf=0, k=28),
                Op(code=0x15, jt=0, jf=3, k=0x01020304),
                Op(code=0x20, jt=0, jf=0, k=32),
                Op(code=0x15, jt=0, jf=1, k=0x05060708),
                Op(code=0x06, jt=0, jf=0, k=0xFFFFFFFF),
                Op(code=0x06, jt=0, jf=0, k=0, label="drop"),
            ],
        ),
        (
            [
                ldb(20),
                jne(11, "drop"),
                ld(28),
                jne(0x01020304, "drop"),
                ld(32),
                jne(0x05060708, "drop"),
                ret(0xFFFFFFFF),
                ret(0, label="drop"),
            ],
            [
                Op(code=0x30, jt=0, jf=0, k=20),
                Op(code=0x15, jt=0, jf=5, k=11),
                Op(code=0x20, jt=0, jf=0, k=28),
                Op(code=0x15, jt=0, jf=3, k=0x01020304),
                Op(code=0x20, jt=0, jf=0, k=32),
                Op(code=0x15, jt=0, jf=1, k=0x05060708),
                Op(code=0x06, jt=0, jf=0, k=0xFFFFFFFF),
                Op(code=0x06, jt=0, jf=0, k=0, label="drop"),
            ],
        ),
        (
            [
                ldh(12),
                jeq(0x800, "accept", "drop"),
                ret(0xFFFFFFFF, label="accept"),
                ret(0, label="drop"),
            ],
            [
                Op(code=40, jt=0, jf=0, k=12),
                Op(code=21, jt=0, jf=1, k=0x800),
                Op(code=6, jt=0, jf=0, k=0xFFFFFFFF, label="accept"),
                Op(code=6, jt=0, jf=0, k=0, label="drop"),
            ],
        ),
        (
            [
                ldh(12),
                jne(0x800, "accept", "drop"),
                ret(0xFFFFFFFF, label="accept"),
                ret(0, label="drop"),
            ],
            [
                Op(code=40, jt=0, jf=0, k=12),
                Op(code=21, jt=1, jf=0, k=0x800),
                Op(code=6, jt=0, jf=0, k=0xFFFFFFFF, label="accept"),
                Op(code=6, jt=0, jf=0, k=0, label="drop"),
            ],
        ),
        (
            [
                ja("drop"),
                ldh(12),
                ret(0xFFFFFFFF, label="accept"),
                ret(0, label="drop"),
            ],
            [
                Op(code=5, jt=0, jf=0, k=2),
                Op(code=40, jt=0, jf=0, k=12),
                Op(code=6, jt=0, jf=0, k=0xFFFFFFFF, label="accept"),
                Op(code=6, jt=0, jf=0, k=0, label="drop"),
            ],
        ),
    ],
)
def test_preprocess_bpf(prog: List[Op], exp: List[Op]) -> None:
    r = preprocess_bpf(prog)
    assert r == exp
