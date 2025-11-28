"""Tests for dictionary operations"""

import pytest
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.core.exceptions import TypeMismatch
from src.operations.dict_ops import (
    def_operation,
    dict_operation,
    begin_operation,
    end_operation,
    length_operation,
    maxlength_operation,
)
from src.interpreter import process_input, register_builtin_operations


class TestDefOperation:
    """Tests for the def operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_def_operation_valid(self):
        op_stack.append("/x")
        op_stack.append(42)
        def_operation()
        assert "x" in dict_stack[-1]
        assert dict_stack[-1]["x"] == 42
        assert len(op_stack) == 0

    def test_def_operation_insufficient_operands(self):
        op_stack.append("/x")
        with pytest.raises(TypeMismatch):
            def_operation()

    def test_def_operation_invalid_key(self):
        op_stack.append("x")  # Missing leading /
        op_stack.append(42)
        with pytest.raises(TypeMismatch):
            def_operation()

    def test_def_operation_repl(self):
        process_input("/x")
        process_input("10")
        process_input("def")
        assert "x" in dict_stack[-1]
        assert dict_stack[-1]["x"] == 10


class TestDictOperation:
    """Tests for the dict operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_dict_operation_creates_psdict(self):
        dict_operation()
        assert len(op_stack) == 1
        assert isinstance(op_stack[-1], PSDict)

    def test_dict_operation_repl(self):
        process_input("dict")
        assert len(op_stack) == 1
        assert isinstance(op_stack[-1], PSDict)


class TestBeginOperation:
    """Tests for the begin operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_begin_operation_valid(self):
        new_dict = PSDict()
        op_stack.append(new_dict)
        initial_dict_stack_len = len(dict_stack)
        begin_operation()
        assert len(dict_stack) == initial_dict_stack_len + 1
        assert dict_stack[-1] is new_dict
        assert len(op_stack) == 0

    def test_begin_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            begin_operation()

    def test_begin_operation_invalid_operand(self):
        op_stack.append(42)  # Not a dictionary
        with pytest.raises(TypeMismatch):
            begin_operation()

    def test_begin_operation_repl(self):
        process_input("/mydict")
        process_input("dict")
        process_input("def")
        process_input("mydict")
        initial_dict_stack_len = len(dict_stack)
        process_input("begin")
        assert len(dict_stack) == initial_dict_stack_len + 1


class TestEndOperation:
    """Tests for the end operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_end_operation_valid(self):
        new_dict = PSDict()
        dict_stack.append(new_dict)
        initial_dict_stack_len = len(dict_stack)
        end_operation()
        assert len(dict_stack) == initial_dict_stack_len - 1

    def test_end_operation_cannot_pop_last_dict(self):
        with pytest.raises(TypeMismatch):
            end_operation()

    def test_end_operation_repl(self):
        process_input("dict")
        process_input("begin")
        initial_dict_stack_len = len(dict_stack)
        process_input("end")
        assert len(dict_stack) == initial_dict_stack_len - 1


class TestLengthOperation:
    """Tests for the length operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_length_operation_empty_dict(self):
        new_dict = PSDict()
        op_stack.append(new_dict)
        length_operation()
        assert op_stack[-1] == 0

    def test_length_operation_with_items(self):
        new_dict = PSDict()
        new_dict["a"] = 1
        new_dict["b"] = 2
        new_dict["c"] = 3
        op_stack.append(new_dict)
        length_operation()
        assert op_stack[-1] == 3

    def test_length_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            length_operation()

    def test_length_operation_invalid_operand(self):
        op_stack.append(42)  # Not a dictionary
        with pytest.raises(TypeMismatch):
            length_operation()

    def test_length_operation_repl(self):
        process_input("dict")
        process_input("begin")
        process_input("/x")
        process_input("10")
        process_input("def")
        process_input("/y")
        process_input("20")
        process_input("def")
        process_input("end")
        # The dictionary should now be on the dict_stack, get it
        process_input("dict")  # Create a new dict to test
        new_dict = op_stack.pop()
        new_dict["key1"] = "value1"
        new_dict["key2"] = "value2"
        op_stack.append(new_dict)
        process_input("length")
        assert op_stack[-1] == 2


class TestMaxlengthOperation:
    """Tests for the maxlength operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_maxlength_operation_default(self):
        new_dict = PSDict()
        op_stack.append(new_dict)
        maxlength_operation()
        assert op_stack[-1] == 20  # Default max_length

    def test_maxlength_operation_with_items(self):
        new_dict = PSDict()
        new_dict["a"] = 1
        new_dict["b"] = 2
        op_stack.append(new_dict)
        maxlength_operation()
        assert op_stack[-1] == 20  # Should still be default max_length

    def test_maxlength_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            maxlength_operation()

    def test_maxlength_operation_invalid_operand(self):
        op_stack.append(42)  # Not a dictionary
        with pytest.raises(TypeMismatch):
            maxlength_operation()

    def test_maxlength_operation_repl(self):
        process_input("dict")
        process_input("maxlength")
        assert op_stack[-1] == 20
