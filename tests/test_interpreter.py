"""Tests for interpreter core functionality"""

import pytest
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.core.exceptions import ParseFailed
from src.operations.arithmetic_ops import add_operation, mul_operation
from src.operations.io_ops import pop_print_operation
from src.operations.dict_ops import (
    def_operation,
    dict_operation,
    begin_operation,
    end_operation,
)
from src.interpreter import process_input, register_builtin_operations


class TestOperandStack:
    """Tests for operand stack operations."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()

    def test_process_input_boolean(self):
        process_input("true")
        assert op_stack[-1] is True

    def test_process_input_number(self):
        process_input("123")
        assert op_stack[-1] == 123

    def test_process_input_invalid(self):
        initial_length = len(op_stack)
        process_input("invalidinput")
        assert len(op_stack) == initial_length  # Stack should remain unchanged


class TestDictionaryScoping:
    """Tests for dictionary scoping and nested dictionaries."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_variable_lookup_in_nested_dict(self):
        # Define x in global scope
        process_input("/x")
        process_input("10")
        process_input("def")

        # Create and enter new dictionary
        process_input("/mydict")
        process_input("dict")
        process_input("def")
        process_input("mydict")
        process_input("begin")

        # x should still be accessible from parent scope
        process_input("x")
        assert op_stack[-1] == 10

    def test_variable_shadowing_in_nested_dict(self):
        # Define x in global scope
        process_input("/x")
        process_input("10")
        process_input("def")

        # Create and enter new dictionary
        process_input("/mydict")
        process_input("dict")
        process_input("def")
        process_input("mydict")
        process_input("begin")

        # Redefine x in nested scope
        process_input("/x")
        process_input("20")
        process_input("def")

        # Should get the shadowed value
        process_input("x")
        assert op_stack[-1] == 20

        # Exit nested scope
        process_input("end")

        # Should get original value
        op_stack.clear()
        process_input("x")
        assert op_stack[-1] == 10


class TestComplexOperations:
    """Tests for complex multi-step operations."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_define_and_use_variable(self):
        process_input("/x")
        process_input("5")
        process_input("def")
        process_input("x")
        process_input("x")
        process_input("mul")
        assert op_stack[-1] == 25

    def test_multiple_operations(self):
        process_input("2")
        process_input("3")
        process_input("add")
        process_input("4")
        process_input("mul")
        assert op_stack[-1] == 20

    def test_define_multiple_variables(self):
        process_input("/a")
        process_input("10")
        process_input("def")
        process_input("/b")
        process_input("20")
        process_input("def")
        process_input("a")
        process_input("b")
        process_input("add")
        assert op_stack[-1] == 30
