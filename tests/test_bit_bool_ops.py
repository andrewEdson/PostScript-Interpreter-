"""Tests for bit and boolean operations"""

import pytest
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.core.exceptions import TypeMismatch
from src.operations.bit_bool_ops import (
    eq_operation,
    ne_operation,
    ge_operation,
    gt_operation,
    le_operation,
    lt_operation,
    and_operation,
    or_operation,
    not_operation,
    true_operation,
    false_operation,
)
from src.interpreter import process_input, register_builtin_operations


class TestEqOperation:
    """Tests for the eq (equal) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_eq_operation_numbers_equal(self):
        op_stack.append(5)
        op_stack.append(5)
        eq_operation()
        assert op_stack[-1] is True

    def test_eq_operation_numbers_not_equal(self):
        op_stack.append(5)
        op_stack.append(3)
        eq_operation()
        assert op_stack[-1] is False

    def test_eq_operation_strings_equal(self):
        op_stack.append("hello")
        op_stack.append("hello")
        eq_operation()
        assert op_stack[-1] is True

    def test_eq_operation_strings_not_equal(self):
        op_stack.append("hello")
        op_stack.append("world")
        eq_operation()
        assert op_stack[-1] is False

    def test_eq_operation_booleans(self):
        op_stack.append(True)
        op_stack.append(True)
        eq_operation()
        assert op_stack[-1] is True

    def test_eq_operation_insufficient_operands(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            eq_operation()

    def test_eq_operation_repl(self):
        process_input("10")
        process_input("10")
        process_input("eq")
        assert op_stack[-1] is True


class TestNeOperation:
    """Tests for the ne (not equal) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_ne_operation_numbers_not_equal(self):
        op_stack.append(5)
        op_stack.append(3)
        ne_operation()
        assert op_stack[-1] is True

    def test_ne_operation_numbers_equal(self):
        op_stack.append(5)
        op_stack.append(5)
        ne_operation()
        assert op_stack[-1] is False

    def test_ne_operation_strings_not_equal(self):
        op_stack.append("hello")
        op_stack.append("world")
        ne_operation()
        assert op_stack[-1] is True

    def test_ne_operation_strings_equal(self):
        op_stack.append("test")
        op_stack.append("test")
        ne_operation()
        assert op_stack[-1] is False

    def test_ne_operation_insufficient_operands(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            ne_operation()

    def test_ne_operation_repl(self):
        process_input("5")
        process_input("10")
        process_input("ne")
        assert op_stack[-1] is True


class TestGeOperation:
    """Tests for the ge (greater than or equal) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_ge_operation_greater(self):
        op_stack.append(10)
        op_stack.append(5)
        ge_operation()
        assert op_stack[-1] is True

    def test_ge_operation_equal(self):
        op_stack.append(5)
        op_stack.append(5)
        ge_operation()
        assert op_stack[-1] is True

    def test_ge_operation_less(self):
        op_stack.append(3)
        op_stack.append(10)
        ge_operation()
        assert op_stack[-1] is False

    def test_ge_operation_insufficient_operands(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            ge_operation()

    def test_ge_operation_incomparable_types(self):
        op_stack.append("hello")
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            ge_operation()

    def test_ge_operation_repl(self):
        process_input("10")
        process_input("5")
        process_input("ge")
        assert op_stack[-1] is True


class TestGtOperation:
    """Tests for the gt (greater than) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_gt_operation_greater(self):
        op_stack.append(10)
        op_stack.append(5)
        gt_operation()
        assert op_stack[-1] is True

    def test_gt_operation_equal(self):
        op_stack.append(5)
        op_stack.append(5)
        gt_operation()
        assert op_stack[-1] is False

    def test_gt_operation_less(self):
        op_stack.append(3)
        op_stack.append(10)
        gt_operation()
        assert op_stack[-1] is False

    def test_gt_operation_insufficient_operands(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            gt_operation()

    def test_gt_operation_incomparable_types(self):
        op_stack.append("hello")
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            gt_operation()

    def test_gt_operation_repl(self):
        process_input("10")
        process_input("5")
        process_input("gt")
        assert op_stack[-1] is True


class TestLeOperation:
    """Tests for the le (less than or equal) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_le_operation_less(self):
        op_stack.append(3)
        op_stack.append(10)
        le_operation()
        assert op_stack[-1] is True

    def test_le_operation_equal(self):
        op_stack.append(5)
        op_stack.append(5)
        le_operation()
        assert op_stack[-1] is True

    def test_le_operation_greater(self):
        op_stack.append(10)
        op_stack.append(5)
        le_operation()
        assert op_stack[-1] is False

    def test_le_operation_insufficient_operands(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            le_operation()

    def test_le_operation_incomparable_types(self):
        op_stack.append("hello")
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            le_operation()

    def test_le_operation_repl(self):
        process_input("3")
        process_input("10")
        process_input("le")
        assert op_stack[-1] is True


class TestLtOperation:
    """Tests for the lt (less than) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_lt_operation_less(self):
        op_stack.append(3)
        op_stack.append(10)
        lt_operation()
        assert op_stack[-1] is True

    def test_lt_operation_equal(self):
        op_stack.append(5)
        op_stack.append(5)
        lt_operation()
        assert op_stack[-1] is False

    def test_lt_operation_greater(self):
        op_stack.append(10)
        op_stack.append(5)
        lt_operation()
        assert op_stack[-1] is False

    def test_lt_operation_insufficient_operands(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            lt_operation()

    def test_lt_operation_incomparable_types(self):
        op_stack.append("hello")
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            lt_operation()

    def test_lt_operation_repl(self):
        process_input("3")
        process_input("10")
        process_input("lt")
        assert op_stack[-1] is True


class TestAndOperation:
    """Tests for the and (logical and) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_and_operation_true_true(self):
        op_stack.append(True)
        op_stack.append(True)
        and_operation()
        assert op_stack[-1] is True

    def test_and_operation_true_false(self):
        op_stack.append(True)
        op_stack.append(False)
        and_operation()
        assert op_stack[-1] is False

    def test_and_operation_false_true(self):
        op_stack.append(False)
        op_stack.append(True)
        and_operation()
        assert op_stack[-1] is False

    def test_and_operation_false_false(self):
        op_stack.append(False)
        op_stack.append(False)
        and_operation()
        assert op_stack[-1] is False

    def test_and_operation_insufficient_operands(self):
        op_stack.append(True)
        with pytest.raises(TypeMismatch):
            and_operation()

    def test_and_operation_non_boolean_operands(self):
        op_stack.append(5)
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            and_operation()

    def test_and_operation_repl(self):
        process_input("true")
        process_input("false")
        process_input("and")
        assert op_stack[-1] is False


class TestOrOperation:
    """Tests for the or (logical or) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_or_operation_true_true(self):
        op_stack.append(True)
        op_stack.append(True)
        or_operation()
        assert op_stack[-1] is True

    def test_or_operation_true_false(self):
        op_stack.append(True)
        op_stack.append(False)
        or_operation()
        assert op_stack[-1] is True

    def test_or_operation_false_true(self):
        op_stack.append(False)
        op_stack.append(True)
        or_operation()
        assert op_stack[-1] is True

    def test_or_operation_false_false(self):
        op_stack.append(False)
        op_stack.append(False)
        or_operation()
        assert op_stack[-1] is False

    def test_or_operation_insufficient_operands(self):
        op_stack.append(True)
        with pytest.raises(TypeMismatch):
            or_operation()

    def test_or_operation_non_boolean_operands(self):
        op_stack.append(5)
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            or_operation()

    def test_or_operation_repl(self):
        process_input("true")
        process_input("false")
        process_input("or")
        assert op_stack[-1] is True


class TestNotOperation:
    """Tests for the not (logical not) operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_not_operation_true(self):
        op_stack.append(True)
        not_operation()
        assert op_stack[-1] is False

    def test_not_operation_false(self):
        op_stack.append(False)
        not_operation()
        assert op_stack[-1] is True

    def test_not_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            not_operation()

    def test_not_operation_non_boolean_operand(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            not_operation()

    def test_not_operation_repl(self):
        process_input("true")
        process_input("not")
        assert op_stack[-1] is False


class TestTrueOperation:
    """Tests for the true constant operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_true_operation(self):
        true_operation()
        assert op_stack[-1] is True
        assert len(op_stack) == 1

    def test_true_operation_multiple_calls(self):
        true_operation()
        true_operation()
        assert len(op_stack) == 2
        assert op_stack[-1] is True
        assert op_stack[-2] is True

    def test_true_operation_repl(self):
        process_input("true")
        assert op_stack[-1] is True


class TestFalseOperation:
    """Tests for the false constant operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_false_operation(self):
        false_operation()
        assert op_stack[-1] is False
        assert len(op_stack) == 1

    def test_false_operation_multiple_calls(self):
        false_operation()
        false_operation()
        assert len(op_stack) == 2
        assert op_stack[-1] is False
        assert op_stack[-2] is False

    def test_false_operation_repl(self):
        process_input("false")
        assert op_stack[-1] is False


class TestCombinedOperations:
    """Tests for combined boolean and comparison operations."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_combined_comparison_and_boolean(self):
        # (5 > 3) and (10 < 20)
        process_input("5")
        process_input("3")
        process_input("gt")
        process_input("10")
        process_input("20")
        process_input("lt")
        process_input("and")
        assert op_stack[-1] is True

    def test_combined_with_not(self):
        # not (5 == 3)
        process_input("5")
        process_input("3")
        process_input("eq")
        process_input("not")
        assert op_stack[-1] is True

    def test_complex_boolean_expression(self):
        # (true and false) or true
        process_input("true")
        process_input("false")
        process_input("and")
        process_input("true")
        process_input("or")
        assert op_stack[-1] is True
