from collections.abc import Callable, Iterable
from injector_collections.Generator import Generator

GENERATING_INJECTOR_COLLECTIONS = False

def generateCollections(
        inject: Callable,
        collectionModule: str,
        scannedModules: Iterable[str]):
    global GENERATING_INJECTOR_COLLECTIONS
    GENERATING_INJECTOR_COLLECTIONS = True
    generator = Generator()
    generator.generate(inject, collectionModule, scannedModules)
