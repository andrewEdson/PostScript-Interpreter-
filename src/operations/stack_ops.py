"""Stack Manipulations Operations"""

from src.core.stacks import op_stack
from src.core.exceptions import TypeMismatch


def exch_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op1)
        op_stack.append(op2)
    else:
        raise TypeMismatch("Not enough operands on the stack for exch.")


def pop_operation():
    if len(op_stack) >= 1:
        op_stack.pop()
    else:
        raise TypeMismatch("Not enough operands on the stack for pop.")


def copy_operation():
    if len(op_stack) >= 1:
        n = op_stack.pop()
        if isinstance(n, int) and n >= 0:
            if len(op_stack) >= n:
                items_to_copy = op_stack[-n:]
                op_stack.extend(items_to_copy)
            else:
                raise TypeMismatch("Not enough operands on the stack to copy.")
        else:
            raise TypeMismatch("Operand for copy must be a non-negative integer.")
    else:
        raise TypeMismatch("Not enough operands on the stack for copy.")


def dup_operation():
    if len(op_stack) >= 1:
        op1 = op_stack[-1]
        op_stack.append(op1)
    else:
        raise TypeMismatch("Not enough operands on the stack for dup.")


def clear_operation():
    op_stack.clear()


def count_operation():
    op_stack.append(len(op_stack))
