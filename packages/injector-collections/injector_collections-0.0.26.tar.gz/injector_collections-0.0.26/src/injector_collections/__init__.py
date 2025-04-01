from typing import Callable, Iterable
from injector_collections.Generator import Generator
from injector_collections.Collection import Collection
from injector_collections.CollectionItem import CollectionItem

GENERATING_INJECTOR_COLLECTIONS = False

def generateCollections(
        inject: Callable,
        collectionModule: str,
        scannedModules: Iterable[str]):
    global GENERATING_INJECTOR_COLLECTIONS
    GENERATING_INJECTOR_COLLECTIONS = True
    generator = Generator()
    generator.generate(inject, collectionModule, scannedModules)
