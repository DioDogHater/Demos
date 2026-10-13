from __future__ import annotations

from lexer import *
from ast_nodes import *

class TranslationUnit:
    def __init__(self, source : str, name : str = "unknown") -> None:
        self.__lex = Lexer(source, name)
        self.__AST : ASTNode | None = None
    
    @property
    def source(self) -> str:
        return self.__lex.source
    
    @property
    def name(self) -> str:
        return self.__lex.name