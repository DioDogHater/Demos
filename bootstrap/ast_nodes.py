from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, override

from generator import *
from globals import *
from lexer import *

"""
This module contains the base for all AST Nodes for Demos.

A statement is an individual instruction, like an if statement.
They cannot be inserted in the middle of another statement.

An expression is something that yields a value, that can be inserted inside a statement if it is appropriate.
Expressions can also hold other expressions.
"""

class EvalError(Exception):
    def __init__(self, *args : object) -> None:
        super().__init__(*args)

class ExecError(Exception):
    def __init__(self, *args : object) -> None:
        super().__init__(*args)

class Expr(ABC):
    """Abstract expression"""

    @property
    @abstractmethod
    def token(self) -> Token:
        pass

    @abstractmethod
    def typeof(self, context : Context) -> Type:
        pass

    def evaluate(self, source : Lexer, context : Context) -> Any:
        raise EvalError("Evaluation not implemented")

    def generate(self, source : Lexer, context : Context, generator : Generator) -> None:
        raise GenerationError("Generation not implemented")

class Type(ABC):
    """Abstract value type"""

    @property
    @abstractmethod
    def size(self) -> int:
        """Size, in bytes."""
        # If size = 0, is not a sized value (like none or any)

    @property
    def methods(self) -> list[Method]:
        return []

    @abstractmethod
    def is_compatible(self, value : Expr) -> bool:
        """Checks if the value can be converted, interpreted as this type."""

    def __repr__(self) -> str:
        return "unknown"

    def __str__(self) -> str: return repr(self)

    def __eq__(self, other : object) -> bool:
        return isinstance(other, self.__class__)

class Void(Type):
    """Type where none is the only value. Does not contain any data."""

    @property
    @override
    def size(self) -> int:
        return 0

    @override
    def is_compatible(self, value : Expr) -> bool:
        return isinstance(value.typeof, Void)

class Int(Type):
    """Integer type"""
    def __init__(self, size : int, signed : bool = True) -> None:
        """Create an integer type.
        Args:
            size (int) : The number of bits in the type.
            signed (bool) : If the integer type is signed."""
        self.__size : int = size // 8
        self.__signed : bool = signed

    @property
    @override
    def size(self) -> int:
        return self.size

    @property
    def signed(self) -> bool:
        return self.__signed

    @override
    def is_compatible(self, value : Expr) -> bool:
        return isinstance(value.typeof, (Int, Char, Bool))

    @override
    def __repr__(self) -> str:
        return f"{"i" if self.signed else "u"}{self.size * 8}"

    @override
    def __eq__(self, other : object) -> bool:
        return isinstance(other, Int) and self.size == other.size

class SizeInt(Int):
    def __init__(self, signed : bool = True) -> None:
        super().__init__(CompilerGlobals().target.pointer_size, signed)

    @override
    def __repr__(self) -> str:
        return f"{"s" if self.signed else "u"}size"

class Float(Type):
    """Floating point number."""
    def __init__(self, size : int) -> None:
        self.__size : int = size // 8

    @property
    @override
    def size(self) -> int:
        return self.__size

    @override
    def is_compatible(self, value : Expr) -> bool:
        return isinstance(value, (Int, Float, Bool))

    @override
    def __repr__(self) -> str:
        return f"f{self.__size * 8}"

class Bool(Type):
    """Boolean type, can be converted to an integer, but is treated differently."""

    @property
    @override
    def size(self) -> int:
        return 1

    @override
    def is_compatible(self, value : Expr) -> bool:
        return isinstance(value.typeof, Bool)

    @override
    def __repr__(self) -> str:
        return "bool"

class Char(Type):
    """Character type, used for strings and general text stuff."""

    @property
    @override
    def size(self) -> int:
        return 1

    @override
    def is_compatible(self, value : Expr) -> bool:
        return isinstance(value.typeof, (Int, Char))

    @override
    def __repr__(self) -> str:
        return "char"

class WChar(Char):
    """Wide, extended version of the character type, for Unicode characters. 4 bytes big instead of 1 byte."""

    @property
    @override
    def size(self) -> int:
        return 4

    @override
    def __repr__(self) -> str:
        return "wchar"

class Pointer(Type):
    """Pointer to another type."""

    def __init__(self, underlying : Type) -> None:
        self.__underlying : Type = underlying

    @property
    def underlying(self) -> Type:
        return self.__underlying

    @property
    @override
    def size(self) -> int:
        return CompilerGlobals().target.pointer_size

    @override
    def is_compatible(self, value: Expr) -> bool:
        return super().is_compatible(value)

    @override
    def __repr__(self) -> str:
        return f"{self.underlying}*"

class Arg:
    """Argument description."""
    def __init__(self, name : str, type : Type, default : Expr | None = None, varg : bool = False) -> None:
        self.__name : str = name
        self.__type : Type = type
        self.__default : Expr | None = default
        self.__varg : bool = varg

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> Type:
        return self.__type

    @property
    def default(self) -> Expr | None:
        return self.__default

    @property
    def is_varg(self) -> bool:
        return self.__varg

class FuncType(Type):
    """Basic function type"""

    def __init__(self, return_type : Type, args : tuple[Arg, ...]) -> None:
        self.__return_type : Type = return_type
        self.__args : tuple[Arg, ...] = args

    @property
    @override
    def size(self) -> int:
        return self.return_type.size

    @property
    def return_type(self) -> Type:
        return self.__return_type

    @property
    def args(self) -> tuple[Arg, ...]:
        return self.__args

    @override
    def is_compatible(self, value : Expr) -> bool:
        return value.typeof == self

    @override
    def __repr__(self) -> str:
        return f"({", ".join([str(arg.type) for arg in self.args])}) -> {self.return_type}"

    @override
    def __eq__(self, other : object) -> bool:
        return isinstance(other, FuncType) and other.args == self.args and other.return_type == self.return_type

class Function(ABC):
    """General function representation"""

    def __init__(self, name : str, type : FuncType) -> None:
        self.__name : str = name
        self.__type : FuncType = type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> FuncType:
        return self.__type

    @property
    def return_type(self) -> Type:
        return self.__type.return_type

    @abstractmethod
    def args_compatible(self, args : list[Expr]) -> bool:
        pass

    def __repr__(self) -> str:
        return f"{self.name}{self.type}"

    def __str__(self) -> str: return repr(self)

class Method(Function):
    """Methods are a subset of functions, because they must be treated differently, but are very similar."""

    @override
    def __repr__(self) -> str:
        return "."+super().__repr__()

class Variable(ABC):
    """Generic variable."""
    def __init__(self, name : str, type : Type) -> None:
        self.__name : str = name
        self.__type : Type = type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> Type:
        return self.__type

    def __repr__(self) -> str:
        return f"{self.name} : {self.type}"

    def __str__(self) -> str: return repr(self)

class Constant(Variable):
    """Generic constant."""
    def __init__(self, name : str, type : Type) -> None:
        super().__init__(name, type)

class Context:
    """The context surrounding a statement.
    i.e. local / global variables, available functions and modules, etc."""

    def __init__(self, parent : Context | None = None) -> None:
        self.__parent : Context | None = parent
        self.__funcs : dict[str, Function] = {}
        self.__vars : dict[str, Variable] = {}

    @property
    def parent(self) -> Context | None:
        return self.__parent

    @property
    def funcs(self) -> dict[str, Function]:
        return self.__funcs

    @property
    def vars(self) -> dict[str, Variable]:
        return self.__vars

    def add_var(self, var : Variable) -> None:
        self.__vars[var.name] = var

    def get_local_var(self, name : str) -> Variable | None:
        return self.__vars.get(name)

    def get_extern_var(self, name : str) -> Variable | None:
        if self.__parent:
            return self.__parent.get_var(name)

    def get_var(self, name : str) -> Variable | None:
        if not (v := self.get_local_var(name)) and self.__parent:
            return self.__parent.get_var(name)
        return v

    def add_func(self, func : Function) -> None:
        self.__funcs[func.name] = func

    def get_local_func(self, name : str) -> Function | None:
        return self.__funcs.get(name)

    def get_extern_func(self, name : str) -> Function | None:
        if self.__parent:
            return self.__parent.get_func(name)

    def get_func(self, name : str) -> Function | None:
        if not (f := self.get_local_func(name)) and self.__parent:
            return self.__parent.get_func(name)
        return f

class ASTNode(ABC):
    """Basic AST node, mostly for statements, declarations and definitions."""
    def __init__(self, parent : ASTNode | None = None) -> None:
        self.__parent : ASTNode | None = parent
        self.__context : Context = Context(parent.context if parent else None)

    @property
    def parent(self) -> ASTNode | None:
        return self.__parent

    @property
    def context(self) -> Context:
        return self.__context

    @property
    @abstractmethod
    def token(self) -> Token:
        pass

    @abstractmethod
    def exec(self, source : Lexer) -> Any:
        pass

    # TODO - Add this back
    # @abstractmethod
    # def generate(self, source : Lexer, generator : Generator) -> None:
    #     pass

# TODO Remove
class TestStmt(ASTNode):
    def __init__(self, test : Token, parent : ASTNode | None = None) -> None:
        super().__init__(parent)
        self.__test : Token = test

    @property
    @override
    def token(self) -> Token:
        return self.__test

    @override
    def exec(self, source : Lexer) -> None:
        print("Test from Demos!")

class ExprStmt(ASTNode):
    def __init__(self, expr : Expr, parent : ASTNode | None = None) -> None:
        super().__init__(parent)
        self.__expr : Expr = expr

    @property
    @override
    def token(self) -> Token:
        return self.__expr.token

    @override
    def exec(self, source : Lexer) -> Any:
        return self.__expr.evaluate(source, self.context)
