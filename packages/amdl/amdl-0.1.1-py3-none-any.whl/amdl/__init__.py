import importlib, subprocess, sys, inspect, platform, os

# Clear the terminal to enable color printing
os.system('cls' if os.name == 'nt' else 'clear')

# ANSI colors
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

def colored_print(color, text):
    print(f"{color}{text}{RESET}")

def __amdl__(module_name, caller_globals):
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        colored_print(YELLOW, f"[!] Module '{module_name}' not found. Attempting to install...")

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            module = importlib.import_module(module_name)
        except Exception as e:
            colored_print(RED, f"[X] ERROR: Failed to install '{module_name}'.")
            colored_print(RED, f"[X] ERROR DETAILS: {e}")

            # Check if it is a Linux system that is blocking the installation
            if platform.system() == "Linux":
                colored_print(YELLOW, "[!] Some Linux VPS (Ubuntu, Debian) require --break-system-packages.")
                choice = input("[?] Try again with '--break-system-packages'? (Y/N): ").strip().lower()
                
                if choice == 'y':
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", module_name])
                        module = importlib.import_module(module_name)
                    except Exception as e:
                        colored_print(RED, f"[X] ERROR: Even with '--break-system-packages', installation failed.")
                        colored_print(RED, f"[X] ERROR DETAILS: {e}")

            input("[!] Press ENTER to continue (the script may crash)...")
            return None  # Exit cleanly if everything fails

    # Inject the module into the caller's global space
    try:
        caller_globals[module_name] = module
    except Exception as e:
        colored_print(RED, f"[X] ERROR: Failed to inject '{module_name}' into the global workspace.")
        colored_print(RED, f"[X] ERROR DETAILS: {e}")

def add(modules):
    caller_globals = inspect.stack()[1].frame.f_globals
    for module in modules:
        __amdl__(module, caller_globals)
    os.system('cls' if os.name == 'nt' else 'clear')
