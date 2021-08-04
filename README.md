# My notes while drafting a [PEP](https://www.python.org/dev/peps/)

The PR that started my journey through this rabbit hole:
<https://github.com/microsoft/pyright/pull/1390>

Advice in typing-sig mailing list with a sketch on how to move forward
with a PEP:
<https://mail.python.org/archives/list/typing-sig@python.org/thread/GKKSWMONVHRLFI4NJAT36RPZCGGIBJ3G/>

# Goal

To extend `typing.TypedDict` [PEP 589](https://www.python.org/dev/peps/pep-0589/)
with generic value support. At the moment `TypedDict` is a special type
that is not paramterizable. We need to add runtime support for it
through `stdlib` and provide a type consistency specification for type
checkers.

``` python
from typing import TypedDict, TypeVar, Generic
T = TypeVar("T")

class TD(Generic[T], TypedDict):
    f1: List[T]

def test_td(aa: TD[T], bb: TD[T]):
    return aa["f1"], bb["f1"]

td1 = test_td({"f1": ["foo"]}, {"f1": ["bar"]})
reveal_type(td1) # info: Type of "td1" is "tuple[List[str], List[str]]"
```

# TODO

As sketched out by David Foster in typing-sig.

- [-] Draft a PEP
- [ ] Get reviewed in typing-sig, get soft approval
- [ ] Implementations
- [ ] Get the PEP approved

# Implementations
- [-] Generic `TypedDict` in `typing.py`
    - [x] [Patch](https://github.com/python/cpython/compare/3.9...sransara:py-generic-typeddict) typing.py for versions >= 3.9
    - [ ] Integrate to test suite
- [-] Generic `TypedDict` runtime in `typing_extensions`
    - [x] [Patch](https://github.com/python/typing/compare/master...sransara:py-generic-typeddict) typing_extensions.py for versions < 3.9.2
    - [ ] Integrate to test suite
- [-] Generic `TypedDict` in one of the type checkers ([pyright](https://github.com/microsoft/pyright/))
    - [x] [Patch](https://github.com/microsoft/pyright/compare/main...sransara:generic-typed-dict) to Pyright ([PR](https://github.com/microsoft/pyright/pull/1390)).
    - [ ] Rebase the PR on to a current version
    - [ ] Support for declaring with TypedDict constructor notation
    - [ ] Adding proper test cases to the automated test suite
    