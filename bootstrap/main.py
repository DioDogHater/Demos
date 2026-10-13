from __future__ import annotations

from lexer import Lexer

if __name__ == "__main__":
    lex = Lexer("   Hello world! != ]{ 742123")
    lex.analyse()
    if tk := lex.peek():
        lex.error(tk, "Not a valid statement")
