import pytest
from src.parsers.parsers import (
    process_boolean,
    process_number,
    process_name_constant,
    process_code_block,
)
from src.core.exceptions import ParseFailed, TypeMismatch
from src.core.stacks import op_stack, dict_stack
from src.core.psdict import PSDict
from src.operations.arithmetic_ops import add_operation, mul_operation
from src.operations.io_ops import pop_print_operation
from src.operations.dict_ops import (
    def_operation,
    dict_operation,
    begin_operation,
    end_operation,
)
from src.interpreter import process_input, register_builtin_operations


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
        result = process_number("42")
        assert result == 42
        assert isinstance(result, int)

    def test_parse_float(self):
        result = process_number("3.14")
        assert result == 3.14
        assert isinstance(result, float)

    def test_parse_invalid(self):
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
        assert op_stack[-1] == 30  # Check the stack directly instead


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


class TestCodeBlockParsing:
    """Tests for code block parsing functions."""

    def test_parse_code_block(self):
        result = process_code_block("{ 1 2 add }")
        assert result == ["1", "2", "add"]

    def test_parse_invalid_code_block(self):
        with pytest.raises(ParseFailed):
            process_code_block("notacodeblock")


class TestNameConstantParsing:
    """Tests for name constant parsing functions."""

    def test_parse_name_constant(self):
        result = process_name_constant("/myvar")
        assert result == "/myvar"

    def test_parse_invalid_name_constant(self):
        with pytest.raises(ParseFailed):
            process_name_constant("myvar")


class TestDefOperation:
    """Tests for the def operation."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        # Re-register built-in operations
        dict_stack[-1]["add"] = add_operation
        dict_stack[-1]["mul"] = mul_operation
        dict_stack[-1]["="] = pop_print_operation
        dict_stack[-1]["def"] = def_operation
        dict_stack[-1]["dict"] = dict_operation
        dict_stack[-1]["begin"] = begin_operation
        dict_stack[-1]["end"] = end_operation

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
        # Re-register built-in operations
        dict_stack[-1]["add"] = add_operation
        dict_stack[-1]["mul"] = mul_operation
        dict_stack[-1]["="] = pop_print_operation
        dict_stack[-1]["def"] = def_operation
        dict_stack[-1]["dict"] = dict_operation
        dict_stack[-1]["begin"] = begin_operation
        dict_stack[-1]["end"] = end_operation

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
        # Re-register built-in operations
        dict_stack[-1]["add"] = add_operation
        dict_stack[-1]["mul"] = mul_operation
        dict_stack[-1]["="] = pop_print_operation
        dict_stack[-1]["def"] = def_operation
        dict_stack[-1]["dict"] = dict_operation
        dict_stack[-1]["begin"] = begin_operation
        dict_stack[-1]["end"] = end_operation

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
        # Re-register built-in operations
        dict_stack[-1]["add"] = add_operation
        dict_stack[-1]["mul"] = mul_operation
        dict_stack[-1]["="] = pop_print_operation
        dict_stack[-1]["def"] = def_operation
        dict_stack[-1]["dict"] = dict_operation
        dict_stack[-1]["begin"] = begin_operation
        dict_stack[-1]["end"] = end_operation

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


class TestDictionaryScoping:
    """Tests for dictionary scoping and nested dictionaries."""

    def setup_method(self):
        """Reset stacks before each test."""
        op_stack.clear()
        dict_stack.clear()
        dict_stack.append(PSDict())
        # Re-register built-in operations
        dict_stack[-1]["add"] = add_operation
        dict_stack[-1]["mul"] = mul_operation
        dict_stack[-1]["="] = pop_print_operation
        dict_stack[-1]["def"] = def_operation
        dict_stack[-1]["dict"] = dict_operation
        dict_stack[-1]["begin"] = begin_operation
        dict_stack[-1]["end"] = end_operation

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
        # Re-register built-in operations
        dict_stack[-1]["add"] = add_operation
        dict_stack[-1]["mul"] = mul_operation
        dict_stack[-1]["="] = pop_print_operation
        dict_stack[-1]["def"] = def_operation
        dict_stack[-1]["dict"] = dict_operation
        dict_stack[-1]["begin"] = begin_operation
        dict_stack[-1]["end"] = end_operation

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
