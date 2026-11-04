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

    @override
    def typeof(self, context : Context) -> Type:
        if self.__value.type == TkType.INT:
            return Int(64)
        elif self.__value.type == TkType.FLOAT:
            return Float(64)
        elif self.__value.type == TkType.CHAR:
            return Char()
        elif self.__value.type == TkType.STRING:
            pass # TODO
        elif self.__value.type == TkType.NAME:
            if var := context.get_var(self.__value.value):
                return var.type

    @override
    def evaluate(self, source : Lexer, context : Context) -> Any:
        if self.__value.type == TkType.INT:
            return int(self.__value.value, base=0)
        elif self.__value.type == TkType.FLOAT:
            return float(self.__value.value)
        elif self.__value.type == TkType.STRING or self.__value.type == TkType.CHAR:
            return self.__value.value

    @override
    def generate(self, source : Lexer, context : Context, generator : Generator) -> None:
        pass

class VariableDef(Expr):
    def __init__(self, name : Token, value : Expr | None, type : Type | None = None) -> None:
        super().__init__()
        self.__name : Token = name
        self.__type : Type | None = type
        self.__value : Expr | None = value

    @property
    def name(self) -> str:
        return self.__name.value

    @property
    def type(self) -> Type | None:
        return self.__type

    @property
    def value(self) -> Expr | None:
        return self.__value

    @property
    @override
    def token(self) -> Token:
        return self.__name

    @override
    def evaluate(self, source : Lexer, context : Context) -> Any:
        if self.value.typeof
        context.add_var(Variable(self.name, self.type))
        if self.value:
            return self.value.evaluate(source, context)
