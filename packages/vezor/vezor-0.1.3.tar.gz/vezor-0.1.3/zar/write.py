import inspect
import importlib
from . import __submodule__

class CodeWriter:
    def writeClassCode(self, class_name):
        for submodule in __submodule__:
            try:
                module = importlib.import_module(f"zar.{submodule}")
                cls = getattr(module, class_name, None)
                if cls and inspect.isclass(cls):
                    code = inspect.getsource(cls)
                    file_path = inspect.getfile(module)

                    with open(file_path, "r+", encoding="utf-8") as file:
                        content = file.read()
                        if code not in content:
                            file.write(f"\n\n{code}")
                            print(f"{class_name} added to {file_path}")
                        else:
                            print(f"{class_name} already exists in {file_path}")
                    return
            except ModuleNotFoundError:
                pass

        print(f"{class_name} not found in zar package.")

    def __getattr__(self, name):
        return lambda: self.writeClassCode(name)

algoWrite = CodeWriter()
