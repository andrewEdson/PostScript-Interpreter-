"""PostScript Interpreter REPL"""

import logging
from src.core.stacks import op_stack
from src.interpreter import process_input


def repl():
    """Read-Eval-Print Loop for PostScript Interpreter"""
    while True:
        user_input = input("REPL> ")
        if user_input.strip().startswith("{"):
            process_input(user_input)
        else:
            tokens = user_input.split()
            for token in tokens:
                if token.lower() == "quit":
                    return
                process_input(token)
        logging.debug(f"Operator Stack: {op_stack}")
