# PostScript Interpreter - Project Structure

## Overview

The codebase has been refactored into a modular structure to support the implementation of additional PostScript operations.

## Directory Structure

```
PostScript Interpreter/
├── src/                           # Main source code
│   ├── __init__.py
│   ├── core/                      # Core components
│   │   ├── __init__.py
│   │   ├── exceptions.py          # ParseFailed, TypeMismatch
│   │   ├── psdict.py              # PSDict class
│   │   └── stacks.py              # Global stacks (op_stack, dict_stack)
│   │
│   ├── parsers/                   # Input parsers
│   │   ├── __init__.py
│   │   └── parsers.py             # Boolean, number, name, code block parsers
│   │
│   ├── operations/                # PostScript operations
│   │   ├── __init__.py
│   │   ├── arithmetic_ops.py      # add, mul (more to be added)
│   │   ├── dict_ops.py            # dict, def, begin, end
│   │   └── io_ops.py              # = (print operation)
│   │
│   ├── interpreter.py             # Core interpreter logic
│   └── repl.py                    # Read-Eval-Print Loop
│
├── tests/                         # Test suite
│   ├── __init__.py
│   └── test_psip.py               # All current tests
│
├── psip.py                        # Entry point
├── .gitignore                     # Git ignore file
└── README.md                      # Project documentation
```

## Key Components

### Core (`src/core/`)

- **exceptions.py**: Custom exception classes
- **psdict.py**: PostScript dictionary implementation
- **stacks.py**: Global operand and dictionary stacks

### Parsers (`src/parsers/`)

- **parsers.py**: All input parsing functions (boolean, number, name constants, code blocks)

### Operations (`src/operations/`)

- **arithmetic_ops.py**: Mathematical operations (add, mul)
- **dict_ops.py**: Dictionary operations (dict, def, begin, end)
- **io_ops.py**: Input/output operations (=)

### Interpreter (`src/`)

- **interpreter.py**: Lookup functions and process_input
- **repl.py**: REPL loop implementation

## Running the Project

### Start the REPL

```powershell
python psip.py
```

### Run Tests

```powershell
pytest tests/test_psip.py -v
```

## Adding New Operations

To add new PostScript operations:

1. Create a new file in `src/operations/` (e.g., `stack_ops.py`, `string_ops.py`)
2. Implement the operation functions
3. Import and register in `src/interpreter.py` → `register_builtin_operations()`
4. Create corresponding test file in `tests/` (e.g., `test_stack_ops.py`)

### Example: Adding a subtraction operation

**File: `src/operations/arithmetic_ops.py`**

```python
def sub_operation():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        result = op2 - op1
        op_stack.append(result)
    else:
        raise TypeMismatch("Not enough operands for subtraction.")
```

**File: `src/interpreter.py`** (add to register_builtin_operations)

```python
from src.operations import sub_operation
# ...
dict_stack[-1]["sub"] = sub_operation
```

## Next Steps

Ready to implement the remaining PostScript operations:

- Stack manipulation (exch, pop, copy, dup, clear, count)
- More arithmetic (div, sub, idiv, mod, abs, neg, ceiling, floor, round, sqrt)
- String operations (length, get, getinterval, putinterval)
- Boolean operations (eq, ne, ge, gt, le, lt, and, not, or, true, false)
- Control flow (if, ifelse, for, repeat, quit)
- I/O (print, ==)
