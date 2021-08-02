import typing as t
import typing_extensions as te
from pprint import pprint
import sys

T = t.TypeVar("T")
KT = t.TypeVar("KT")
VT = t.TypeVar("VT")

print("Here 1")
class A(te.TypedDict, t.Generic[T, VT], total=False):
    a1: t.List[t.List[T]]
    a2: VT

class B(A[KT, int]):
    b: KT

print("+"*100)
class C(B[str]):
    c: bool


pprint(C.__dict__)
sys.exit(1)

print("Here 2")
E = te.TypedDict("E", { 'e': T }, total=True)

print(E.__annotations__)
print(E.__total__)