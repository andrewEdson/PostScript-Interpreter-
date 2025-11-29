"""Flow Control Operations for PostScript Interpreter"""

from src.core.stacks import op_stack
from src.core.exceptions import TypeMismatch


def if_operation():
    if len(op_stack) >= 2:
        code_block = op_stack.pop()
        condition = op_stack.pop()
        if not isinstance(code_block, list):
            raise TypeMismatch("Code block must be a list.")
        if condition:
            for item in code_block:
                op_stack.append(item)
    else:
        raise TypeMismatch("Not enough operands on the stack for if operation.")


def ifelse_operation():
    if len(op_stack) >= 3:
        else_block = op_stack.pop()
        if_block = op_stack.pop()
        condition = op_stack.pop()
        if not isinstance(if_block, list) or not isinstance(else_block, list):
            raise TypeMismatch("Both code blocks must be lists.")
        if condition:
            for item in if_block:
                op_stack.append(item)
        else:
            for item in else_block:
                op_stack.append(item)
    else:
        raise TypeMismatch("Not enough operands on the stack for ifelse operation.")


def repeat_operation():
    if len(op_stack) >= 2:
        code_block = op_stack.pop()
        count = op_stack.pop()
        if not isinstance(code_block, list):
            raise TypeMismatch("Code block must be a list.")
        if not isinstance(count, int) or count < 0:
            raise TypeMismatch("Count must be a non-negative integer.")
        for _ in range(count):
            for item in code_block:
                op_stack.append(item)
    else:
        raise TypeMismatch("Not enough operands on the stack for repeat operation.")
