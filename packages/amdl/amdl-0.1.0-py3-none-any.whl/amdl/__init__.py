import importlib
import subprocess
import sys
import inspect

def __amdl__(module_name, caller_globals):
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print(f'[+] Module not found: {module_name}')
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            module = importlib.import_module(module_name)
            print(f'[+] Module installed & imported')
        except Exception as e:
            print(f'[-] ERROR: The script failed to restart the project and re-import it.')
            print(f'[-] ERROR-RESPONSE: {e}')
            print(f'[-] PRESS [ENTER] TO CONTINUE (MAYBE CRASH AFTER): ')

    # best method to inject module in the global workspace of the caller
    caller_globals[module_name] = module

def add(modules):
    caller_globals = inspect.stack()[1].frame.f_globals
    for module in modules:
        __amdl__(module, caller_globals)