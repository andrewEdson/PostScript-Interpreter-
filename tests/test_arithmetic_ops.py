"""Tests for arithmetic operations"""

import pytest
import math
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.core.exceptions import TypeMismatch
from src.operations.arithmetic_ops import (
    add_operation,
    mul_operation,
    div_operation,
    sub_operation,
    idiv_operation,
    mod_operation,
    abs_operation,
    neg_operation,
    ceil_operation,
    floor_operation,
    round_operation,
    sqrt_operation,
)
from src.interpreter import process_input, register_builtin_operations


class TestAddOperation:
    """Tests for the add operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_add_operation_valid(self):
        op_stack.append(10)
        op_stack.append(20)
        add_operation()
        assert op_stack[-1] == 30

    def test_add_operation_insufficient_operands(self):
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            add_operation()

    def test_add_operation_repl(self):
        process_input("10")
        process_input("20")
        process_input("add")
        assert op_stack[-1] == 30


class TestMulOperation:
    """Tests for the multiply operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()

    def test_mul_operation_valid(self):
        op_stack.append(5)
        op_stack.append(4)
        mul_operation()
        assert op_stack[-1] == 20

    def test_mul_operation_insufficient_operands(self):
        op_stack.append(5)
        with pytest.raises(TypeMismatch):
            mul_operation()


class TestDivOperation:
    """Tests for the division operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_div_operation_valid(self):
        op_stack.append(20)
        op_stack.append(4)
        div_operation()
        assert op_stack[-1] == 5.0

    def test_div_operation_float_result(self):
        op_stack.append(10)
        op_stack.append(4)
        div_operation()
        assert op_stack[-1] == 2.5

    def test_div_operation_zero_division(self):
        op_stack.append(10)
        op_stack.append(0)
        with pytest.raises(TypeMismatch):
            div_operation()

    def test_div_operation_insufficient_operands(self):
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            div_operation()

    def test_div_operation_repl(self):
        process_input("20")
        process_input("4")
        process_input("div")
        assert op_stack[-1] == 5.0


class TestSubOperation:
    """Tests for the subtraction operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_sub_operation_valid(self):
        op_stack.append(20)
        op_stack.append(5)
        sub_operation()
        assert op_stack[-1] == 15

    def test_sub_operation_negative_result(self):
        op_stack.append(5)
        op_stack.append(10)
        sub_operation()
        assert op_stack[-1] == -5

    def test_sub_operation_insufficient_operands(self):
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            sub_operation()

    def test_sub_operation_repl(self):
        process_input("50")
        process_input("20")
        process_input("sub")
        assert op_stack[-1] == 30


class TestIdivOperation:
    """Tests for the integer division operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_idiv_operation_valid(self):
        op_stack.append(20)
        op_stack.append(4)
        idiv_operation()
        assert op_stack[-1] == 5

    def test_idiv_operation_truncates(self):
        op_stack.append(10)
        op_stack.append(3)
        idiv_operation()
        assert op_stack[-1] == 3

    def test_idiv_operation_zero_division(self):
        op_stack.append(10)
        op_stack.append(0)
        with pytest.raises(TypeMismatch):
            idiv_operation()

    def test_idiv_operation_insufficient_operands(self):
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            idiv_operation()

    def test_idiv_operation_repl(self):
        process_input("10")
        process_input("3")
        process_input("idiv")
        assert op_stack[-1] == 3


class TestModOperation:
    """Tests for the modulus operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_mod_operation_valid(self):
        op_stack.append(10)
        op_stack.append(3)
        mod_operation()
        assert op_stack[-1] == 1

    def test_mod_operation_zero_remainder(self):
        op_stack.append(10)
        op_stack.append(5)
        mod_operation()
        assert op_stack[-1] == 0

    def test_mod_operation_zero_division(self):
        op_stack.append(10)
        op_stack.append(0)
        with pytest.raises(TypeMismatch):
            mod_operation()

    def test_mod_operation_insufficient_operands(self):
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            mod_operation()

    def test_mod_operation_repl(self):
        process_input("17")
        process_input("5")
        process_input("mod")
        assert op_stack[-1] == 2


class TestAbsOperation:
    """Tests for the absolute value operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_abs_operation_positive(self):
        op_stack.append(42)
        abs_operation()
        assert op_stack[-1] == 42

    def test_abs_operation_negative(self):
        op_stack.append(-42)
        abs_operation()
        assert op_stack[-1] == 42

    def test_abs_operation_zero(self):
        op_stack.append(0)
        abs_operation()
        assert op_stack[-1] == 0

    def test_abs_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            abs_operation()

    def test_abs_operation_repl(self):
        process_input("-15")
        process_input("abs")
        assert op_stack[-1] == 15


class TestNegOperation:
    """Tests for the negation operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_neg_operation_positive(self):
        op_stack.append(42)
        neg_operation()
        assert op_stack[-1] == -42

    def test_neg_operation_negative(self):
        op_stack.append(-42)
        neg_operation()
        assert op_stack[-1] == 42

    def test_neg_operation_zero(self):
        op_stack.append(0)
        neg_operation()
        assert op_stack[-1] == 0

    def test_neg_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            neg_operation()

    def test_neg_operation_repl(self):
        process_input("25")
        process_input("neg")
        assert op_stack[-1] == -25


class TestCeilOperation:
    """Tests for the ceiling operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_ceil_operation_positive_decimal(self):
        op_stack.append(3.2)
        ceil_operation()
        assert op_stack[-1] == 4

    def test_ceil_operation_negative_decimal(self):
        op_stack.append(-4.8)
        ceil_operation()
        assert op_stack[-1] == -4

    def test_ceil_operation_integer(self):
        op_stack.append(5)
        ceil_operation()
        assert op_stack[-1] == 5

    def test_ceil_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            ceil_operation()

    def test_ceil_operation_repl(self):
        process_input("3.7")
        process_input("ceiling")
        assert op_stack[-1] == 4


class TestFloorOperation:
    """Tests for the floor operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_floor_operation_positive_decimal(self):
        op_stack.append(3.8)
        floor_operation()
        assert op_stack[-1] == 3

    def test_floor_operation_negative_decimal(self):
        op_stack.append(-4.2)
        floor_operation()
        assert op_stack[-1] == -5

    def test_floor_operation_integer(self):
        op_stack.append(5)
        floor_operation()
        assert op_stack[-1] == 5

    def test_floor_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            floor_operation()

    def test_floor_operation_repl(self):
        process_input("3.2")
        process_input("floor")
        assert op_stack[-1] == 3


class TestRoundOperation:
    """Tests for the round operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_round_operation_up(self):
        op_stack.append(3.7)
        round_operation()
        assert op_stack[-1] == 4

    def test_round_operation_down(self):
        op_stack.append(3.2)
        round_operation()
        assert op_stack[-1] == 3

    def test_round_operation_half(self):
        op_stack.append(3.5)
        round_operation()
        assert op_stack[-1] == 4

    def test_round_operation_integer(self):
        op_stack.append(5)
        round_operation()
        assert op_stack[-1] == 5

    def test_round_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            round_operation()

    def test_round_operation_repl(self):
        process_input("3.6")
        process_input("round")
        assert op_stack[-1] == 4


class TestSqrtOperation:
    """Tests for the square root operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_sqrt_operation_perfect_square(self):
        op_stack.append(16)
        sqrt_operation()
        assert op_stack[-1] == 4.0

    def test_sqrt_operation_non_perfect_square(self):
        op_stack.append(2)
        sqrt_operation()
        assert abs(op_stack[-1] - math.sqrt(2)) < 0.0001

    def test_sqrt_operation_zero(self):
        op_stack.append(0)
        sqrt_operation()
        assert op_stack[-1] == 0.0

    def test_sqrt_operation_negative(self):
        op_stack.append(-4)
        with pytest.raises(TypeMismatch):
            sqrt_operation()

    def test_sqrt_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            sqrt_operation()

    def test_sqrt_operation_repl(self):
        process_input("25")
        process_input("sqrt")
        assert op_stack[-1] == 5.0
