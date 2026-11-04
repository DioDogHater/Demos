from __future__ import annotations

from ast_nodes import *
from lexer import *

"""
This module will convert the stream of tokens provided by the lexer into an
ordered AST Node structure.

NOTE : Use pattern matching preferably.

"txt" -> match text
"txt1" "txt2" -> match text 1 and text2 (space not actually needed in code)

"txt1"|"txt2" -> match either
[0123456789] -> match any from selection
[0-9] -> match any from range
(pattern1|pattern2 test) -> match any from whole package
NUMBER -> Match from pre-defined pattern
EXPR -> Match from parser function, returns the parsed result
?"txt" -> Optionally match
*"txt" -> Match as many times as possible
+"txt" -> match at least 1 time
,"txt" -> Match as many times, separated by comma
:"txt" -> Save match in stack
.INT -> Match type of token
"""

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
