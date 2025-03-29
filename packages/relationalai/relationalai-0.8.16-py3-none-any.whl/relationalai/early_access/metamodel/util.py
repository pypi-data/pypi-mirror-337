from __future__ import annotations
from typing import Callable, Generic, IO, Iterable, Optional, Sequence, Tuple, TypeVar
import copy
from dataclasses import dataclass, field

#--------------------------------------------------
# FrozenOrderedSet
#--------------------------------------------------

T = TypeVar('T')
class FrozenOrderedSet(Generic[T]):
    """ Immutable access to an ordered sequence of elements without duplicates. """

    def __init__(self, data:Sequence[T]):
        # TODO - maybe verify that there are no duplicates?
        self.data = tuple(data)

    @classmethod
    def from_iterable(cls, items:Iterable[T]|None):
        return OrderedSet.from_iterable(items).frozen()

    def some(self) -> T:
        assert len(self.data) > 0
        return self.data[0]

    def __hash__(self) -> int:
        return hash(self.data)

    def __eq__(self, other):
        if not isinstance(other, FrozenOrderedSet):
            return False
        return self.data == other.data

    def __getitem__(self, ix):
        if len(self.data) <= ix:
            return None
        return self.data[ix]

    def __contains__(self, item:T):
        return item in self.data

    def __bool__(self):
        return bool(self.data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __sub__(self, other:Iterable[T]) -> FrozenOrderedSet[T]:
        # set difference guaranteeing deterministic order
        new = OrderedSet()
        new.update(self.data)
        for item in other:
            new.remove(item)
        return new.frozen()

    def __str__(self) -> str:
        return self.data.__str__()

#--------------------------------------------------
# OrderedSet
#--------------------------------------------------

T = TypeVar('T')
class OrderedSet(Generic[T]):
    def __init__(self):
        self.set = set()
        self.list:list[T] = []

    @classmethod
    def from_iterable(cls, items:Iterable[T]|None):
        s = OrderedSet()
        s.update(items)
        return s

    def add(self, item:T|None):
        if item is not None and item not in self.set:
            self.set.add(item)
            self.list.append(item)

    def update(self, items:Iterable[T]|None):
        if items is not None:
            for item in items:
                self.add(item)

    def remove(self, item:T):
        if item in self.set:
            self.set.remove(item)
            # list.remove uses == under the covers, which screws
            # with our DSL objects that have __eq__ defined and
            # return expressions, so we need to do this manually
            new_list = []
            for cur in self.list:
                if cur is not item:
                    new_list.append(cur)
            self.list = new_list

    def clear(self):
        self.set.clear()
        self.list.clear()

    def some(self) -> T:
        assert len(self.list) > 0
        return self.list[0]

    def frozen(self) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet(self.list)

    def __hash__(self) -> int:
        return hash((tuple(self.list)))

    def __contains__(self, item:T):
        return item in self.set

    def __bool__(self):
        return bool(self.set)

    def __getitem__(self, ix) -> T:
        if ix >= len(self.list):
            raise IndexError
        return self.list[ix]

    def __iter__(self):
        return iter(self.list)

    def __len__(self):
        return len(self.list)

    def __sub__(self, other:Iterable[T]) -> OrderedSet[T]:
        # set difference guaranteeing deterministic order
        new = copy.copy(self)
        for item in other:
            new.remove(item)
        return new

    def __str__(self) -> str:
        return self.list.__str__()


T = TypeVar('T')
def ordered_set(*items: T) -> OrderedSet[T]:
    """ Create an OrderedSet with these items. """
    s = OrderedSet()
    if items is not None:
        s.update(items)
    return s

def frozen(*items: T) -> FrozenOrderedSet[T]:
    """ Create a FrozenOrderedSet with these items."""
    return FrozenOrderedSet(items)

V = TypeVar('V')
K = TypeVar('K')
def index_by(s: Iterable[V], f:Callable[[V], K]) -> dict[K, V]:
    """ Create an index for the sequence by computing a key for each value using this function. """
    d = dict()
    for v in s:
        d[f(v)] = v
    return d

V = TypeVar('V')
K = TypeVar('K')
def group_by(s: Iterable[V], f:Callable[[V], K]) -> dict[K, OrderedSet[V]]:
    """ Group elements of the sequence by a key computed for each value using this function. """
    d = dict()
    for v in s:
        key = f(v)
        if key not in d:
            d[key] = OrderedSet()
        d[key].add(v)
    return d

def split_by(s: Iterable[V], f:Callable[[V], bool]) -> Tuple[list[V], list[V]]:
    """ Split the iterable in 2 groups depending on the result of the callable: [True, False]."""
    trues = []
    falses = []
    for v in s:
        trues.append(v) if f(v) else falses.append(v)
    return (trues, falses)

def filter_by_type(s: Iterable[V], types)-> list[V]:
    """ Filter the iterable keeping only elements of these types. """
    r = []
    for v in s:
        if isinstance(v, types):
            r.append(v)
    return r

@dataclass(frozen=True)
class NameCache():
    # support to generate object names with a count when there's collision
    # the next count to use as a suffix for an object with this name
    name_next_count: dict[str, int] = field(default_factory=dict)
    # cache of precomputed names for the object with this id
    name_cache: dict[int, str] =  field(default_factory=dict)

    def get_name(self, id: int, name: str) -> str:
        """ Get the name to use for the object with this id and name, avoiding name collisions. """
        if id in self.name_cache:
            return self.name_cache[id]

        if name in self.name_next_count:
            c = self.name_next_count[name]
            self.name_next_count[name] = c + 1
            name = f"{name}_{c}"
        else:
            self.name_next_count[name] = 2
            name = f"{name}"

        self.name_cache[id] = name
        return name

@dataclass(frozen=True)
class Printer():
    """ Helper class to print ASTs into an IO object. """
    io: Optional[IO[str]] = None

    def _nl(self) -> None:
        """ Print a new line character. """
        self._print("\n")

    def _print(self, arg) -> None:
        """ Print the argument into the io without indentation. """
        if self.io is None:
            print(arg, end='')
        else:
            self.io.write(arg)

    def _indent_print(self, depth, arg) -> None:
        """ Print the argument into the io with indentation based on depth. """
        if self.io is None:
            print("    " * depth + str(arg), end='')
        else:
            self.io.write("    " * depth + str(arg))

    def _indent_print_nl(self, depth, arg) -> None:
        """ Helper for the common case of calling _indent_print followed by _nl. """
        self._indent_print(depth, arg)
        self._nl()
