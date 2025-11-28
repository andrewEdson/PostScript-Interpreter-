"""Arithmetic operations for PostScript Interpreter"""

from src.core.stacks import op_stack
from src.core.exceptions import TypeMismatch


def add_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 + op1
        except TypeError:
            raise TypeMismatch("Operands must be numbers for addition.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for addition.")


def mul_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 * op1
        except TypeError:
            raise TypeMismatch("Operands must be numbers for multiplication.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for multiplication.")
