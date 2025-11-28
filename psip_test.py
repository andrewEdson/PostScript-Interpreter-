import pytest
from psip import (
    process_boolean,
    ParseFailed,
    process_number,
    process_input,
    op_stack,
    add_operation,
    pop_print_operation,
    mul_operation,
    TypeMismatch,
)


class TestBooleanParsing:
    """Tests for boolean parsing functions."""

    def test_parse_true(self):
        result = process_boolean("true")
        assert result is True

    def test_parse_false(self):
        result = process_boolean("false")
        assert result is False

    def test_parse_invalid(self):
        with pytest.raises(ParseFailed):
            process_boolean("notabool")


class TestNumberParsing:
    """Tests for number parsing functions."""

    def test_parse_integer(self):
        from psip import process_number

        result = process_number("42")
        assert result == 42
        assert isinstance(result, int)

    def test_parse_float(self):
        from psip import process_number

        result = process_number("3.14")
        assert result == 3.14
        assert isinstance(result, float)

    def test_parse_invalid(self):
        from psip import ParseFailed

        with pytest.raises(ParseFailed):
            process_number("notanumber")


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


class TestAddOperation:
    """Tests for the add operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()

    def test_add_operation_valid(self):
        op_stack.append(10)
        op_stack.append(20)
        add_operation()
        assert op_stack[-1] == 30

    def test_add_operation_insufficient_operands(self):
        op_stack.append(10)
        with pytest.raises(TypeMismatch):
            add_operation()


class TestPopPrintOperation:
    """Tests for the pop and print operation."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()

    def test_pop_print_operation_valid(self, capsys):
        op_stack.append(42)
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out.strip() == "42"
        assert len(op_stack) == 0  # Stack should be empty after pop

    def test_pop_print_operation_insufficient_operands(self):
        with pytest.raises(TypeMismatch):
            pop_print_operation()


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
