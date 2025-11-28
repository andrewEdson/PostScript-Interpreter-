"""Dictionary operations for PostScript Interpreter"""

from src.core.stacks import op_stack, dict_stack, STATIC_SCOPING
from src.core.exceptions import TypeMismatch
from src.core.psdict import PSDict


def def_operation():
    if len(op_stack) >= 2:
        value = op_stack.pop()
        key = op_stack.pop()
        if isinstance(key, str) and key.startswith("/"):
            key = key[1:]  # Remove leading '/'
            dict_stack[-1][key] = value
        else:
            op_stack.append(key)
            op_stack.append(value)
            raise TypeMismatch("Key must be a name constant starting with '/'.")
    else:
        raise TypeMismatch("Not enough operands on the stack for definition.")


def dict_operation():
    new_dict = PSDict()
    if STATIC_SCOPING:
        current_dict = dict_stack[-1]
        new_dict.set_parent(current_dict)
    op_stack.append(new_dict)


def begin_operation():
    if len(op_stack) >= 1:
        dict_obj = op_stack.pop()
        if isinstance(dict_obj, PSDict):
            dict_stack.append(dict_obj)
        else:
            raise TypeMismatch("Operand must be a dictionary for begin operation.")
    else:
        raise TypeMismatch("Not enough operands on the stack for begin operation.")


def end_operation():
    if len(dict_stack) > 1:
        dict_stack.pop()
    else:
        raise TypeMismatch("Cannot pop the last dictionary from the dictionary stack.")


def length_operation():
    if len(op_stack) >= 1:
        dict_obj = op_stack.pop()
        if isinstance(dict_obj, PSDict):
            length = len(dict_obj)
            op_stack.append(length)
        else:
            raise TypeMismatch("Operand must be a dictionary for length operation.")
    else:
        raise TypeMismatch("Not enough operands on the stack for length operation.")


def maxlength_operation():
    if len(op_stack) >= 1:
        dict_obj = op_stack.pop()
        if isinstance(dict_obj, PSDict):
            maxlength = dict_obj.max_length()
            op_stack.append(maxlength)
        else:
            raise TypeMismatch("Operand must be a dictionary for maxlength operation.")
    else:
        raise TypeMismatch("Not enough operands on the stack for maxlength operation.")
