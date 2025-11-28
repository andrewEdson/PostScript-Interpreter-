import logging

logging.basicConfig(level=logging.DEBUG)

STATIC_SCOPING = False


##------PSDICT
class PSDict:
    """PostScript Dictionary Object"""

    def __init__(self):
        self.dict = {}
        self.parent = None  # For static scoping

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]

    def set_parent(self, parent):
        self.parent = parent

    def __contains__(self, key):
        return key in self.dict

    def __repr__(self):
        return f"PSDict({self.dict})"

    def __str__(self):
        return f"PSDict({self.dict})"


##--------Interprester Exceptions ----------------------------
class ParseFailed(Exception):
    """A exception indicating that parsing has failed."""

    def __init__(self, message):
        super().__init__(message)


class TypeMismatch(Exception):
    """A exception indicating that type mismatch has failed."""

    def __init__(self, message):
        super().__init__(message)


##----------Parsers -----------------------------------


# Boolean Parser
def process_boolean(input):
    logging.debug("input to process_boolean: %s", input)
    if input == "true":
        return True
    elif input == "false":
        return False
    else:
        raise ParseFailed(f"Invalid boolean value: {input}")


# Number Parser
def process_number(input):
    logging.debug("input to process_number: %s", input)
    try:
        float_value = float(input)
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        raise ParseFailed(f"Invalid number value: {input}")


# Parse Varaibles
def process_name_constant(input):
    logging.debug("input to process_name_constant: %s", input)
    if input.startswith("/"):
        return input
    else:
        raise ParseFailed(f"Invalid name constant: {input}")


# Code Block Parser
def process_code_block(input):
    logging.debug("input to process_code_block: %s", input)
    if len(input) >= 2 and input.startswith("{") and input.endswith("}"):
        return input[1:-1].strip().split()
    else:
        raise ParseFailed(f"Invalid code block: {input}")


# Set of all parsers
PARSERS = {
    process_boolean,
    process_number,
    process_name_constant,
    process_code_block,
}


def process_constants(inputs):
    for parser in PARSERS:
        try:
            return parser(inputs)
        except ParseFailed as e:
            logging.debug("Parser %s failed: %s", parser.__name__, e)
            continue
    raise ParseFailed(f"No parser could handle the input: {inputs}")


# Global Stacks
op_stack = []
dict_stack = []
dict_stack.append(PSDict())

##--------- IN BUILT OPERATIONS -----------------------


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


def pop_print_operation():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        print(op1)
    else:
        raise TypeMismatch("Not enough operands on the stack for pop and print.")


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


# Registering operations in the dictionary stack
dict_stack[-1]["add"] = add_operation
dict_stack[-1]["mul"] = mul_operation
dict_stack[-1]["="] = pop_print_operation
dict_stack[-1]["def"] = def_operation
dict_stack[-1]["dict"] = dict_operation
dict_stack[-1]["begin"] = begin_operation
dict_stack[-1]["end"] = end_operation


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


# REPL
def repl():
    while True:
        user_input = input("REPL> ")
        if user_input.strip().startswith("{"):
            process_input(user_input)
        else:
            tokens = user_input.split()
            for token in tokens:
                if token.lower() == "quit":
                    return
                process_input(token)
        logging.debug(f"Operator Stack: {op_stack}")


if __name__ == "__main__":
    repl()
