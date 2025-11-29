"""Tests for flow control operations"""

import pytest
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.core.exceptions import TypeMismatch
from src.operations.flow_ops import (
    if_operation,
    ifelse_operation,
    repeat_operation,
)
from src.interpreter import process_input, register_builtin_operations


class TestIfOperation:
    """Tests for the if operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_if_operation_true_condition(self):
        op_stack.append(True)
        op_stack.append([1, 2, 3])
        if_operation()
        assert len(op_stack) == 3
        assert op_stack[-3] == 1
        assert op_stack[-2] == 2
        assert op_stack[-1] == 3

    def test_if_operation_false_condition(self):
        op_stack.append(False)
        op_stack.append([1, 2, 3])
        if_operation()
        assert len(op_stack) == 0

    def test_if_operation_truthy_value(self):
        op_stack.append(5)  # Non-zero is truthy
        op_stack.append([10, 20])
        if_operation()
        assert len(op_stack) == 2
        assert op_stack[-2] == 10
        assert op_stack[-1] == 20

    def test_if_operation_falsy_value(self):
        op_stack.append(0)  # Zero is falsy
        op_stack.append([10, 20])
        if_operation()
        assert len(op_stack) == 0

    def test_if_operation_empty_code_block(self):
        op_stack.append(True)
        op_stack.append([])
        if_operation()
        assert len(op_stack) == 0

    def test_if_operation_insufficient_operands(self):
        op_stack.append(True)
        with pytest.raises(TypeMismatch):
            if_operation()

    def test_if_operation_non_list_code_block(self):
        op_stack.append(True)
        op_stack.append(42)
        with pytest.raises(TypeMismatch):
            if_operation()

    def test_if_operation_repl(self):
        process_input("3")
        process_input("2")
        process_input("gt")
        process_input("{ 100 }")
        process_input("if")
        assert op_stack[-1] == "100"  # Code blocks push strings


class TestIfelseOperation:
    """Tests for the ifelse operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_ifelse_operation_true_condition(self):
        op_stack.append(True)
        op_stack.append([1, 2])
        op_stack.append([3, 4])
        ifelse_operation()
        assert len(op_stack) == 2
        assert op_stack[-2] == 1
        assert op_stack[-1] == 2

    def test_ifelse_operation_false_condition(self):
        op_stack.append(False)
        op_stack.append([1, 2])
        op_stack.append([3, 4])
        ifelse_operation()
        assert len(op_stack) == 2
        assert op_stack[-2] == 3
        assert op_stack[-1] == 4

    def test_ifelse_operation_truthy_value(self):
        op_stack.append(10)  # Non-zero is truthy
        op_stack.append([100])
        op_stack.append([200])
        ifelse_operation()
        assert len(op_stack) == 1
        assert op_stack[-1] == 100

    def test_ifelse_operation_falsy_value(self):
        op_stack.append(0)  # Zero is falsy
        op_stack.append([100])
        op_stack.append([200])
        ifelse_operation()
        assert len(op_stack) == 1
        assert op_stack[-1] == 200

    def test_ifelse_operation_empty_if_block(self):
        op_stack.append(True)
        op_stack.append([])
        op_stack.append([5, 6])
        ifelse_operation()
        assert len(op_stack) == 0

    def test_ifelse_operation_empty_else_block(self):
        op_stack.append(False)
        op_stack.append([5, 6])
        op_stack.append([])
        ifelse_operation()
        assert len(op_stack) == 0

    def test_ifelse_operation_both_blocks_empty(self):
        op_stack.append(True)
        op_stack.append([])
        op_stack.append([])
        ifelse_operation()
        assert len(op_stack) == 0

    def test_ifelse_operation_insufficient_operands(self):
        op_stack.append(True)
        op_stack.append([1, 2])
        with pytest.raises(TypeMismatch):
            ifelse_operation()

    def test_ifelse_operation_non_list_if_block(self):
        op_stack.append(True)
        op_stack.append(42)
        op_stack.append([3, 4])
        with pytest.raises(TypeMismatch):
            ifelse_operation()

    def test_ifelse_operation_non_list_else_block(self):
        op_stack.append(True)
        op_stack.append([1, 2])
        op_stack.append(42)
        with pytest.raises(TypeMismatch):
            ifelse_operation()

    def test_ifelse_operation_repl(self):
        process_input("5")
        process_input("10")
        process_input("gt")
        process_input("{ 100 }")
        process_input("{ 200 }")
        process_input("ifelse")
        assert op_stack[-1] == "200"  # Code blocks push strings


class TestRepeatOperation:
    """Tests for the repeat operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_repeat_operation_valid(self):
        op_stack.append(3)
        op_stack.append([5, 10])
        repeat_operation()
        assert len(op_stack) == 6
        assert op_stack == [5, 10, 5, 10, 5, 10]

    def test_repeat_operation_once(self):
        op_stack.append(1)
        op_stack.append([42])
        repeat_operation()
        assert len(op_stack) == 1
        assert op_stack[-1] == 42

    def test_repeat_operation_zero_times(self):
        op_stack.append(0)
        op_stack.append([1, 2, 3])
        repeat_operation()
        assert len(op_stack) == 0

    def test_repeat_operation_empty_code_block(self):
        op_stack.append(5)
        op_stack.append([])
        repeat_operation()
        assert len(op_stack) == 0

    def test_repeat_operation_single_element(self):
        op_stack.append(4)
        op_stack.append([7])
        repeat_operation()
        assert len(op_stack) == 4
        assert op_stack == [7, 7, 7, 7]

    def test_repeat_operation_large_count(self):
        op_stack.append(100)
        op_stack.append([1])
        repeat_operation()
        assert len(op_stack) == 100
        assert all(x == 1 for x in op_stack)

    def test_repeat_operation_insufficient_operands(self):
        op_stack.append(3)
        with pytest.raises(TypeMismatch):
            repeat_operation()

    def test_repeat_operation_non_list_code_block(self):
        op_stack.append(3)
        op_stack.append(42)
        with pytest.raises(TypeMismatch):
            repeat_operation()

    def test_repeat_operation_non_integer_count(self):
        op_stack.append(3.5)
        op_stack.append([1, 2])
        with pytest.raises(TypeMismatch):
            repeat_operation()

    def test_repeat_operation_negative_count(self):
        op_stack.append(-1)
        op_stack.append([1, 2])
        with pytest.raises(TypeMismatch):
            repeat_operation()

    def test_repeat_operation_repl(self):
        process_input("3")
        process_input("{ 5 10 }")
        process_input("repeat")
        assert len(op_stack) == 6
        assert op_stack == ["5", "10", "5", "10", "5", "10"]  # Code blocks push strings


class TestCombinedFlowOperations:
    """Tests for combined flow control operations."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_nested_if_operations(self):
        # if (true) { if (true) { 100 } }
        op_stack.append(True)
        op_stack.append([True, [100], "if"])
        if_operation()
        # Now we need to process the items that were pushed
        assert True in op_stack
        assert [100] in op_stack
        assert "if" in op_stack

    def test_if_with_comparison(self):
        # 5 > 3 then push 100
        process_input("5")
        process_input("3")
        process_input("gt")
        process_input("{ 100 }")
        process_input("if")
        assert op_stack[-1] == "100"  # Code blocks push strings

    def test_ifelse_with_comparison(self):
        # 2 > 5 ? push 100 : push 200
        process_input("2")
        process_input("5")
        process_input("gt")
        process_input("{ 100 }")
        process_input("{ 200 }")
        process_input("ifelse")
        assert op_stack[-1] == "200"  # Code blocks push strings

    def test_repeat_with_arithmetic(self):
        # Repeat 3 times: push 5
        process_input("3")
        process_input("{ 5 }")
        process_input("repeat")
        # Should have ["5", "5", "5"] on stack (strings from code block)
        assert len(op_stack) == 3
        assert all(x == "5" for x in op_stack)

    def test_complex_flow_combination(self):
        # if (10 > 5) { repeat 2 times: push 7 }
        op_stack.append(10)
        op_stack.append(5)
        process_input("gt")
        op_stack.append([2, [7], "repeat"])
        if_operation()
        # Items from the if block should be on stack
        assert 2 in op_stack
        assert [7] in op_stack
        assert "repeat" in op_stack
