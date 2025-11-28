"""Tests for parser functions"""

import pytest
from src.parsers.parsers import (
    process_boolean,
    process_number,
    process_name_constant,
    process_code_block,
)
from src.core.exceptions import ParseFailed


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


class TestNameConstantParsing:
    """Tests for name constant parsing functions."""

    def test_parse_name_constant(self):
        result = process_name_constant("/myvar")
        assert result == "/myvar"

    def test_parse_invalid_name_constant(self):
        with pytest.raises(ParseFailed):
            process_name_constant("myvar")


class TestCodeBlockParsing:
    """Tests for code block parsing functions."""

    def test_parse_code_block(self):
        result = process_code_block("{ 1 2 add }")
        assert result == ["1", "2", "add"]

    def test_parse_invalid_code_block(self):
        with pytest.raises(ParseFailed):
            process_code_block("notacodeblock")
