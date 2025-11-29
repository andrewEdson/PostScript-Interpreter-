"""Global stacks and configuration for PostScript Interpreter"""

from .psdict import PSDict

# Global Stacks
op_stack = []
dict_stack = []
dict_stack.append(PSDict())

# Scoping configuration
# Set to True for static (lexical) scoping, False for dynamic scoping (default)
STATIC_SCOPING = False
