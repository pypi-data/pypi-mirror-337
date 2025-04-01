from collections.abc import Callable, Iterable
import os
import shutil
import pkgutil
from importlib import util, import_module
from pathlib import Path
from typing import Generator as Gen
import importlib.machinery
from types import ModuleType
from jinja2 import FileSystemLoader
from jinja2 import Environment
from injector_collections.CollectionItem import CollectionItem
import injector_collections
from injector_collections.constants import (
    generatedCollectionsModuleName,
    collectionTemplateFilename,
)

class Generator:
    def generate(
        self,
        inject: Callable,
        collectionModule: str,
        scannedModules: Iterable[str]
    ):
        collectionModuleDirectory = self.getModuleDirectory(collectionModule)

        generatedDirPath = f'{collectionModuleDirectory}/{generatedCollectionsModuleName}'
        shutil.rmtree(generatedDirPath, ignore_errors=True)
        os.makedirs(generatedDirPath, exist_ok=True)

        Path(f'{generatedDirPath}/__init__.py').touch()

        collectionMetadata = self.gatherCollectionMetadata(scannedModules)

        # create each collection in a seperate '<CollectionName>.py' file
        for collectionType, collectionItems in collectionMetadata.items():
            generatedFilePath = f'{generatedDirPath}/{collectionType.__name__}.py'
            with open(generatedFilePath, 'w', encoding='utf-8') as f:
                f.write(self.renderCollectionTemplate(
                    inject,
                    collectionType,
                    collectionItems))

    def getModuleDirectory(self, module: str|ModuleType) -> str:
        if isinstance(module, str):
            moduleSpec = util.find_spec(module)
            assert moduleSpec is not None
            modulePath = moduleSpec.origin
        else:
            modulePath = module.__file__
        assert modulePath is not None
        return os.path.dirname(modulePath)

    def getModuleName(self, module: str|ModuleType) -> str:
        if isinstance(module, str):
            return module

        return module.__name__

    def renderCollectionTemplate(
            self,
            inject: Callable,
            collection: type,
            collectionItems: list[CollectionItem]):
        icModuleDirectory = self.getModuleDirectory(injector_collections)
        file_loader = FileSystemLoader(f'{icModuleDirectory}')
        env = Environment(loader=file_loader)
        template = env.get_template(collectionTemplateFilename)
        return template.render(
            collection = collection,
            collectionItems = collectionItems,
            inject = inject
        )

    def gatherCollectionMetadata(
            self,
            scannedModules: Iterable[str],
            ) -> dict[type, list[CollectionItem]]:
        ''' Gather Metadata for Collection generation with template

        Recursively walks through all modules in 'scannedModules' and gathers
        metadata for every class decorated with '@CollectionItem'.
        '''
        for m in scannedModules:
            for spec in self.walkModules(m):
                if spec.origin is not None:
                    with open(spec.origin, 'r', encoding='utf-8') as f:
                        if '@CollectionItem' in f.read():
                            import_module(spec.name)

        return CollectionItem.getItems()

    def walkModules(self, rootModule: str) -> Gen[importlib.machinery.ModuleSpec, None, None]:
        if (info := util.find_spec(rootModule)) is None:
            return

        yield info

        if info.submodule_search_locations is None:
            return

        for modinfo in pkgutil.iter_modules(info.submodule_search_locations):
            name = f'{info.name}.{modinfo.name}'

            if (spec := util.find_spec(name)) is not None:
                yield spec

            submods = self.walkModules(name)
            next(submods, None) # remove the root, which was just yielded
            yield from submods
