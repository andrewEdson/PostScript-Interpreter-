"""PostScript Interpreter - Entry Point"""

import logging

logging.basicConfig(level=logging.DEBUG)

from src.interpreter import register_builtin_operations
from src.repl import repl

if __name__ == "__main__":
    # Register built-in operations
    register_builtin_operations()
    # Start REPL
    repl()
