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

If we want to support versions before 3.7, this syntax would be better
because we can hide the workaround for metaclass conflicts.