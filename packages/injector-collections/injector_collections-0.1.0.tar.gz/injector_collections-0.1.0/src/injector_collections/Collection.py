import importlib
from injector import inject, Injector

class CollectionException(Exception):
    pass

class Collection[T]:
    @inject
    def __init__(self, injector: Injector):
        self.injector = injector
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
        _class = next(iter(cls.__subclasses__()), cls)

        # get everything before "collections" in module path and append "generated"
        # also append the generated collections module name
        module_path_parts = _class.__module__.split(".")
        last_index = len(module_path_parts) - 1 - module_path_parts[::-1].index("collections")
        generatedModulesPath = ".".join(module_path_parts[:last_index]) + ".generated"
        return f"{generatedModulesPath}.{cls.getCollectionName()}"

    def _getGeneratedCollection(self):
        if self.injector is None:
            raise CollectionException("injector must be set for class Collection.")

        if self._generatedCollection is None:
            module = importlib.import_module(self.getGeneratedModulePath())
            _class = getattr(module, self.getCollectionName())
            self._generatedCollection = self.injector.get(_class)

        return self._generatedCollection
