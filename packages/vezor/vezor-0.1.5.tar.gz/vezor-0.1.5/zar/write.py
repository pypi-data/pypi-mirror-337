import inspect
from . import __submodule__

class CodeWriter:
    def writeFunctionCode(self, function_name):
        for submodule_name, module in __submodule__.items():
            try:
                func = getattr(module, function_name, None)
                if func and inspect.isfunction(func):
                    code = inspect.getsource(func)
                    file_path = inspect.getfile(module)

                    with open(file_path, "r+", encoding="utf-8") as file:
                        content = file.read()
                        if code not in content:
                            file.write(f"\n\n{code}")
                            print(f"{function_name} added to {file_path}")
                        else:
                            print(f"{function_name} already exists in {file_path}")
                    return
            except ModuleNotFoundError:
                pass

        print(f"{function_name} not found in zar package.")

    def __getattr__(self, name):
        return lambda: self.writeFunctionCode(name)

algoWrite = CodeWriter()
