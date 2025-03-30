import importlib

modules = {
    "print": ["algoPrint"],
    "write": ["algoWrite"]
}
submodules = ["sorting"]

__all__ = []
__submodule__ = []

for module, symbols in modules.items():
    imported_module = importlib.import_module(f".{module}", package=__name__)
    globals()[module] = imported_module

    for symbol in symbols:
        globals()[symbol] = getattr(imported_module, symbol)
        __all__.append(symbol)

for submodule in submodules:
    imported_submodule = importlib.import_module(f".{submodule}", package=__name__)
    globals()[submodule] = imported_submodule
    __submodule__.append(submodule)
