# Initial notes

-   I’m expecting this will be a mishmash of ideas from different
    concepts that we already have class based syntax already has Generic
    support. But the assignment syntax may need to be more explored. It
    will be similar to how we declare Generic aliases (Guido had
    mentioned [here](https://github.com/python/mypy/issues/3863)).

-   Type consistency especially regarding structural subtyping will need
    to be carefully explored. I assume this will be similar to how we do
    Protocols with Generics.

-   After some investigation I noticed run time support for TypedDict
    before PEP 560 will need some metaclass hacks due to metaclass
    conflicts. But after version 3.7 with PEP 560 it seems simpler.

# Abstract

PEP 589 introduces a type constructor `TypedDict` to support the use
case where a dictionary object has a specific set of string keys, each
with a value of a specific type. But it does not specify the details
of supporting generic TypedDicts. This PEP specifies the details of a
type parameterized TypedDicts as an extension of PEP 589.

# Motivation

TypedDict is a container data type. Almost all container data types of
the standard library support generics. TypedDicts should also support
generics.

With the addition of PEP 560, users can define generic TypedDict without
the need for adhoc metaclass hacks.

Following is an example where we can use type annotations to convey
relationships between keys.

```
class Page(TypedDict, Generic[T]):
    uid: Hash[T]
    desc: str
    item: T
```

Here is an example where the function on container type does not concern
with the concrete type of the contents.

```
def get_items(*pages: Page[T]) -> List[T]:
    return [page["item"] for page in pages]
```

Another usage example in annotating polymorphic JSON responses.

```
class Item(TypedDict):
    type: str

class ValueItem(Item):
    value: int

T = TypeVar('T')

class ItemPager(TypedDict, Generic[T]):
    next_page: Optional[str]
    items: List[T]

def get_value_items() -> List[ValueItem]:
    value_items: List[ValueItem] = []
    url = "https://example.com/value_items"
    while url:
        response = requests.get(url)
        pager: ItemPager[ValueItem] = response.json()
        url = pager['next_page']
        value_items += pager['items']
    return value_items
```

# Specification

This PEP is an extension of PEP 589, hence details specified here for
TypedDicts will be in addition to what is specified in PEP 589.

## Class based syntax

Class based syntax for TypedDicts will follow the same specification as
user defined generic types in PEP 484 and class based syntax
specification detailed in PEP 589.

````
from typing import TypedDict

T = TypeVar("T")

class Pager(TypedDict, Generic[T]):
    next_page: str
    items: List[T]
```

`Generic[T]` as a base class defines that the class `Pager` takes a
single type parameter `T`. `Pager[int]` is a TypedDict that has a key
`items` with value type `List[int]`.

## Alternative syntax

The following alternative syntax is semantically equivalent to the
previous class based syntax example. Order of Generic subscript TypeVars
will be in the order of their appearance.

```
from typing import TypedDict

T = TypeVar("T")

Pager = TypedDict("Pager", {
    'next_page': str,
    'items': List[T],
})
```

## Inheritance

A TypedDict can only inherit from another TypedDict or TypedDict with
Generic. This is in contrast to PEP 589, which specifies that a
TypedDict can only inherit from a TypedDict.

Subclassing a generic TypedDict without specifying type parameters
assumes `Any` for each position.

All other details of TypedDict inheritance from PEP 589 applies.

## Using generic TypedDict types

Here is an example of how the type `Pager` can be used.

```
pager: Pager[str] = {
    'next_page': 'https://example.com/value_items?p=2',
    'items': ['item 1', 'item2',]
}
```

If the type parameter is not specified, type checker can follow the same
behavior as how it treats other generic instances without a type
parameter.

## Type consistency

Same type consistency rules from PEP 589 applies.

Since TypedDict objects are mutable, value types should behave
invariantly. Therefore at declaration a type checker should only accept
invariant TypeVars.

```
from typing import TypedDict

T = TypeVar("T", covariant=True)

class Page(TypedDict, Generic[T]): # Covariant T should not be allowed
    item: T

def set_item(p: Page[Animal]):
    p["item"] = Animal()

page: Page[Dog] = Page(item=Dog())
set_item(page)
page["item"].bark() # Run time error
```