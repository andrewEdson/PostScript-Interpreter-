"""PostScript Interpreter Core Logic"""

import logging
from src.core.stacks import op_stack, dict_stack, STATIC_SCOPING
from src.core.exceptions import ParseFailed
from src.parsers.parsers import process_constants


def lookup_in_dictionary(input):
    for i in range(len(dict_stack) - 1, -1, -1):
        current_dict = dict_stack[i]
        if input in current_dict:
            value = current_dict[input]
            if callable(value):
                value()  # Execute the operation
            elif isinstance(value, list):
                for item in value:
                    process_input(item)
            else:
                op_stack.append(value)
            return
    raise ParseFailed(f"Could not find {input} in any dictionary.")


def lookup_in_dictionary_static(input):
    current_dict = dict_stack[-1]
    while current_dict is not None:
        if input in current_dict:
            value = current_dict[input]
            if callable(value):
                value()  # Execute the operation
            elif isinstance(value, list):
                for item in value:
                    process_input(item)
            else:
                op_stack.append(value)
            return
        current_dict = current_dict.parent
    raise ParseFailed(f"Could not find {input} in any dictionary.")


def process_input(user_input):
    try:
        res = process_constants(user_input)
        op_stack.append(res)
    except ParseFailed as e:
        logging.debug(e)
        try:
            if STATIC_SCOPING:
                lookup_in_dictionary_static(user_input)
            else:
                lookup_in_dictionary(user_input)
        except Exception as e:
            logging.error(f"Could not process input '{user_input}': {e}")


def register_builtin_operations():
    """Register all built-in operations in the dictionary stack"""
    from src.operations import (
        add_operation,
        mul_operation,
        div_operation,
        sub_operation,
        idiv_operation,
        mod_operation,
        abs_operation,
        neg_operation,
        ceil_operation,
        floor_operation,
        round_operation,
        sqrt_operation,
        pop_print_operation,
        def_operation,
        dict_operation,
        begin_operation,
        end_operation,
        dict_length_operation,
        maxlength_operation,
        string_length_operation,
        get_operation,
        getinterval_operation,
        putinterval_operation,
        eq_operation,
        ne_operation,
        ge_operation,
        gt_operation,
        le_operation,
        lt_operation,
        and_operation,
        or_operation,
        not_operation,
        true_operation,
        false_operation,
        if_operation,
        ifelse_operation,
        repeat_operation,
        exch_operation,
        pop_operation,
        copy_operation,
        dup_operation,
        clear_operation,
        count_operation,
    )

    # Arithmetic operations
    dict_stack[-1]["add"] = add_operation
    dict_stack[-1]["mul"] = mul_operation
    dict_stack[-1]["div"] = div_operation
    dict_stack[-1]["sub"] = sub_operation
    dict_stack[-1]["idiv"] = idiv_operation
    dict_stack[-1]["mod"] = mod_operation
    dict_stack[-1]["abs"] = abs_operation
    dict_stack[-1]["neg"] = neg_operation
    dict_stack[-1]["ceiling"] = ceil_operation
    dict_stack[-1]["floor"] = floor_operation
    dict_stack[-1]["round"] = round_operation
    dict_stack[-1]["sqrt"] = sqrt_operation

    # I/O operations
    dict_stack[-1]["="] = pop_print_operation

    # Dictionary operations
    dict_stack[-1]["def"] = def_operation
    dict_stack[-1]["dict"] = dict_operation
    dict_stack[-1]["begin"] = begin_operation
    dict_stack[-1]["end"] = end_operation
    dict_stack[-1]["maxlength"] = maxlength_operation

    # String operations
    dict_stack[-1]["length"] = string_length_operation
    dict_stack[-1]["get"] = get_operation
    dict_stack[-1]["getinterval"] = getinterval_operation
    dict_stack[-1]["putinterval"] = putinterval_operation

    # Stack operations
    dict_stack[-1]["exch"] = exch_operation
    dict_stack[-1]["pop"] = pop_operation
    dict_stack[-1]["copy"] = copy_operation
    dict_stack[-1]["dup"] = dup_operation
    dict_stack[-1]["clear"] = clear_operation
    dict_stack[-1]["count"] = count_operation

    # Bit and Boolean operations
    dict_stack[-1]["eq"] = eq_operation
    dict_stack[-1]["ne"] = ne_operation
    dict_stack[-1]["ge"] = ge_operation
    dict_stack[-1]["gt"] = gt_operation
    dict_stack[-1]["le"] = le_operation
    dict_stack[-1]["lt"] = lt_operation
    dict_stack[-1]["and"] = and_operation
    dict_stack[-1]["or"] = or_operation
    dict_stack[-1]["not"] = not_operation
    dict_stack[-1]["true"] = true_operation
    dict_stack[-1]["false"] = false_operation

    # Flow Control operations
    dict_stack[-1]["if"] = if_operation
    dict_stack[-1]["ifelse"] = ifelse_operation
    dict_stack[-1]["repeat"] = repeat_operation
