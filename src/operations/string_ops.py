"""String Operations For PostScript Interpreter"""

from src.core.stacks import op_stack
from src.core.exceptions import TypeMismatch


def length_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        try:
            length = len(op1)
        except TypeError:
            raise TypeMismatch(
                "Operand must be a string or array for length operation."
            )
        op_stack.append(length)
    else:
        raise TypeMismatch("Not enough operands on the stack for length operation.")


def get_operation():
    if len(op_stack) >= 2:
        index = op_stack.pop()
        string_obj = op_stack.pop()
        if not isinstance(string_obj, str):
            raise TypeMismatch("First operand must be a string for get operation.")
        if not isinstance(index, int):
            raise TypeMismatch(
                "Second operand must be an integer index for get operation."
            )
        try:
            char = string_obj[index]
        except IndexError:
            raise TypeMismatch("Index out of bounds for get operation.")
        op_stack.append(char)
    else:
        raise TypeMismatch("Not enough operands on the stack for get operation.")


def getinterval_operation():
    if len(op_stack) >= 3:
        length = op_stack.pop()
        index = op_stack.pop()
        string_obj = op_stack.pop()
        if not isinstance(string_obj, str):
            raise TypeMismatch(
                "First operand must be a string for getinterval operation."
            )
        if not isinstance(index, int) or not isinstance(length, int):
            raise TypeMismatch(
                "Second and third operands must be integers for getinterval operation."
            )
        try:
            substring = string_obj[index : index + length]
        except IndexError:
            raise TypeMismatch(
                "Index and length out of bounds for getinterval operation."
            )
        op_stack.append(substring)
    else:
        raise TypeMismatch(
            "Not enough operands on the stack for getinterval operation."
        )


def putinterval_operation():
    if len(op_stack) >= 3:
        substring = op_stack.pop()
        index = op_stack.pop()
        string_obj = op_stack.pop()
        if not isinstance(string_obj, str):
            raise TypeMismatch(
                "First operand must be a string for putinterval operation."
            )
        if not isinstance(index, int):
            raise TypeMismatch(
                "Second operand must be an integer index for putinterval operation."
            )
        if not isinstance(substring, str):
            raise TypeMismatch(
                "Third operand must be a string for putinterval operation."
            )
        if index < 0 or index + len(substring) > len(string_obj):
            raise TypeMismatch(
                "Index and substring length out of bounds for putinterval operation."
            )
        new_string = (
            string_obj[:index] + substring + string_obj[index + len(substring) :]
        )
        op_stack.append(new_string)
    else:
        raise TypeMismatch(
            "Not enough operands on the stack for putinterval operation."
        )
