from ast_nodes import *


"""
class Expr(ABC):
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
"""

class Literal(Expr):
    def __init__(self, value : Token) -> None:
        super().__init__()
        self.__value : Token = value

    @property
    @override
    def token(self) -> Token:
        return self.__value

    def evaluate(self, source : Lexer, context : Context) -> Any:
        pass

    def generate(self, source : Lexer, context : Context, generator : Generator) -> None:
        pass
