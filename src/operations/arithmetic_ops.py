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


def div_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 / op1
        except TypeError:
            raise TypeMismatch("Operands must be numbers for division.")
        except ZeroDivisionError:
            raise TypeMismatch("Division by zero is not allowed.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for division.")


def sub_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 - op1
        except TypeError:
            raise TypeMismatch("Operands must be numbers for subtraction.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for subtraction.")


def idiv_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 // op1
        except TypeError:
            raise TypeMismatch("Operands must be numbers for integer division.")
        except ZeroDivisionError:
            raise TypeMismatch("Division by zero is not allowed.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for integer division.")


def mod_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 % op1
        except TypeError:
            raise TypeMismatch("Operands must be numbers for modulus operation.")
        except ZeroDivisionError:
            raise TypeMismatch("Division by zero is not allowed.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for modulus operation.")


def abs_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        try:
            result = abs(op1)
        except TypeError:
            raise TypeMismatch("Operand must be a number for absolute value.")
        op_stack.append(result)
    else:
        raise TypeMismatch(
            "Not enough operands on the stack for absolute value operation."
        )


def neg_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        try:
            result = -op1
        except TypeError:
            raise TypeMismatch("Operand must be a number for negation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for negation operation.")


def ceil_operation():
    import math

    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        try:
            result = math.ceil(op1)
        except TypeError:
            raise TypeMismatch("Operand must be a number for ceiling operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for ceiling operation.")


def floor_operation():
    import math

    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        try:
            result = math.floor(op1)
        except TypeError:
            raise TypeMismatch("Operand must be a number for floor operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for floor operation.")


def round_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        try:
            result = round(op1)
        except TypeError:
            raise TypeMismatch("Operand must be a number for round operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for round operation.")


def sqrt_operation():
    import math

    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        try:
            if op1 < 0:
                raise TypeMismatch("Cannot compute square root of negative number.")
            result = math.sqrt(op1)
        except TypeError:
            raise TypeMismatch("Operand must be a number for square root operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch(
            "Not enough operands on the stack for square root operation."
        )
