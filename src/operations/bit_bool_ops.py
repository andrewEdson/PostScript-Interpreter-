"""Bit and Boolean Operations for PostScript Interpreter"""

from src.core.stacks import op_stack
from src.core.exceptions import TypeMismatch


def eq_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        result = op2 == op1
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for eq operation.")


def ne_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        result = op2 != op1
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for ne operation.")


def ge_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 >= op1
        except TypeError:
            raise TypeMismatch("Operands must be comparable for ge operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for ge operation.")


def gt_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 > op1
        except TypeError:
            raise TypeMismatch("Operands must be comparable for gt operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for gt operation.")


def le_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 <= op1
        except TypeError:
            raise TypeMismatch("Operands must be comparable for le operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for le operation.")


def lt_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            result = op2 < op1
        except TypeError:
            raise TypeMismatch("Operands must be comparable for lt operation.")
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands on the stack for lt operation.")


def and_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, bool) and isinstance(op2, bool):
            result = op2 and op1
            op_stack.append(result)
        else:
            raise TypeMismatch("Operands must be booleans for and operation.")
    else:
        raise TypeMismatch("Not enough operands on the stack for and operation.")


def or_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, bool) and isinstance(op2, bool):
            result = op2 or op1
            op_stack.append(result)
        else:
            raise TypeMismatch("Operands must be booleans for or operation.")
    else:
        raise TypeMismatch("Not enough operands on the stack for or operation.")


def not_operation():
    if len(op_stack) >= 1:
        op = op_stack.pop()
        if isinstance(op, bool):
            result = not op
            op_stack.append(result)
        else:
            raise TypeMismatch("Operand must be a boolean for not operation.")
    else:
        raise TypeMismatch("Not enough operands on the stack for not operation.")


def true_operation():
    op_stack.append(True)


def false_operation():
    op_stack.append(False)
