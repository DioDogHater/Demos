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

def convert_string(string : str) -> str:
    rep : str = string.replace("\\a", "\a") \
                .replace("\\b", "\b") \
                .replace("\\e", "\x1b") \
                .replace("\\f", "\f") \
                .replace("\\n", "\n") \
                .replace("\\r", "\r") \
                .replace("\\t", "\t") \
                .replace("\\v", "\v") \
                .replace("\\\\", "\\") \
                .replace("\\'", "\'") \
                .replace("\\\"", "\"")
    
    # TODO Handle \xXX, \XX, \uXXXX and \UXXXXXXXX
    return rep

class Literal(Expr):
    def __init__(self, value : Token) -> None:
        super().__init__()
        self.__value : Token = value

    @property
    @override
    def token(self) -> Token:
        return self.__value

    def evaluate(self, source : Lexer, context : Context) -> Any:
        if self.__value.type == TkType.INT:
            return int(self.__value.value, base=0)
        elif self.__value.type == TkType.FLOAT:
            return float(self.__value.value)
        elif self.__value.type == TkType.STRING:
            return self.__value.value
        elif self.__value.type == TkType.CHAR:
            return self.__value.value

    def generate(self, source : Lexer, context : Context, generator : Generator) -> None:
        pass
