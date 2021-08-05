#! /usr/bin/env python3.9

import typing as t

T = t.TypeVar("T")
KT = t.TypeVar("KT")
VT = t.TypeVar("VT")

class A(t.TypedDict, t.Generic[T, VT], total=False):
    a1: t.List[t.List[T]]
    a2: VT

assert(A[int, str].__annotations__["a2"] is str)

class B(A[KT, int]):
    b: KT

assert(B.__annotations__["a2"] is int)

class C(B[str]):
    c: bool

assert(all(x in C.__annotations__ for x in ('a1', 'a2', 'b', 'c')))
assert(C.__annotations__['a2'] is int)
assert(x in C.__optional_keys__ for x in ('a1', 'a2'))

E = t.TypedDict("E", { 'e': T }, total=False)

class F(E[str]):
    f: int

assert(all(x in F.__annotations__ for x in ('e', 'f')))
assert(F.__annotations__['e'] is str)
assert('e' in F.__optional_keys__)

class G(t.TypedDict):
    g: str

class H(G):
    h: int

assert(x in H.__annotations__ for x in ('g', 'h'))