import importlib

modules = ["bubble_sort", "quick_sort", "linear_search"]
__all__ = []

for module in modules:
    imported_module = importlib.import_module(f".{module}", package=__name__)
    globals()[module] = imported_module
    __all__.append(module)
