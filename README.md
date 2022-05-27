# An attempt to add generic support for TypedDict

# Goal

To extend `typing.TypedDict` [PEP 589](https://www.python.org/dev/peps/pep-0589/)
with generic value support. At the moment `TypedDict` is a special type
that is not paramterizable. We need to add runtime support for it
through `stdlib` and provide a type consistency specification for type
checkers.

```python
from typing import TypedDict, TypeVar, Generic
T = TypeVar("T")

class TD(Generic[T], TypedDict):
    f1: List[T]

def test_td(aa: TD[T], bb: TD[T]):
    return aa["f1"], bb["f1"]

td1 = test_td({"f1": ["foo"]}, {"f1": ["bar"]})
reveal_type(td1) # info: Type of "td1" is "tuple[List[str], List[str]]"
```

# Timeline

Jan 19 2021:

- Opened [PR in pyright](https://github.com/microsoft/pyright/pull/1390)
- Requested by maintainers to get approval through the typing-sig or PEP drafting process
- Send out [email to typing-sig](https://mail.python.org/archives/list/typing-sig@python.org/thread/GKKSWMONVHRLFI4NJAT36RPZCGGIBJ3G/)

Jan 24 2021:

- [Advice in typing-sig mailing list](https://mail.python.org/archives/list/typing-sig@python.org/thread/GKKSWMONVHRLFI4NJAT36RPZCGGIBJ3G/)
  with a sketch on how to move forward with a PEP

...

Aug 1 2021:

- [PEP ready for review](pep-9999.rst)
- Prototype [patch](https://github.com/python/cpython/compare/main...sransara:py-generic-typeddict) for typing.py
- Prototype [patch](https://github.com/python/typing/compare/master...sransara:py-generic-typeddict) for typing_extensions.py

Aug 4 2021:

- Send out [email to typing-sig](https://mail.python.org/archives/list/typing-sig@python.org/thread/JIG63TRUTF7NSDRGUMI3GHRK3J564CUI/)
  for comments

Aug 6 2021:

- Foward references are proving to be an issue with the current alternative syntax spec,
  because `_collect_type_vars` can't look inside ForwardRef.
- Considering that annotations are not meant for run time,
  the two previous patches which try to resolve generic params may be too complicated.
- Create new [patch](https://github.com/python/cpython/compare/main...sransara:py-generic-typeddict-simple) for typing.py

Aug 7 2021:

- Create [issue in bugs.python.org](https://bugs.python.org/issue44863) and [cpython pull request](https://github.com/python/cpython/pull/27663)

Sep 1st week 2021:

- Including @uriyyo's suggestions in simplifying the implementaion and test cases
- Including @sobolevn suggested test case which found a bug
- Addressing @Fidget-Spinner's concerns
- Pending issue on whether to proxy the dunders like `__total__` through the GenericAlias

  ```python
  class A(TypedDict, Generic[T]):
    foo: T

  assert(A[str].__required_keys__  == frozenset(['foo']) # Raises Attribute error
  assert(A[str].__origin__.__required_keys__  == frozenset(['foo']) # Works
  ```

  Current personal decision to not proxy dunder attributes because:

  ```python
  class A(Generic[T]):
    a: T

  print(A.__annotations__) # {'a': ~T}
  print(A[str].__annotations__) # raises AttributeError
  print(A[str].__origin__.__annotations__) # {'a': ~T}
  ```

- Found a bug in the upstream implementation. Non generic TypedDicts are subscriptable.
  Not sure if this should be fixed in this PR by overriding `__getitem__`

  ```python
  class G(TypedDict):
    g: str

  print(G[int]) # G is subscriptable although not a Generic
  ```

8 Sep 2021:

- Email sent to typing-sig mailing list: [Viability of letting TypedDict classes inherit from Generic without a PEP change](https://mail.python.org/archives/list/typing-sig@python.org/thread/I7P3ER2NH7SENVMIXK74U6L4Z5JDLQGZ/)

# TODO

As sketched out by David Foster in typing-sig.

- [ ] Draft a PEP
- [ ] Get reviewed in typing-sig, get soft approval
- [ ] Implementations
- [ ] Get the PEP approved

# Implementations

- [ ] Generic `TypedDict` in `typing.py`
  - [x] Simple [patch](https://github.com/python/cpython/compare/main...sransara:py-generic-typeddict-simple) that allows inherit from Generic
    - [x] Integrate to test suite
  - [x] [Patch with resolving annotation](https://github.com/python/cpython/compare/3.9...sransara:py-generic-typeddict)
    - [ ] Integrate to test suite
- [ ] Generic `TypedDict` runtime in `typing_extensions`
  - [x] [Patch](https://github.com/python/typing/compare/master...sransara:py-generic-typeddict) typing_extensions.py
  - [ ] Integrate to test suite
- [ ] Generic `TypedDict` in one of the type checkers ([pyright](https://github.com/microsoft/pyright/))
  - [x] [Patch](https://github.com/microsoft/pyright/compare/main...sransara:generic-typed-dict) to Pyright ([PR](https://github.com/microsoft/pyright/pull/1390)).
  - [ ] Rebase the PR on to a current version
  - [ ] Support for declaring with TypedDict constructor notation
  - [ ] Adding proper test cases to the automated test suite
