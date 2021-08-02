import dataclasses
import typing as t
from dataclasses import dataclass

T = t.TypeVar("T")
KT = t.TypeVar("KT")
VT = t.TypeVar("VT")


# @dataclass
# class AA(t.Generic[T, KT]):
#     a: T

# class BB(AA[str, T]):
#     b: str

# class CC(BB[T]):
#     c: int

# print(dataclasses.fields(CC))

class AAA(t.Generic[KT, VT]):
    a1: KT
    a2: VT

class BBB(AAA[KT, VT], t.Generic[VT, KT]):
    b: int



print("Here 1")
class A(t.TypedDict, t.Generic[T, VT], total=False):
    a1: list[list[T]]
    a2: VT


class B(A[KT, int]):
    b: KT

class C(B[str]):
    c: bool

assert(C.__annotations__["a2"] is int)

# print(A[int, t.List[str]].__args__)


# class BB(AA):
#     b: str

# class C(t.TypedDict):
#     c: str

# class D(dict):
#     ...

# print("Here 2")
# E = t.TypedDict("E", { 'e': T }, total=True)

# print("Here 3")
# print(type(B))
# print(A[int].__annotations__)

class E(t.TypedDict):
    e: str

class F(E):
    f: int

assert(all(x in F.__annotations__ for x in ('e', 'f')))