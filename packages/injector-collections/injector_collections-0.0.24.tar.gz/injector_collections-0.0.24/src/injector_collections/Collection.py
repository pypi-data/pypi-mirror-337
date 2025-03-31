from typing import Any

class Collection[T]:
    def __init__(self):
        self._items: dict[type[T], T] = {}
        self._byClassname: dict[str, T] = {}

    @property
    def items(self) -> dict[type[T], T]:
        return self._items

    def __contains__(self, key):
        return key in self._items

    def __getitem__(self, key) -> T:
        return self._items[key]

    def __setitem__(self, key, item: T):
        self._items[key] = item

    @property
    def byClassname(self) -> dict[str, T]:
        return self._byClassname

    @classmethod
    def getItemType(cls) -> type[T]:
        return Any
