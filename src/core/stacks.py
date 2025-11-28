"""Global stacks and configuration for PostScript Interpreter"""

from .psdict import PSDict

# Global Stacks
op_stack = []
dict_stack = []
dict_stack.append(PSDict())

# Scoping configuration
STATIC_SCOPING = False
