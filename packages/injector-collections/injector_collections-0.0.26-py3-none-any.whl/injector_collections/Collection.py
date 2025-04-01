import importlib

class CollectionException(Exception):
    pass

class Collection[T]:
    def __init__(self):
        self._generatedCollection = None

    @property
    def items(self) -> dict[type[T], T]:
        return self._getGeneratedCollection().items

    def __contains__(self, key):
        return key in self.items

    def __getitem__(self, key) -> T:
        return self.items[key]

    def __setitem__(self, key, item: T):
        self.items[key] = item

    @property
    def byClassname(self) -> dict[str, T]:
        return self._getGeneratedCollection().byClassname

    @classmethod
    def getCollectionName(cls) -> str:
        # Get the name of the first derived subclass
        for subclass in cls.__subclasses__():
            return subclass.__name__
        return cls.__name__  # return the own name if no child exists

    @classmethod
    def getGeneratedModulePath(cls) -> str:
        if not (subclasses := cls.__subclasses__()):
            raise CollectionException("Collection cannot be used directly.")

        # get everything before "collections" in module path and append "generated"
        # also append the generated collections module name
        module_path_parts = subclasses[0].__module__.split(".")
        last_index = len(module_path_parts) - 1 - module_path_parts[::-1].index("collections")
        generatedModulesPath = ".".join(module_path_parts[:last_index]) + ".generated"
        return f"{generatedModulesPath}.generated.{cls.getCollectionName()}"

    def _getGeneratedCollection(self):
        if self._generatedCollection is None:
            module = importlib.import_module(self.getGeneratedModulePath())
            self._generatedCollection = getattr(module, self.getCollectionName())

        return self._generatedCollection
