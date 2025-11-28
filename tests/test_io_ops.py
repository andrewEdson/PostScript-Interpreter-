"""Tests for I/O operations"""

import pytest
from src.core.stacks import op_stack
from src.core.exceptions import TypeMismatch
from src.operations.io_ops import pop_print_operation


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
