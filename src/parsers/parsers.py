"""PostScript Parsers"""

import logging
from src.core.exceptions import ParseFailed


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


# Parse Variables
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
