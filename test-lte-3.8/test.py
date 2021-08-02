#! /usr/bin/env python3.6

import typing as t
import typing_extensions as te

T = t.TypeVar("T")
KT = t.TypeVar("KT")
VT = t.TypeVar("VT")

class A(te.TypedDict, t.Generic[T, VT], total=False):
    a1: t.List[t.List[T]]
    a2: VT

class B(A[KT, int]):
    b: KT

class C(B[str]):
    c: bool

assert(all(x in C.__annotations__ for x in ('a1', 'a2', 'b', 'c')))
assert(C.__annotations__['a2'] is int)
assert(x in C.__optional_keys__ for x in ('a1', 'a2'))

E = te.TypedDict("E", { 'e': T }, total=False)

class F(E[str]):
    f: int

assert(all(x in F.__annotations__ for x in ('e', 'f')))
assert(F.__annotations__['e'] is str)
assert('e' in F.__optional_keys__)