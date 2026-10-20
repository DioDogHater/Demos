from __future__ import annotations
from typing import override

import re
from collections.abc import Callable
from enum import IntEnum
from types import NoneType

"""
This module englobes the lexical analysis step of the compiler.
Its purpose is to read source code and turn it into a stream of atomic tokens.
"""

class TkType(IntEnum):
    """Different categories of tokens."""
    NAME = 0
    INT = 1
    FLOAT = 2
    CHAR = 3
    STRING = 4
    OPERATOR = 5
    UNKNOWN = -1

class Token:
    """
    Represents an atomic symbol in the code.
    """
    def __init__(self, type : TkType, value : str, line : int, offset : int) -> None:
        """Creates a Token with its attributes."""
        if not isinstance(type, TkType) or not isinstance(value, str) or not isinstance(line, int) or not isinstance(offset, int):
            raise TypeError(f"Mismatched types for Token({type} : TkType, {value} : str, {line} : int, {offset} : int)")
        self.__type : TkType = type
        self.__value : str = value
        self.__line : int = line
        self.__offset : int = offset

    @property
    def type(self) -> TkType:
        """The category of the token."""
        return self.__type

    @property
    def value(self) -> str:
        """The string that is represented by the Token interface."""
        return self.__value

    @property
    def line(self) -> int:
        """The line number where the Token is located."""
        return self.__line

    @property
    def offset(self) -> int:
        """The number of characters before the token since the start of line."""
        return self.__offset

    def criteria(self, type : TkType | tuple[TkType] | None = None, value : str | tuple[str] | Callable[[str], bool] | None = None) -> bool:
        if not isinstance(type, (TkType, tuple, NoneType)) or not (isinstance(value, (str, tuple, NoneType)) or callable(value)):
            raise TypeError(f"Mismatched types for Token.criteria({type} : TkType | ..., {value} : str | ...)")

        if isinstance(value, str) and self.value != value or \
           isinstance(value, tuple) and not (self.value in value) or \
           callable(value) and not value(self.value):
            return False

        return not (isinstance(type, TkType) and self.type != type or isinstance(type, tuple) and not self.type in type)

    def __eq__(self, other : object) -> bool:
        return isinstance(other, Token) and other.type == self.type and other.value == self.value

    def __repr__(self) -> str:
        return f"Token({self.type.name}, \"{self.value}\", {self.line}, {self.offset})"

class VirtualToken(Token):
    def __init__(self, value : str, type : TkType = TkType.UNKNOWN):
        super().__init__(type, value, -1, -1)

class LexerError(Exception):
    """Error during lexical analysis."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ContextError(Exception):
    """Exception thrown when a token's context is used to display where the error is."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Lexer:
    """
    The Lexer is in charge of analysing the source code and tokenizing it.
    It owns the tokens and only offers access to them via a peeking / consuming system.
    """

    operators : re.Pattern = re.compile(r"[><]{2}|[><]=?|[=~]?=|/_=?|[!\+\-\*/%&\|\^]=?|[\[\]\{\}\(\).,:;]")

    def __init__(self, source : str, name : str = "unknown") -> None:
        """
        Creates the Lexer.
        Args:
            source (str) : The source code to analyse.
            name (str) : The name of the file / source where the code comes from.
        """
        if not isinstance(source, str) or not isinstance(name, str):
            raise TypeError(f"Mismatched type for Lexer({source} : str)")
        self.__source : str = source
        self.__name : str = name
        self.__tokens : list[Token] = []
        self.__cursor = -1

    @property
    def source(self) -> str:
        return self.__source

    @property
    def name(self) -> str:
        return self.__name

    def rewind(self) -> None:
        """Reinitializes the current position in the token stream."""
        self.__cursor = -1

    def extend(self, lex : Lexer) -> None:
        """Appends the tokens of the other lexer to this lexer."""
        self.__tokens.extend(lex.__tokens)

    @property
    def current(self) -> Token | None:
        """The current token in the token stream."""
        return self.__tokens[self.__cursor] if 0 <= self.__cursor < self.token_count else None

    @property
    def cursor(self) -> int:
        return self.__cursor

    @property
    def tokens(self) -> list[Token]:
        # TODO Remove this
        return self.__tokens

    @property
    def token_count(self) -> int:
        """Number of tokens."""
        return len(self.__tokens)

    def peek(self, n : int = 1, type : TkType | tuple[TkType] | None = None, value : str | tuple[str] | Callable[[str], bool] | None = None) -> Token | None:
        """
        Peeks at the nth next token in the token stream.
        When n is negative, we look at the last tokens.
        Additional criteria can be given to only peek specific tokens.

        Args:
            n (int) : The number of tokens forward / backwards to peek.
            type (TkType | tuple[TkType] | None) : Type selection. None = any type, single value = only one type accepted, tuple = all included types accepted.
            value (str | tuple[str] | Callable[[str], bool] | None) : Value selection. None = any value, single value = only one value accepted, tuple = all included values accepted, Callable = if function returns true, token is accepted.

        Returns:
            Token: If there is an existing token n tokens away abiding given criteria, if provided. Otherwise, returns None.
        """
        if not isinstance(n, int) or not isinstance(type, (TkType, tuple, NoneType)) or not (isinstance(value, (str, tuple, NoneType)) or callable(value)):
            raise TypeError(f"Mismatched types for Lexer.peek({n} : int, {type} : TkType | ..., {value} : str | ...)")

        if 0 <= self.__cursor + n < self.token_count:
            tk : Token = self.__tokens[self.__cursor + n]
            if tk.criteria(type, value):
                return tk

    def consume(self, n : int = 1, type : TkType | tuple[TkType] | None = None, value : str | tuple[str] | Callable[[str], bool] | None = None) -> Token | None:
        """
        Consumes up to the nth next token in the token stream.
        Additional criteria can be given to only consume specific tokens.
        Only the nth next token is checked against criteria.

        Args:
            n (int) : The number of tokens forward to consume. (must be positive)
            type (TkType | tuple[TkType] | None) : Type selection. None = any type, single value = only one type accepted, tuple = all included types accepted.
            value (str | tuple[str] | Callable[[str], bool] | None) : Value selection. None = any value, single value = only one value accepted, tuple = all included values accepted, Callable = if function returns true, token is accepted.

        Returns:
            Token: If there is an existing token n tokens away abiding given criteria, if provided. Otherwise, returns None.
        """
        if not isinstance(n, int) or not isinstance(type, (TkType, tuple, NoneType)) or not (isinstance(value, (str, tuple, NoneType)) or callable(value)):
            raise TypeError(f"Mismatched types for Lexer.peek({n} : int, {type} : TkType | ..., {value} : str | ...)")

        tk : Token | None = self.peek(n, type, value)
        if tk:
            self.__cursor += n
            return tk

    def analyse(self) -> None:
        """
        Analyses the source code and generates tokens internally.
        """

        i : int = 0
        line : int = 0
        offset : int = 0

        # Helper functions
        def in_bounds() -> bool: return i < len(self.source)
        def char() -> str: return self.source[i]
        def append_tk(t : TkType, val : str, offset : int):
            self.__tokens.append(Token(t, val, line, offset))
            return offset + len(val)

        while in_bounds():
            if char().isspace():
                if char() == "\n":
                    line += 1
                    offset = 0
                if char() == "\t":
                    offset += 4
                else:
                    offset += 1
                i += 1

            elif char().isalpha() or not char().isascii():
                name : str = char()
                i += 1

                while in_bounds() and (char().isalnum() or char() == "_" or not char().isascii()):
                    name += char()
                    i += 1

                offset = append_tk(TkType.NAME, name, offset)

            elif char().isnumeric():
                number : str = char()
                t : TkType = TkType.INT
                i += 1

                if number == "0" and char() in ("o", "x", "b"):
                    accepted_range = {"o": "01234567", "x": "0123456789ABCDEF", "b": "01"}[char()]
                    i += 1
                    while in_bounds() and char() in accepted_range:
                        number += char()
                        i += 1
                    offset = append_tk(TkType.INT, number, offset)
                    continue

                while in_bounds() and char().isnumeric():
                    number += char()
                    i += 1

                if in_bounds() and char() == ".":
                    number += char()
                    i += 1
                    while in_bounds() and char().isnumeric():
                        number += char()
                        i += 1
                    t = TkType.FLOAT

                if in_bounds() and char() == "e":
                    number += char()
                    i += 1
                    while in_bounds() and (char().isnumeric() or char() in ("+", "-")):
                        number += char()
                        i += 1
                    t = TkType.FLOAT

                offset = append_tk(t, number, offset)

            elif (match := Lexer.operators.match(self.__source[i:])) != None:
                op : str = match.group()
                offset = append_tk(TkType.OPERATOR, op, offset)
                i += len(op)

            else:
                raise LexerError(f"{self.name}:{line}:{offset} - Unexpected character {char()}")

    def context(self, target : Token | int | tuple[int, int], msg : str = "") -> str:
        """Returns the context of the line, character or token from the lexer unit."""
        lines = self.__source.splitlines()
        if isinstance(target, Token):
            return f"{self.name}:{target.line}:{target.offset}{" - "+msg if msg else msg}\n{target.line:<4d}{lines[target.line]}\n    {' '*target.offset}{'^'+'~'*len(target.value)}"
        elif isinstance(target, int):
            return f"{self.name}:{target}{" - "+msg if msg else msg}\n{target:<4d}{lines[target]}"
        elif isinstance(target, tuple):
            return f"{self.name}:{target[0]}:{target[1]}{" - "+msg if msg else msg}\n{target[0]:<4d}{lines[target[0]]}\n    {' '*target[1]}{'^'}"

        raise TypeError(f"Mismatched types for Lexer.context({target} : Token | int | tuple[int, int], ...)")

    def error(self, target : Token | int | tuple[int, int], msg : str = "") -> None:
        """Shortcut to create a context error."""
        raise ContextError(self.context(target, msg))
