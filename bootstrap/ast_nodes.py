from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, override

from generator import *
from lexer import *


class EvalError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Expr(ABC):
    """Abstract expression"""

    @property
    @abstractmethod
    def token(self) -> Token:
        pass

    @property
    @abstractmethod
    def typeof(self) -> Type:
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
        # If size = 0, is not a sized value (like none or any)
        pass

    @abstractmethod
    def is_compatible(self, value : Expr) -> bool:
        pass

    def __repr__(self) -> str:
        return "unknown"

    def __str__(self) -> str: return repr(self)

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
    def __repr__(self) -> str:
        return f"({", ".join([str(arg.type) for arg in self.args])}) -> {self.return_type}"

class Function(ABC):
    """General function representation"""

    def __init__(self, name : str, type : FuncType) -> None:
        self.__name : str = name
        self.__type : FuncType = type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> Type:
        return self.__type

    @property
    def return_type(self) -> Type:
        return self.__type.return_type

    @abstractmethod
    def args_compatible(self, args : list[Expr]) -> bool:
        pass

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

class Context:
    """The context surrounding a statement.
    i.e. local / global variables, available functions and modules, etc."""

    def __init__(self, parent : Context | None = None) -> None:
        self.__parent : Context | None = parent

    @property
    def parent(self) -> Context | None:
        return self.__parent

class ASTNode(ABC):
    """Basic AST node, mostly for statements, declarations and definitions."""
    def __init__(self, parent : ASTNode | None = None) -> None:
        self.__parent : ASTNode | None = parent

    @property
    def parent(self) -> ASTNode | None:
        return self.__parent

    @property
    @abstractmethod
    def token(self) -> Token:
        pass
