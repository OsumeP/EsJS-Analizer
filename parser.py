import sys
from LexicAnalizer import Lexer
from EnumTokenModule import EnumToken
from Token import Token

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.next_token()

    def next_token(self):
        token = self.lexer.next_token()
        if token is None:
            return Token(EnumToken.END, 'EOF', -1, -1, None)
        return token

    def token(self):
        return self.lookahead

    def match(self, t):
        if isinstance(t, str):
            if self.lookahead.name == t:
                self.lookahead = self.next_token()
            else:
                self.syntax_error([t])
        else:
            if self.lookahead.type == t:
                self.lookahead = self.next_token()
            else:
                self.syntax_error([t])

    def syntax_error(self, expected):
        if self.lookahead.type == EnumToken.END:
            found = 'final de archivo'
        else:
            found = self.lookahead.name

        expected_str = ', '.join(map(str, expected))

        print(f"<{self.lookahead.row}:{self.lookahead.col}> Error sintactico: se encontro: '{found}'; se esperaba: {expected_str}.)")

    def Programa(self):
        if self.token().name == '(' or self.token().name == 'mientras' or self.token().name == '-' or self.token().name == 'continuar' or self.token().name == 'crear' or self.token().name == 'const' or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'retornar' or self.token().name == 'hacer' or self.token().name == 'var' or self.token().name == 'funcion' or self.token().name == 'elegir' or self.token().name == 'romper' or self.token().name == 'nulo' or self.token().type == EnumToken.NUMBER or self.token().name == '$' or self.token().name == 'si' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'para' or self.token().name == 'verdadero' or self.token().name == 'mut' or self.token().name == '{':
            self.ListaDeclaraciones()
        else:
            self.syntax_error(['(', 'mientras', '-', 'continuar', 'crear', 'const', 'indefinido', 'tipoDe', '!', '[', 'retornar', 'hacer', 'var', 'funcion', 'elegir', 'romper', 'nulo', EnumToken.NUMBER, '$', 'si', 'falso', EnumToken.ID, EnumToken.STRING, 'para', 'verdadero', 'mut', '{'])

    def ListaDeclaraciones(self):
        if self.token().name == '(' or self.token().name == 'mientras' or self.token().name == '-' or self.token().name == 'para' or self.token().name == 'crear' or self.token().name == 'const' or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().type == EnumToken.ID or self.token().name == 'retornar' or self.token().name == 'hacer' or self.token().name == 'var' or self.token().name == 'funcion' or self.token().name == 'elegir' or self.token().name == 'romper' or self.token().name == 'nulo' or self.token().type == EnumToken.NUMBER or self.token().name == 'si' or self.token().name == 'falso' or self.token().type == EnumToken.STRING or self.token().name == 'continuar' or self.token().name == 'verdadero' or self.token().name == 'mut' or self.token().name == '{':
            self.Declaracion()
            self.ListaDeclaraciones()
        elif self.token().name == 'porDefecto' or self.token().name == '}' or self.token().name == 'caso' or self.token().name == '$':
            pass
        else:
            self.syntax_error(['(', 'mientras', '-', 'para', 'crear', 'const', 'indefinido', 'tipoDe', '!', '[', EnumToken.ID, 'retornar', 'hacer', 'var', 'funcion', 'elegir', 'romper', 'nulo', EnumToken.NUMBER, 'si', 'falso', EnumToken.STRING, 'continuar', 'verdadero', 'mut', '{', 'porDefecto', '}', 'caso', '$'])

    def Declaracion(self):
        if self.token().name == 'var' or self.token().name == 'mut':
            self.DeclVar()
        elif self.token().name == 'const':
            self.DeclConst()
        elif self.token().name == 'funcion':
            self.DeclFuncion()
        elif self.token().name == 'si':
            self.SentSi()
        elif self.token().name == 'mientras':
            self.SentMientras()
        elif self.token().name == 'hacer':
            self.SentHacerMientras()
        elif self.token().name == 'para':
            self.SentPara()
        elif self.token().name == 'elegir':
            self.SentElegir()
        elif self.token().name == 'retornar':
            self.SentRetornar()
        elif self.token().name == 'romper':
            self.SentRomper()
        elif self.token().name == 'continuar':
            self.SentContinuar()
        elif self.token().name == '{':
            self.Bloque()
        elif self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.SentExpr()
        else:
            self.syntax_error(['var', 'mut', 'const', 'funcion', 'si', 'mientras', 'hacer', 'para', 'elegir', 'retornar', 'romper', 'continuar', '{', '(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def DeclVar(self):
        if self.token().name == 'mut':
            self.match('mut')
            self.match(EnumToken.ID)
            self.InicOpcional()
            self.RestDeclaradores()
            self.match(';')
        elif self.token().name == 'var':
            self.match('var')
            self.match(EnumToken.ID)
            self.InicOpcional()
            self.RestDeclaradores()
            self.match(';')
        else:
            self.syntax_error(['mut', 'var'])

    def RestDeclaradores(self):
        if self.token().name == ',':
            self.match(',')
            self.match(EnumToken.ID)
            self.InicOpcional()
            self.RestDeclaradores()
        elif self.token().name == ';':
            pass
        else:
            self.syntax_error([',', ';'])

    def DeclConst(self):
        if self.token().name == 'const':
            self.match('const')
            self.match(EnumToken.ID)
            self.match('=')
            self.Expresion()
            self.match(';')
        else:
            self.syntax_error(['const'])

    def InicOpcional(self):
        if self.token().name == '=':
            self.match('=')
            self.Expresion()
        elif self.token().name == ';' or self.token().name == ',':
            pass
        else:
            self.syntax_error(['=', ';', ','])

    def DeclFuncion(self):
        if self.token().name == 'funcion':
            self.match('funcion')
            self.match(EnumToken.ID)
            self.match('(')
            self.ListaParams()
            self.match(')')
            self.Bloque()
        else:
            self.syntax_error(['funcion'])

    def ListaParams(self):
        if self.token().type == EnumToken.ID:
            self.match(EnumToken.ID)
            self.RestParams()
        elif self.token().name == ')':
            pass
        else:
            self.syntax_error([EnumToken.ID, ')'])

    def RestParams(self):
        if self.token().name == ',':
            self.match(',')
            self.match(EnumToken.ID)
            self.RestParams()
        elif self.token().name == ')':
            pass
        else:
            self.syntax_error([',', ')'])

    def Bloque(self):
        if self.token().name == '{':
            self.match('{')
            self.ListaDeclaraciones()
            self.match('}')
        else:
            self.syntax_error(['{'])

    def SentRetornar(self):
        if self.token().name == 'retornar':
            self.match('retornar')
            self.ExprOpcional()
            self.match(';')
        else:
            self.syntax_error(['retornar'])

    def ExprOpcional(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
        elif self.token().name == ';':
            pass
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion', ';'])

    def SentSi(self):
        if self.token().name == 'si':
            self.match('si')
            self.match('(')
            self.Expresion()
            self.match(')')
            self.Bloque()
            self.SinoOpcional()
        else:
            self.syntax_error(['si'])

    def SinoOpcional(self):
        if self.token().name == 'sino':
            self.match('sino')
            self.Bloque()
        elif self.token().name == '(' or self.token().name == '-' or self.token().name == 'porDefecto' or self.token().name == 'para' or self.token().name == '}' or self.token().name == 'continuar' or self.token().name == 'crear' or self.token().name == 'const' or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().type == EnumToken.ID or self.token().name == 'retornar' or self.token().name == 'hacer' or self.token().name == 'var' or self.token().name == 'funcion' or self.token().name == 'elegir' or self.token().name == 'romper' or self.token().name == 'nulo' or self.token().type == EnumToken.NUMBER or self.token().name == '$' or self.token().name == 'si' or self.token().name == 'falso' or self.token().name == 'caso' or self.token().type == EnumToken.STRING or self.token().name == 'mientras' or self.token().name == 'verdadero' or self.token().name == 'mut' or self.token().name == '{':
            pass
        else:
            self.syntax_error(['sino', '(', '-', 'porDefecto', 'para', '}', 'continuar', 'crear', 'const', 'indefinido', 'tipoDe', '!', '[', EnumToken.ID, 'retornar', 'hacer', 'var', 'funcion', 'elegir', 'romper', 'nulo', EnumToken.NUMBER, '$', 'si', 'falso', 'caso', EnumToken.STRING, 'mientras', 'verdadero', 'mut', '{'])

    def SentMientras(self):
        if self.token().name == 'mientras':
            self.match('mientras')
            self.match('(')
            self.Expresion()
            self.match(')')
            self.Bloque()
        else:
            self.syntax_error(['mientras'])

    def SentHacerMientras(self):
        if self.token().name == 'hacer':
            self.match('hacer')
            self.Bloque()
            self.match('mientras')
            self.match('(')
            self.Expresion()
            self.match(')')
            self.match(';')
        else:
            self.syntax_error(['hacer'])

    def SentPara(self):
        if self.token().name == 'para':
            self.match('para')
            self.match('(')
            self.InicPara()
            self.CondPara()
            self.match(';')
            self.ActPara()
            self.match(')')
            self.Bloque()
        else:
            self.syntax_error(['para'])

    def InicPara(self):
        if self.token().name == 'var' or self.token().name == 'mut':
            self.DeclVarSinPuntoComa()
            self.match(';')
        elif self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
            self.match(';')
        elif self.token().name == ';':
            self.match(';')
        else:
            self.syntax_error(['var', 'mut', '(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion', ';'])

    def DeclVarSinPuntoComa(self):
        if self.token().name == 'mut':
            self.match('mut')
            self.match(EnumToken.ID)
            self.InicOpcional()
            self.RestDeclaradores()
        elif self.token().name == 'var':
            self.match('var')
            self.match(EnumToken.ID)
            self.InicOpcional()
            self.RestDeclaradores()
        else:
            self.syntax_error(['mut', 'var'])

    def CondPara(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
        elif self.token().name == ';':
            pass
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion', ';'])

    def ActPara(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
        elif self.token().name == ')':
            pass
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion', ')'])

    def SentElegir(self):
        if self.token().name == 'elegir':
            self.match('elegir')
            self.match('(')
            self.Expresion()
            self.match(')')
            self.match('{')
            self.ListaCasos()
            self.PorDefectoOpc()
            self.match('}')
        else:
            self.syntax_error(['elegir'])

    def ListaCasos(self):
        if self.token().name == 'caso':
            self.Caso()
            self.ListaCasos()
        elif self.token().name == '}' or self.token().name == 'porDefecto':
            pass
        else:
            self.syntax_error(['caso', '}', 'porDefecto'])

    def Caso(self):
        if self.token().name == 'caso':
            self.match('caso')
            self.Expresion()
            self.match(':')
            self.ListaDeclaraciones()
        else:
            self.syntax_error(['caso'])

    def PorDefectoOpc(self):
        if self.token().name == 'porDefecto':
            self.match('porDefecto')
            self.match(':')
            self.ListaDeclaraciones()
        elif self.token().name == '}':
            pass
        else:
            self.syntax_error(['porDefecto', '}'])

    def SentRomper(self):
        if self.token().name == 'romper':
            self.match('romper')
            self.match(';')
        else:
            self.syntax_error(['romper'])

    def SentContinuar(self):
        if self.token().name == 'continuar':
            self.match('continuar')
            self.match(';')
        else:
            self.syntax_error(['continuar'])

    def SentExpr(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
            self.match(';')
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def Expresion(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpAsign()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def ExpAsign(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpOr()
            self.RestAsign()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestAsign(self):
        if self.token().name == '=':
            self.match('=')
            self.ExpAsign()
        elif self.token().name == '+=':
            self.match('+=')
            self.ExpAsign()
        elif self.token().name == '-=':
            self.match('-=')
            self.ExpAsign()
        elif self.token().name == '*=':
            self.match('*=')
            self.ExpAsign()
        elif self.token().name == '/=':
            self.match('/=')
            self.ExpAsign()
        elif self.token().name == '%=':
            self.match('%=')
            self.ExpAsign()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '*' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ';' or self.token().name == ')' or self.token().name == '==' or self.token().name == ',' or self.token().name == '/' or self.token().name == '&&' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '||' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['=', '+=', '-=', '*=', '/=', '%=', '(', '/=', '-=', '-', '%=', '}', '>', '*', '<=', '[', ']', '!==', ';', ')', '==', ',', '/', '&&', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '||', '.'])

    def ExpOr(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpAnd()
            self.RestOr()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestOr(self):
        if self.token().name == '||':
            self.match('||')
            self.ExpAnd()
            self.RestOr()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ')' or self.token().name == ';' or self.token().name == '==' or self.token().name == '||' or self.token().name == ',' or self.token().name == '/' or self.token().name == '&&' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '*' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['||', '(', '/=', '-=', '-', '%=', '}', '>', '<=', '[', ']', '!==', ')', ';', '==', '||', ',', '/', '&&', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '*', '.'])

    def ExpAnd(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpIgualdad()
            self.RestAnd()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestAnd(self):
        if self.token().name == '&&':
            self.match('&&')
            self.ExpIgualdad()
            self.RestAnd()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ';' or self.token().name == ')' or self.token().name == '==' or self.token().name == '||' or self.token().name == ',' or self.token().name == '/' or self.token().name == '&&' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '*' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['&&', '(', '/=', '-=', '-', '%=', '}', '>', '<=', '[', ']', '!==', ';', ')', '==', '||', ',', '/', '&&', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '*', '.'])

    def ExpIgualdad(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpRelac()
            self.RestIgualdad()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestIgualdad(self):
        if self.token().name == '===':
            self.match('===')
            self.ExpRelac()
            self.RestIgualdad()
        elif self.token().name == '!==':
            self.match('!==')
            self.ExpRelac()
            self.RestIgualdad()
        elif self.token().name == '==':
            self.match('==')
            self.ExpRelac()
            self.RestIgualdad()
        elif self.token().name == '!=':
            self.match('!=')
            self.ExpRelac()
            self.RestIgualdad()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ')' or self.token().name == ';' or self.token().name == '==' or self.token().name == '||' or self.token().name == ',' or self.token().name == '&&' or self.token().name == '/' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '*' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['===', '!==', '==', '!=', '(', '/=', '-=', '-', '%=', '}', '>', '<=', '[', ']', '!==', ')', ';', '==', '||', ',', '&&', '/', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '*', '.'])

    def ExpRelac(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpAdic()
            self.RestRelac()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestRelac(self):
        if self.token().name == '<':
            self.match('<')
            self.ExpAdic()
            self.RestRelac()
        elif self.token().name == '>':
            self.match('>')
            self.ExpAdic()
            self.RestRelac()
        elif self.token().name == '<=':
            self.match('<=')
            self.ExpAdic()
            self.RestRelac()
        elif self.token().name == '>=':
            self.match('>=')
            self.ExpAdic()
            self.RestRelac()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ';' or self.token().name == ')' or self.token().name == '==' or self.token().name == '||' or self.token().name == ',' or self.token().name == '&&' or self.token().name == '/' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '*' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['<', '>', '<=', '>=', '(', '/=', '-=', '-', '%=', '}', '>', '<=', '[', ']', '!==', ';', ')', '==', '||', ',', '&&', '/', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '*', '.'])

    def ExpAdic(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpMult()
            self.RestAdic()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestAdic(self):
        if self.token().name == '+':
            self.match('+')
            self.ExpMult()
            self.RestAdic()
        elif self.token().name == '-':
            self.match('-')
            self.ExpMult()
            self.RestAdic()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ';' or self.token().name == ')' or self.token().name == '==' or self.token().name == '||' or self.token().name == ',' or self.token().name == '&&' or self.token().name == '/' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '*' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['+', '-', '(', '/=', '-=', '-', '%=', '}', '>', '<=', '[', ']', '!==', ';', ')', '==', '||', ',', '&&', '/', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '*', '.'])

    def ExpMult(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpUnaria()
            self.RestMult()
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestMult(self):
        if self.token().name == '*':
            self.match('*')
            self.ExpUnaria()
            self.RestMult()
        elif self.token().name == '/':
            self.match('/')
            self.ExpUnaria()
            self.RestMult()
        elif self.token().name == '%':
            self.match('%')
            self.ExpUnaria()
            self.RestMult()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ';' or self.token().name == ')' or self.token().name == '==' or self.token().name == '||' or self.token().name == ',' or self.token().name == '&&' or self.token().name == '/' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '*' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['*', '/', '%', '(', '/=', '-=', '-', '%=', '}', '>', '<=', '[', ']', '!==', ';', ')', '==', '||', ',', '&&', '/', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '*', '.'])

    def ExpUnaria(self):
        if self.token().name == '!':
            self.match('!')
            self.ExpUnaria()
        elif self.token().name == '-':
            self.match('-')
            self.ExpUnaria()
        elif self.token().name == 'tipoDe':
            self.match('tipoDe')
            self.ExpUnaria()
        elif self.token().name == '(' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpPostfija()
        else:
            self.syntax_error(['!', '-', 'tipoDe', '(', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def ExpPostfija(self):
        if self.token().name == '(' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.ExpPrimaria()
            self.RestPostfija()
        else:
            self.syntax_error(['(', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def RestPostfija(self):
        if self.token().name == '[':
            self.match('[')
            self.Expresion()
            self.match(']')
            self.RestPostfija()
        elif self.token().name == '.':
            self.match('.')
            self.match(EnumToken.ID)
            self.RestPostfija()
        elif self.token().name == '(':
            self.match('(')
            self.ListaArgs()
            self.match(')')
            self.RestPostfija()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ';' or self.token().name == ')' or self.token().name == '==' or self.token().name == '||' or self.token().name == ',' or self.token().name == '/' or self.token().name == '&&' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '*' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['[', '.', '(', '(', '/=', '-=', '-', '%=', '}', '>', '<=', '[', ']', '!==', ';', ')', '==', '||', ',', '/', '&&', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '*', '.'])

    def ExpPrimaria(self):
        if self.token().type == EnumToken.ID:
            self.match(EnumToken.ID)
        elif self.token().name == 'indefinido' or self.token().name == 'nulo' or self.token().name == 'falso' or self.token().type == EnumToken.STRING or self.token().type == EnumToken.NUMBER or self.token().name == 'verdadero':
            self.Literal()
        elif self.token().name == '(':
            self.ExpPrimParentesis()
        elif self.token().name == '[':
            self.LiteralArreglo()
        elif self.token().name == '{':
            self.LiteralObjeto()
        elif self.token().name == 'funcion':
            self.match('funcion')
            self.IDOpcional()
            self.match('(')
            self.ListaParams()
            self.match(')')
            self.Bloque()
        elif self.token().name == 'crear':
            self.match('crear')
            self.ExpPostfija()
        else:
            self.syntax_error([EnumToken.ID, 'indefinido', 'nulo', 'falso', EnumToken.STRING, EnumToken.NUMBER, 'verdadero', '(', '[', '{', 'funcion', 'crear'])

    def ExpPrimParentesis(self):
        if self.token().name == '(':
            self.match('(')
            self.ContenidoParentesis()
            self.match(')')
            self.RestArrow()
        else:
            self.syntax_error(['('])

    def ContenidoParentesis(self):
        if self.token().name == ')' or self.token().type == EnumToken.ID:
            self.ListaParams()
        else:
            self.syntax_error([')', EnumToken.ID])

    def RestArrow(self):
        if self.token().name == '=>':
            self.match('=>')
            self.CuerpoArrow()
        elif self.token().name == '(' or self.token().name == '/=' or self.token().name == '-=' or self.token().name == '-' or self.token().name == '%=' or self.token().name == '}' or self.token().name == '>' or self.token().name == '*' or self.token().name == '<=' or self.token().name == '[' or self.token().name == ']' or self.token().name == '!==' or self.token().name == ';' or self.token().name == ')' or self.token().name == '==' or self.token().name == ',' or self.token().name == '/' or self.token().name == '&&' or self.token().name == '=' or self.token().name == '!=' or self.token().name == '+=' or self.token().name == '%' or self.token().name == '+' or self.token().name == '>=' or self.token().name == '*=' or self.token().name == '===' or self.token().name == ':' or self.token().name == '<' or self.token().name == '||' or self.token().name == '.':
            pass
        else:
            self.syntax_error(['=>', '(', '/=', '-=', '-', '%=', '}', '>', '*', '<=', '[', ']', '!==', ';', ')', '==', ',', '/', '&&', '=', '!=', '+=', '%', '+', '>=', '*=', '===', ':', '<', '||', '.'])

    def CuerpoArrow(self):
        if self.token().name == '{':
            self.Bloque()
        elif self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
        else:
            self.syntax_error(['{', '(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion'])

    def IDOpcional(self):
        if self.token().type == EnumToken.ID:
            self.match(EnumToken.ID)
        elif self.token().name == '(':
            pass
        else:
            self.syntax_error([EnumToken.ID, '('])

    def Literal(self):
        if self.token().type == EnumToken.NUMBER:
            self.match(EnumToken.NUMBER)
        elif self.token().type == EnumToken.STRING:
            self.match(EnumToken.STRING)
        elif self.token().name == 'verdadero':
            self.match('verdadero')
        elif self.token().name == 'falso':
            self.match('falso')
        elif self.token().name == 'nulo':
            self.match('nulo')
        elif self.token().name == 'indefinido':
            self.match('indefinido')
        else:
            self.syntax_error([EnumToken.NUMBER, EnumToken.STRING, 'verdadero', 'falso', 'nulo', 'indefinido'])

    def LiteralArreglo(self):
        if self.token().name == '[':
            self.match('[')
            self.ListaElems()
            self.match(']')
        else:
            self.syntax_error(['['])

    def ListaElems(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
            self.RestElems()
        elif self.token().name == ']':
            pass
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion', ']'])

    def RestElems(self):
        if self.token().name == ',':
            self.match(',')
            self.Expresion()
            self.RestElems()
        elif self.token().name == ']':
            pass
        else:
            self.syntax_error([',', ']'])

    def LiteralObjeto(self):
        if self.token().name == '{':
            self.match('{')
            self.ListaPropiedades()
            self.match('}')
        else:
            self.syntax_error(['{'])

    def ListaPropiedades(self):
        if self.token().type == EnumToken.NUMBER or self.token().type == EnumToken.STRING or self.token().type == EnumToken.ID:
            self.Propiedad()
            self.RestPropiedades()
        elif self.token().name == '}':
            pass
        else:
            self.syntax_error([EnumToken.NUMBER, EnumToken.STRING, EnumToken.ID, '}'])

    def Propiedad(self):
        if self.token().type == EnumToken.NUMBER or self.token().type == EnumToken.STRING or self.token().type == EnumToken.ID:
            self.ClaveProp()
            self.match(':')
            self.Expresion()
        else:
            self.syntax_error([EnumToken.NUMBER, EnumToken.STRING, EnumToken.ID])

    def ClaveProp(self):
        if self.token().type == EnumToken.ID:
            self.match(EnumToken.ID)
        elif self.token().type == EnumToken.STRING:
            self.match(EnumToken.STRING)
        elif self.token().type == EnumToken.NUMBER:
            self.match(EnumToken.NUMBER)
        else:
            self.syntax_error([EnumToken.ID, EnumToken.STRING, EnumToken.NUMBER])

    def RestPropiedades(self):
        if self.token().name == ',':
            self.match(',')
            self.Propiedad()
            self.RestPropiedades()
        elif self.token().name == '}':
            pass
        else:
            self.syntax_error([',', '}'])

    def ListaArgs(self):
        if self.token().name == '(' or self.token().name == '-' or self.token().name == 'nulo' or self.token().name == 'crear' or self.token().type == EnumToken.NUMBER or self.token().name == 'indefinido' or self.token().name == 'tipoDe' or self.token().name == '!' or self.token().name == '[' or self.token().name == 'falso' or self.token().type == EnumToken.ID or self.token().type == EnumToken.STRING or self.token().name == 'verdadero' or self.token().name == '{' or self.token().name == 'funcion':
            self.Expresion()
            self.RestArgs()
        elif self.token().name == ')':
            pass
        else:
            self.syntax_error(['(', '-', 'nulo', 'crear', EnumToken.NUMBER, 'indefinido', 'tipoDe', '!', '[', 'falso', EnumToken.ID, EnumToken.STRING, 'verdadero', '{', 'funcion', ')'])

    def RestArgs(self):
        if self.token().name == ',':
            self.match(',')
            self.Expresion()
            self.RestArgs()
        elif self.token().name == ')':
            pass
        else:
            self.syntax_error([',', ')'])

code = sys.stdin.read()
lexer = Lexer()
lexer.tokenize(code)

parser = Parser(lexer)

parser.Programa()