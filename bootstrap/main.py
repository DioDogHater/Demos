from __future__ import annotations

from globals import CompilerGlobals, CompilerTarget
from lexer import Lexer

if __name__ == "__main__":
    CompilerGlobals(CompilerTarget("dummy", ("dummy","dummy","dummy"), 64, 64))
    lex = Lexer("   Hello world! != ]{ 742123")
    lex.analyse()
    if tk := lex.peek():
        lex.error(tk, "Not a valid statement")
