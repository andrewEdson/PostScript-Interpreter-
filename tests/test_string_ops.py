"""Tests for string operations"""

import pytest
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.core.exceptions import TypeMismatch
from src.operations.string_ops import (
    length_operation,
    get_operation,
    getinterval_operation,
    putinterval_operation,
)
from src.interpreter import process_input, register_builtin_operations


class TestLengthOperation:
    """Tests for the length operation on strings."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_length_operation_string(self):
        op_stack.append("hello")
        length_operation()
        assert op_stack[-1] == 5

    def test_length_operation_empty_string(self):
        op_stack.append("")
        length_operation()
        assert op_stack[-1] == 0

    def test_length_operation_list(self):
        op_stack.append([1, 2, 3, 4])
        length_operation()
        assert op_stack[-1] == 4

    def test_length_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            length_operation()

    def test_length_operation_invalid_operand(self):
        op_stack.append(42)  # Number doesn't have length
        with pytest.raises(TypeMismatch):
            length_operation()

    def test_length_operation_repl(self):
        process_input("(hello world)")
        process_input("length")
        assert op_stack[-1] == 11


class TestGetOperation:
    """Tests for the get operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_get_operation_valid(self):
        op_stack.append("hello")
        op_stack.append(0)
        get_operation()
        assert op_stack[-1] == "h"

    def test_get_operation_middle_index(self):
        op_stack.append("world")
        op_stack.append(2)
        get_operation()
        assert op_stack[-1] == "r"

    def test_get_operation_last_index(self):
        op_stack.append("test")
        op_stack.append(3)
        get_operation()
        assert op_stack[-1] == "t"

    def test_get_operation_index_out_of_bounds(self):
        op_stack.append("hello")
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            get_operation()

    def test_get_operation_negative_index(self):
        op_stack.append("hello")
        op_stack.append(-1)
        get_operation()
        assert op_stack[-1] == "o"  # Python allows negative indexing

    def test_get_operation_insufficient_operands(self):
        op_stack.append("hello")
        with pytest.raises(TypeMismatch):
            get_operation()

    def test_get_operation_non_string_first_operand(self):
        op_stack.append(42)
        op_stack.append(0)
        with pytest.raises(TypeMismatch):
            get_operation()

    def test_get_operation_non_integer_index(self):
        op_stack.append("hello")
        op_stack.append(1.5)
        with pytest.raises(TypeMismatch):
            get_operation()

    def test_get_operation_repl(self):
        process_input("(PostScript)")
        process_input("4")
        process_input("get")
        assert op_stack[-1] == "S"


class TestGetintervalOperation:
    """Tests for the getinterval operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_getinterval_operation_valid(self):
        op_stack.append("hello world")
        op_stack.append(0)
        op_stack.append(5)
        getinterval_operation()
        assert op_stack[-1] == "hello"

    def test_getinterval_operation_middle_substring(self):
        op_stack.append("hello world")
        op_stack.append(6)
        op_stack.append(5)
        getinterval_operation()
        assert op_stack[-1] == "world"

    def test_getinterval_operation_partial_substring(self):
        op_stack.append("testing")
        op_stack.append(2)
        op_stack.append(3)
        getinterval_operation()
        assert op_stack[-1] == "sti"

    def test_getinterval_operation_zero_length(self):
        op_stack.append("hello")
        op_stack.append(2)
        op_stack.append(0)
        getinterval_operation()
        assert op_stack[-1] == ""

    def test_getinterval_operation_full_string(self):
        op_stack.append("complete")
        op_stack.append(0)
        op_stack.append(8)
        getinterval_operation()
        assert op_stack[-1] == "complete"

    def test_getinterval_operation_insufficient_operands(self):
        op_stack.append("hello")
        op_stack.append(0)
        with pytest.raises(TypeMismatch):
            getinterval_operation()

    def test_getinterval_operation_non_string_first_operand(self):
        op_stack.append(42)
        op_stack.append(0)
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            getinterval_operation()

    def test_getinterval_operation_non_integer_index(self):
        op_stack.append("hello")
        op_stack.append(1.5)
        op_stack.append(3)
        with pytest.raises(TypeMismatch):
            getinterval_operation()

    def test_getinterval_operation_non_integer_length(self):
        op_stack.append("hello")
        op_stack.append(0)
        op_stack.append(2.5)
        with pytest.raises(TypeMismatch):
            getinterval_operation()

    def test_getinterval_operation_repl(self):
        process_input("(PostScript Language)")
        process_input("4")
        process_input("6")
        process_input("getinterval")
        assert op_stack[-1] == "Script"


class TestPutintervalOperation:
    """Tests for the putinterval operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_putinterval_operation_valid(self):
        op_stack.append("hello world")
        op_stack.append(0)
        op_stack.append("HELLO")
        putinterval_operation()
        assert op_stack[-1] == "HELLO world"

    def test_putinterval_operation_middle_replacement(self):
        op_stack.append("hello world")
        op_stack.append(6)
        op_stack.append("WORLD")
        putinterval_operation()
        assert op_stack[-1] == "hello WORLD"

    def test_putinterval_operation_partial_replacement(self):
        op_stack.append("testing")
        op_stack.append(1)
        op_stack.append("EST")
        putinterval_operation()
        assert op_stack[-1] == "tESTing"

    def test_putinterval_operation_single_char(self):
        op_stack.append("hello")
        op_stack.append(0)
        op_stack.append("H")
        putinterval_operation()
        assert op_stack[-1] == "Hello"

    def test_putinterval_operation_empty_substring(self):
        op_stack.append("hello")
        op_stack.append(2)
        op_stack.append("")
        putinterval_operation()
        assert op_stack[-1] == "hello"

    def test_putinterval_operation_index_out_of_bounds(self):
        op_stack.append("hello")
        op_stack.append(10)
        op_stack.append("test")
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_operation_substring_too_long(self):
        op_stack.append("hello")
        op_stack.append(3)
        op_stack.append("TOOLONG")
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_operation_negative_index(self):
        op_stack.append("hello")
        op_stack.append(-1)
        op_stack.append("x")
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_operation_insufficient_operands(self):
        op_stack.append("hello")
        op_stack.append(0)
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_operation_non_string_first_operand(self):
        op_stack.append(42)
        op_stack.append(0)
        op_stack.append("test")
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_operation_non_integer_index(self):
        op_stack.append("hello")
        op_stack.append(1.5)
        op_stack.append("test")
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_operation_non_string_substring(self):
        op_stack.append("hello")
        op_stack.append(0)
        op_stack.append(42)
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_operation_repl(self):
        process_input("(hello world)")
        process_input("6")
        process_input("(WORLD)")
        process_input("putinterval")
        assert op_stack[-1] == "hello WORLD"
