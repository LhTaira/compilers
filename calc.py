import math
from lark import Lark, InlineTransformer

grammar = Lark(
    r"""
start  : sum

?sum   : sum "+" mul    -> add     
       | sum "-" mul    -> sub
       | mul

?mul   : mul "*" pow    -> mul     
       | mul "/" pow    -> div     
       | pow

?pow   : unary "^" pow  -> pow     
       | unary

?unary : "-" atom       -> neg 
       | "+" atom       -> pos
       | atom

?atom  : INT
       | COMPLEX
       | NAME
       | "(" sum ")"
       sqrt "(" sum ")"

INT     : ("0".."9")+
COMPLEX : INT "i"
NAME    : ("a".."z" | "_" | "A".."Z")+

%ignore " "
"""
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow, neg, pos
    names = {
        "pi": math.pi, 
        "e": math.e, 
        "answer": 42,
        "sqrt": math.sqrt
    }

    def INT(self, tk):
        return int(tk)

    def COMPLEX(self, tk):
        return self.INT(tk[:-1]) * 1j

    def NAME(self, tk):
        return self.names[tk]


transformer = CalcTransformer()
# exemplos = '40 2 +', '3 2 - 1 -', '2 10 4 * +', '4 3 2 ^ ^'
exemplos = "sqrt(4)", # "2 * pi", "e^1", "3 + 2i", '3 - 2 - (-1)', '(2 + 10) * 4', '4 ^ 3 ^ 2'

for src in exemplos:
    tree = grammar.parse(src)
    print(src)
    print(tree.pretty())
    print(transformer.transform(tree).pretty())