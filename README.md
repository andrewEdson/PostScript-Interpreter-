# PostScript Interpreter

A Python-based PostScript interpreter supporting dynamic and static (lexical) scoping, with comprehensive implementation of PostScript operations.

## Table of Contents

- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Scoping Behavior](#scoping-behavior)
- [Important Syntax Notes](#important-syntax-notes)
- [Implemented Commands](#implemented-commands)
- [Testing](#testing)

## Features

- **Full PostScript subset implementation** with 40+ operations
- **Dynamic scoping** (default) - matches actual PostScript behavior
- **Static/Lexical scoping** - toggle via flag for comparison
- **Comprehensive test suite** with 311+ automated tests
- **REPL interface** for interactive use
- **File execution** for running PostScript scripts

## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd "PostScript Interpreter"
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Interactive REPL Mode

Start the interpreter in interactive mode:

```bash
python psip.py
```

Then enter PostScript commands line by line:

```
REPL> 5 3 add
REPL> =
8
```

### File Execution Mode

Run a PostScript script file:

```bash
python psip.py script.ps
```

### Exit the Interpreter

Type `quit` or press `Ctrl+C` in REPL mode.

## Scoping Behavior

The interpreter supports both **dynamic scoping** (PostScript default) and **static/lexical scoping**.

### How to Change Scoping Mode

1. Open `src/core/stacks.py`
2. Locate the `STATIC_SCOPING` variable (around line 11)
3. Set the value:
   - `STATIC_SCOPING = False` for **dynamic scoping** (default)
   - `STATIC_SCOPING = True` for **static/lexical scoping**

### Scoping Demonstration Example

Here's a test case that demonstrates the difference between dynamic and static scoping:

```postscript
/x 10 def
/test
{ x = }
def
test
1 dict begin
/x 99 def
test
end
```

**With Dynamic Scoping (`STATIC_SCOPING = False`):**

```
Output: 10
        99
```

The function `test` looks up `x` from the current scope each time it's called. When called inside the `begin`/`end` block, it finds `x = 99`.

**With Static/Lexical Scoping (`STATIC_SCOPING = True`):**

```
Output: 10
        10
```

The function `test` captures the scope where it was defined (where `x = 10`). It always uses that value regardless of where it's called from.

**Explanation:**

- **Dynamic Scoping**: Variables are resolved by searching the dictionary stack from top (current scope) to bottom (global scope) at the time the variable is accessed.
- **Static/Lexical Scoping**: Variables are resolved using the scope where the function was defined, not where it's called. This is implemented using closures that capture the defining dictionary.

## Important Syntax Notes

### Code Blocks Must Be on Separate Lines

Due to the parser design, **code blocks (procedures) must be placed on separate lines**

**✗ INCORRECT:**

```postscript
/x { 1 2 add } def
```

**✓ CORRECT:**

```postscript
/x
{ 1 2 add }
def
```

**Example - Defining and using a function:**

```postscript
/square
{ dup mul }
def
5 square =
```

Output: `25`

## Implemented Commands

### Stack Manipulation Operations

| Command | Description                          | Example                      |
| ------- | ------------------------------------ | ---------------------------- |
| `exch`  | Exchange the top two elements        | `1 2 exch` → `2 1`           |
| `pop`   | Remove the top element               | `1 2 pop` → `1`              |
| `dup`   | Duplicate the top element            | `5 dup` → `5 5`              |
| `copy`  | Copy the top n elements              | `1 2 3 2 copy` → `1 2 3 2 3` |
| `clear` | Remove all elements from the stack   | `1 2 3 clear` → (empty)      |
| `count` | Push the number of elements on stack | `1 2 3 count` → `1 2 3 3`    |

### Arithmetic Operations

| Command | Description               | Example             |
| ------- | ------------------------- | ------------------- |
| `add`   | Add two numbers           | `3 4 add` → `7`     |
| `sub`   | Subtract (second - first) | `10 3 sub` → `7`    |
| `mul`   | Multiply two numbers      | `3 4 mul` → `12`    |
| `div`   | Divide (second / first)   | `10 2 div` → `5.0`  |
| `idiv`  | Integer division          | `10 3 idiv` → `3`   |
| `mod`   | Modulus operation         | `10 3 mod` → `1`    |
| `abs`   | Absolute value            | `-5 abs` → `5`      |
| `neg`   | Negate a number           | `5 neg` → `-5`      |
| `ceil`  | Round up to integer       | `3.2 ceil` → `4.0`  |
| `floor` | Round down to integer     | `3.8 floor` → `3.0` |
| `round` | Round to nearest integer  | `3.5 round` → `4.0` |
| `sqrt`  | Square root               | `16 sqrt` → `4.0`   |

### Boolean/Comparison Operations

| Command | Description           | Example                    |
| ------- | --------------------- | -------------------------- |
| `eq`    | Test equality         | `5 5 eq` → `true`          |
| `ne`    | Test inequality       | `5 3 ne` → `true`          |
| `gt`    | Greater than          | `5 3 gt` → `true`          |
| `lt`    | Less than             | `3 5 lt` → `true`          |
| `ge`    | Greater than or equal | `5 5 ge` → `true`          |
| `le`    | Less than or equal    | `3 5 le` → `true`          |
| `and`   | Logical AND           | `true false and` → `false` |
| `or`    | Logical OR            | `true false or` → `true`   |
| `not`   | Logical NOT           | `true not` → `false`       |
| `true`  | Push boolean true     | `true` → `true`            |
| `false` | Push boolean false    | `false` → `false`          |

### Dictionary Operations

| Command     | Description                     | Example                   |
| ----------- | ------------------------------- | ------------------------- |
| `dict`      | Create a new dictionary         | `5 dict` → (creates dict) |
| `begin`     | Push dictionary onto dict stack | `mydict begin`            |
| `end`       | Pop dictionary from dict stack  | `end`                     |
| `def`       | Define a key-value pair         | `/x 10 def`               |
| `length`    | Get dictionary size             | `mydict length`           |
| `maxlength` | Get dictionary capacity         | `mydict maxlength`        |

### String Operations

| Command       | Description             | Example                               |
| ------------- | ----------------------- | ------------------------------------- |
| `length`      | Get string/array length | `(hello) length` → `5`                |
| `get`         | Get character at index  | `(hello) 1 get` → `e`                 |
| `getinterval` | Get substring           | `(hello) 1 3 getinterval` → `ell`     |
| `putinterval` | Replace substring       | `(hello) 1 (i) putinterval` → `hillo` |

### Flow Control Operations

| Command  | Description           | Example                          |
| -------- | --------------------- | -------------------------------- |
| `if`     | Conditional execution | `true { 1 = } if` → `1`          |
| `ifelse` | If-then-else          | `false { 1 } { 2 } ifelse` → `2` |
| `for`    | Loop with counter     | `1 3 { = } for` → `1 2 3`        |
| `repeat` | Repeat n times        | `3 { 5 = } repeat` → `5 5 5`     |

### Input/Output Operations

| Command | Description                     | Example                   |
| ------- | ------------------------------- | ------------------------- |
| `=`     | Print top of stack (pop)        | `42 =` → `42`             |
| `==`    | Print PostScript representation | `(hello) ==` → `(hello)`  |
| `print` | Print string without newline    | `(hello) print` → `hello` |

## Testing

The interpreter includes a comprehensive test suite with 311+ automated tests covering all operations.

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests for Specific Module

```bash
pytest tests/test_arithmetic_ops.py
pytest tests/test_stack_ops.py
pytest tests/test_dict_ops.py
```

### Run Tests with Coverage Report

```bash
pytest --cov=src
```

### Test Structure

- `tests/test_arithmetic_ops.py` - Arithmetic operation tests
- `tests/test_stack_ops.py` - Stack manipulation tests
- `tests/test_dict_ops.py` - Dictionary operation tests
- `tests/test_bit_bool_ops.py` - Boolean/comparison tests
- `tests/test_flow_ops.py` - Flow control tests
- `tests/test_string_ops.py` - String operation tests
- `tests/test_io_ops.py` - I/O operation tests

## Project Structure

```
PostScript Interpreter/
├── src/
│   ├── core/
│   │   ├── stacks.py          # Global stacks and STATIC_SCOPING flag
│   │   ├── psdict.py          # Dictionary and Closure classes
│   │   └── exceptions.py      # Custom exceptions
│   ├── operations/
│   │   ├── arithmetic_ops.py  # Arithmetic operations
│   │   ├── stack_ops.py       # Stack manipulation
│   │   ├── dict_ops.py        # Dictionary operations
│   │   ├── bit_bool_ops.py    # Boolean/comparison ops
│   │   ├── flow_ops.py        # Flow control
│   │   ├── string_ops.py      # String operations
│   │   └── io_ops.py          # Input/output operations
│   ├── parsers/
│   │   └── parsers.py         # Input parsing logic
│   ├── interpreter.py         # Core interpreter with scoping logic
│   └── repl.py                # REPL interface
├── tests/                     # Automated test suite
├── psip.py                    # Main entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Implementation Notes

- **Dynamic Scoping**: Implemented by searching the `dict_stack` list from top (most recent) to bottom (global scope)
- **Static Scoping**: Implemented using `PSClosure` objects that wrap code blocks with their defining dictionary, creating lexical closures
- **Parser**: Line-based parser that requires code blocks on separate lines
- **Error Handling**: Custom exceptions for type mismatches and parsing failures

## Author

Andrew Edson

## License

Academic project for CS 355 (Programming Language Design)
