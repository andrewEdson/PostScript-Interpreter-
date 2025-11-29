"""Input/Output operations for PostScript Interpreter"""

from src.core.stacks import op_stack
from src.core.exceptions import TypeMismatch


def pop_print_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        print(op1)
    else:
        raise TypeMismatch("Not enough operands on the stack for pop and print.")


def string_print_operation():
    if len(op_stack) >= 1:
        if not isinstance(op_stack[-1], str):
            raise TypeMismatch("Operand must be a string for string print operation.")
        op1 = op_stack.pop()
        print(op1)
    else:
        raise TypeMismatch(
            "Not enough operands on the stack for string print operation."
        )


def pop_print_postscript_rep_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        if isinstance(op1, str):
            print(f"({op1})")
        else:
            print(op1)
    else:
        raise TypeMismatch(
            "Not enough operands on the stack for pop and print PostScript representation."
        )
