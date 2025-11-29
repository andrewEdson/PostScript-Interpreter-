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
            from src.interpreter import process_input

            for item in code_block:
                if isinstance(item, str):
                    process_input(item)
                else:
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
        from src.interpreter import process_input

        if condition:
            for item in if_block:
                if isinstance(item, str):
                    process_input(item)
                else:
                    op_stack.append(item)
        else:
            for item in else_block:
                if isinstance(item, str):
                    process_input(item)
                else:
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
        from src.interpreter import process_input

        for _ in range(count):
            for item in code_block:
                if isinstance(item, str):
                    process_input(item)
                else:
                    op_stack.append(item)
    else:
        raise TypeMismatch("Not enough operands on the stack for repeat operation.")


def for_operation():
    if len(op_stack) >= 3:
        code_block = op_stack.pop()
        end = op_stack.pop()
        start = op_stack.pop()
        if not isinstance(code_block, list):
            raise TypeMismatch("Code block must be a list.")
        if not all(isinstance(i, int) for i in (start, end)):
            raise TypeMismatch("Start and end values must be integers.")
        from src.interpreter import process_input

        step = 1 if end >= start else -1
        for i in range(start, end + step, step):
            op_stack.append(i)
            for item in code_block:
                if isinstance(item, str):
                    process_input(item)
                else:
                    op_stack.append(item)
    else:
        raise TypeMismatch("Not enough operands on the stack for for operation.")
