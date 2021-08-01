# 2021/02/04
I’m expecting this will be a mishmash of ideas from different
concepts that we already have class based syntax already has Generic
support. But the assignment syntax may need to be more explored. It
will be similar to how we declare Generic aliases (Guido had
mentioned [here](https://github.com/python/mypy/issues/3863)).

Type consistency especially regarding structural subtyping will need
to be carefully explored. I assume this will be similar to how we do
Protocols with Generics.

After some investigation I noticed run time support for TypedDict
before PEP 560 will need some metaclass hacks due to metaclass
conflicts. But after version 3.7 with PEP 560 it seems simpler.

# 2021/07/31
Current PEP draft is to define class based generic TypedDict like:

```
class Page(TypedDict, Generic[T]):
    ...
```

Another option that could be better is to define just as 
how Generic protocols are defined:

```
class Page(TypedDict[T]):
    ...
```

# 2021/08/01
For versions lower than Python3.7, we have to use typing_extensions
and to get that backward compatiblity support and handle metaclass conflicts
we can have something like. But haven't tried it yet on typing_extensions.

```
from typing import *

T = TypeVar("T")


class LibraryMeta(type):
    ...

class AdHocMeta(GenericMeta, LibraryMeta):
    ...

class LibraryBase(metaclass=AdHocMeta):
    ...

class UserClass(LibraryBase, Generic[T]):
    ...
```