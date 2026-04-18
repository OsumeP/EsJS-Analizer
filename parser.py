import sys
from LexicAnalizer import Lexer
from EnumTokenModule import EnumToken

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()

    def token(self):
        return self.lookahead

    def match(self, t):
        if isinstance(t, str):
            if self.lookahead.name == t:
                self.lookahead = self.lexer.next_token()
            else:
                self.syntax_error([t])
        else:
            if self.lookahead.type == t:
                self.lookahead = self.lexer.next_token()
            else:
                self.syntax_error([t])

    def syntax_error(self, expected):
        raise Exception(
            f"Error sintáctico. Se esperaba {expected} y llegó {self.lookahead}"
        )

    def S(self):
        if self.token().name == 'mut':
            self.match('mut')
            self.B()
        elif self.token().name == 'var':
            self.match('var')
            self.match(EnumToken.NUMBER)
            self.B()
        else:
            self.syntax_error(['mut', 'var'])

    def B(self):
        if self.token().name == 'a':
            self.match('a')
            self.B()
            self.match('b')
        elif self.token().name == 'b':
            self.match('b')
        else:
            self.syntax_error(['a', 'b'])

code = sys.stdin.read()
lexer = Lexer()
lexer.tokenize(code)

parser = Parser(lexer)

parser.S()