"""
Tests for I/O operations.
"""

import pytest
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.core.exceptions import TypeMismatch
from src.operations.io_ops import (
    pop_print_operation,
    string_print_operation,
    pop_print_postscript_rep_operation,
)
from src.interpreter import register_builtin_operations


class TestPopPrintOperation:
    """Tests for the pop_print_operation (=)."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_pop_print_integer(self, capsys):
        """Test printing an integer."""
        op_stack.append(42)
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "42\n"
        assert len(op_stack) == 0

    def test_pop_print_float(self, capsys):
        """Test printing a float."""
        op_stack.append(3.14159)
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "3.14159\n"
        assert len(op_stack) == 0

    def test_pop_print_string(self, capsys):
        """Test printing a string."""
        op_stack.append("hello world")
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "hello world\n"
        assert len(op_stack) == 0

    def test_pop_print_boolean(self, capsys):
        """Test printing a boolean."""
        op_stack.append(True)
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "True\n"
        assert len(op_stack) == 0

    def test_pop_print_empty_string(self, capsys):
        """Test printing an empty string."""
        op_stack.append("")
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "\n"
        assert len(op_stack) == 0

    def test_pop_print_negative_number(self, capsys):
        """Test printing a negative number."""
        op_stack.append(-100)
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "-100\n"
        assert len(op_stack) == 0

    def test_pop_print_zero(self, capsys):
        """Test printing zero."""
        op_stack.append(0)
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "0\n"
        assert len(op_stack) == 0

    def test_pop_print_dict(self, capsys):
        """Test printing a dictionary."""
        op_stack.append({"a": 1, "b": 2})
        pop_print_operation()
        captured = capsys.readouterr()
        assert "a" in captured.out
        assert "b" in captured.out
        assert len(op_stack) == 0

    def test_pop_print_underflow(self):
        """Test pop_print_operation with empty stack."""
        with pytest.raises(TypeMismatch):
            pop_print_operation()

    def test_pop_print_multiple_calls(self, capsys):
        """Test multiple consecutive prints."""
        op_stack.append(1)
        op_stack.append(2)
        op_stack.append(3)
        pop_print_operation()
        pop_print_operation()
        pop_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "3\n2\n1\n"
        assert len(op_stack) == 0


class TestStringPrintOperation:
    """Tests for the string_print_operation (print)."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_string_print_basic(self, capsys):
        """Test printing a basic string."""
        op_stack.append("hello")
        string_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "hello\n"
        assert len(op_stack) == 0

    def test_string_print_with_spaces(self, capsys):
        """Test printing a string with spaces."""
        op_stack.append("hello world test")
        string_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "hello world test\n"
        assert len(op_stack) == 0

    def test_string_print_empty_string(self, capsys):
        """Test printing an empty string."""
        op_stack.append("")
        string_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "\n"
        assert len(op_stack) == 0

    def test_string_print_special_chars(self, capsys):
        """Test printing a string with special characters."""
        op_stack.append("hello\tworld\n")
        string_print_operation()
        captured = capsys.readouterr()
        assert "hello\tworld\n" in captured.out
        assert len(op_stack) == 0

    def test_string_print_numeric_string(self, capsys):
        """Test printing a string that looks like a number."""
        op_stack.append("12345")
        string_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "12345\n"
        assert len(op_stack) == 0

    def test_string_print_integer_type_error(self):
        """Test string_print_operation with an integer."""
        op_stack.append(42)
        with pytest.raises(TypeMismatch):
            string_print_operation()

    def test_string_print_float_type_error(self):
        """Test string_print_operation with a float."""
        op_stack.append(3.14)
        with pytest.raises(TypeMismatch):
            string_print_operation()

    def test_string_print_boolean_type_error(self):
        """Test string_print_operation with a boolean."""
        op_stack.append(True)
        with pytest.raises(TypeMismatch):
            string_print_operation()

    def test_string_print_dict_type_error(self):
        """Test string_print_operation with a dictionary."""
        op_stack.append({"a": 1})
        with pytest.raises(TypeMismatch):
            string_print_operation()

    def test_string_print_underflow(self):
        """Test string_print_operation with empty stack."""
        with pytest.raises(TypeMismatch):
            string_print_operation()

    def test_string_print_multiple_calls(self, capsys):
        """Test multiple consecutive string prints."""
        op_stack.append("first")
        op_stack.append("second")
        op_stack.append("third")
        string_print_operation()
        string_print_operation()
        string_print_operation()
        captured = capsys.readouterr()
        assert captured.out == "third\nsecond\nfirst\n"
        assert len(op_stack) == 0


class TestPopPrintPostscriptRepOperation:
    """Tests for the pop_print_postscript_rep_operation (==)."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_postscript_rep_integer(self, capsys):
        """Test PostScript representation of an integer."""
        op_stack.append(42)
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "42\n"
        assert len(op_stack) == 0

    def test_postscript_rep_float(self, capsys):
        """Test PostScript representation of a float."""
        op_stack.append(3.14159)
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "3.14159\n"
        assert len(op_stack) == 0

    def test_postscript_rep_string(self, capsys):
        """Test PostScript representation of a string (with parentheses)."""
        op_stack.append("hello")
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "(hello)\n"
        assert len(op_stack) == 0

    def test_postscript_rep_empty_string(self, capsys):
        """Test PostScript representation of an empty string."""
        op_stack.append("")
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "()\n"
        assert len(op_stack) == 0

    def test_postscript_rep_string_with_spaces(self, capsys):
        """Test PostScript representation of a string with spaces."""
        op_stack.append("hello world")
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "(hello world)\n"
        assert len(op_stack) == 0

    def test_postscript_rep_boolean(self, capsys):
        """Test PostScript representation of a boolean."""
        op_stack.append(True)
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "True\n"
        assert len(op_stack) == 0

    def test_postscript_rep_negative_number(self, capsys):
        """Test PostScript representation of a negative number."""
        op_stack.append(-50)
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "-50\n"
        assert len(op_stack) == 0

    def test_postscript_rep_zero(self, capsys):
        """Test PostScript representation of zero."""
        op_stack.append(0)
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "0\n"
        assert len(op_stack) == 0

    def test_postscript_rep_dict(self, capsys):
        """Test PostScript representation of a dictionary."""
        op_stack.append({"a": 1, "b": 2})
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert "a" in captured.out
        assert "b" in captured.out
        assert len(op_stack) == 0

    def test_postscript_rep_underflow(self):
        """Test pop_print_postscript_rep_operation with empty stack."""
        with pytest.raises(TypeMismatch):
            pop_print_postscript_rep_operation()

    def test_postscript_rep_multiple_calls(self, capsys):
        """Test multiple consecutive PostScript representation prints."""
        op_stack.append("first")
        op_stack.append(42)
        op_stack.append("last")
        pop_print_postscript_rep_operation()
        pop_print_postscript_rep_operation()
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "(last)\n42\n(first)\n"
        assert len(op_stack) == 0

    def test_postscript_rep_mixed_types(self, capsys):
        """Test PostScript representation with mixed types on stack."""
        op_stack.append(100)
        op_stack.append("test")
        op_stack.append(3.14)
        pop_print_postscript_rep_operation()
        captured = capsys.readouterr()
        assert captured.out == "3.14\n"
        assert len(op_stack) == 2
        assert op_stack[0] == 100
        assert op_stack[1] == "test"


class TestIOOperationsIntegration:
    """Integration tests for I/O operations."""

    def setup_method(self):
        """Reset the operand stack before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        register_builtin_operations()

    def test_all_three_operations(self, capsys):
        """Test using all three I/O operations together."""
        op_stack.append("hello")
        op_stack.append(42)
        op_stack.append("world")

        # Use = (pop_print_operation) - prints "world"
        pop_print_operation()
        # Use == (pop_print_postscript_rep_operation) - prints "42"
        pop_print_postscript_rep_operation()
        # Use print (string_print_operation) - prints "hello"
        string_print_operation()

        captured = capsys.readouterr()
        assert "world\n" in captured.out
        assert "42\n" in captured.out
        assert "hello\n" in captured.out
        assert len(op_stack) == 0

    def test_print_vs_postscript_rep_strings(self, capsys):
        """Test difference between print and == for strings."""
        # print shows string without parentheses
        op_stack.append("test")
        string_print_operation()
        captured1 = capsys.readouterr()
        assert captured1.out == "test\n"

        # == shows string with parentheses
        op_stack.append("test")
        pop_print_postscript_rep_operation()
        captured2 = capsys.readouterr()
        assert captured2.out == "(test)\n"

    def test_print_vs_equals_numbers(self, capsys):
        """Test that = and == work the same for numbers."""
        # = for numbers
        op_stack.append(100)
        pop_print_operation()
        captured1 = capsys.readouterr()

        # == for numbers
        op_stack.append(100)
        pop_print_postscript_rep_operation()
        captured2 = capsys.readouterr()

        assert captured1.out == captured2.out == "100\n"

    def test_sequential_prints(self, capsys):
        """Test sequential printing of different values."""
        for i in range(1, 6):
            op_stack.append(i)

        for _ in range(5):
            pop_print_operation()

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines == ["5", "4", "3", "2", "1"]
        assert len(op_stack) == 0

    def test_stack_preservation_on_error(self):
        """Test that stack is preserved when operation fails."""
        op_stack.append(1)
        op_stack.append(2)
        op_stack.append(3)

        with pytest.raises(TypeMismatch):
            string_print_operation()

        # Stack should still have all elements since operation failed
        assert len(op_stack) == 3
        assert op_stack[0] == 1
        assert op_stack[1] == 2
        assert op_stack[2] == 3
