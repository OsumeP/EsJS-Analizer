import re
import sys
from Token import Token
from EnumTokenModule import EnumToken
class Lexer:

    def __init__(self):

        self.keywords = {
            #Control Keywords
                    'capturar', 'caso', 'con', 'continuar', 'crear', 'elegir', 'esperar', 'hacer', 'mientras', 'para', 'retornar', 'sino', 'si', 'constructor', 'eliminar', 'extiende', 'finalmente', 'instanciaDe',
                    'intentar', 'lanzar', 'longitud', 'romper', 'simbolo', 'subcad', 'tipoDe', 'vacio', 'ambiente', 'super', 'de', 'en', 'clase', 'const', 'var', 'mut', 'porDefecto', 'funcion',
                    #Language Constants
                    'falso', 'nulo', 'verdadero', 'indefinido', 'Infinito', 'NuN', 
                    #Support Functions
                    'consola', 'Fecha', 'Numero', 'Mate', 'Matriz', 'Arreglo', 'Booleano', 'Cadena', 'Funcion', 
                    #Console Object
                    'afirmar', 'limpiar', 'listar', 'error',
                    'agrupar', 'info', 'escribir', 'tabla',
                    #String Object
                    'enPosicion', 'caracterEn', 'codigoDeCaracterEn', 'puntoDeCodigoEn', 'concatenar', 'terminaCon', 'desdeCodigoDeCaracter', 'desdePuntoDeCodigo', 'incluye',
                    'indiceDe', 'ultimoIndiceDe', 'compararLocalizada', 'coincidir', 'coincidirTodo', 'normalizar', 'rellenarAlFinal', 'rellenarAlComienzo', 'crudo', 'repetir', 'reemplazar', 'reemplazarTodo', 'buscarRegex',
                    'recortar', 'dividir', 'comienzaCon', 'subcadena', 'aMinusculasLocalizada', 'aMayusculasLocalizada', 'aMinusculas', 'aMayusculas', 'aCadena', 'recortarEspacios', 'recortarEspaciosAlFinal', 
                    'recortarEspaciosAlComienzo', 'valorDe',
                    #Number Object
                    'esNuN', 'esFinito', 'esEntero', 'esEnteroSeguro', 'interpretarDecimal', 'interpretarEntero','aExponencial', 'fijarDecimales', 'aCadenaLocalizada', 'aPrecision', 'aCadena', 'valorDe',
                    #Math Object
                    'absoluto', 'arcocoseno', 'arcocosenoHiperbolico', 'arcoseno', 'arcosenoHiperbolico', 'arcotangente', 'arcotangente2', 'arcotangenteHiperbolica', 'raizCubica', 'redondearHaciaArriba','cerosALaIzquierdaEn32Bits',
                    'coseno', 'cosenoHiperbolico', 'exponencial', 'exponencialMenos1', 'redondearHaciaAbajo', 'redondearAComaFlotante', 'hipotenusa', 'multiplicacionEntera', 'logaritmo', 'logaritmoBase10', 'logaritmoDe1Mas',
                    'logaritmoBase2', 'maximo', 'minimo', 'potencia', 'aleatorio', 'redondear', 'signo', 'seno', 'senoHiperbolico', 'raizCuadrada', 'tangente', 'tangenteHiperbolica', 'truncar',
                    #Array Object
                    'posicion', 'concatenar', 'copiarDentro', 'entradas', 'cada', 'llenar', 'filtrar', 'buscar', 'buscarIndice', 'buscarUltimo', 'buscarUltimoIndice', 'plano', 'planoMapear','paraCada', 'grupo','grupoAMapear',
                    'incluye', 'indiceDe', 'juntar', 'claves', 'ultimoIndiceDe', 'mapear', 'sacar', 'agregar', 'reducir', 'reducirDerecha', 'reverso', 'sacarPrimero', 'rodaja', 'algun', 'ordenar', 'empalmar', 'aCadenaLocalizada',
                    'aCadena', 'agregarInicio', 'valores'
        }

        self.operators = {
            "&&": "and",
            "||": "or",
            "...": "spread",
            "===": "strict_equal",
            "!==": "strict_neq",
            "==": "equal",
            "!=": "neq",
            "<=": "leq",
            ">=": "geq",
            "++": "increment",
            "--": "decrement",
            "+=": "plus_assign",
            "-=": "minus_assign",
            "*=": "times_assign",
            "/=": "div_assign",
            "%=": "mod_assign",
            "**=": "power_assign",
            "=>": "arrow",
            "??": "nulish",
            "**": "power",
            "+": "plus",
            "-": "minus",
            "*": "times",
            "/": "div",
            "%": "mod",
            "=": "assign",
            ">": "greater",
            "<": "less",
            "!": "not",
            "?": "ternary",
            ".": "period",
            ",": "comma",
            ";": "semicolon",
            ":": "colon",
            "{": "opening_key",
            "}": "closing_key",
            "(": "opening_par",
            ")": "closing_par",
            "[": "opening_bra",
            "]": "closing_bra"
        }

        self.regexPatterns = [
            ("comment_block", re.compile(r'/\*[\s\S]*?\*/')),
            ("comment_line", re.compile(r'//[^\n]*')),
            ("string", re.compile(r'"(?:\\.|[^"\n])*"|\'(?:\\.|[^\'\n])*\'')),
            ("regex", re.compile(r'/(?:\\.|[^/\n])+/')),
            ("number", re.compile(r'\d+\.\d+|\d+')),
            ("identifier", re.compile(
                r'(?:[$A-Za-z_]|[^\W\d]|\\u[0-9A-Fa-f]{4}|\\u\{[0-9A-Fa-f]+\})'
                r'(?:[$A-Za-z0-9_]|[^\W]|\\u[0-9A-Fa-f]{4}|\\u\{[0-9A-Fa-f]+\})*'
            )),
            ("whitespace", re.compile(r'\s+'))
        ]

        self.tokens = []

    def tokenize(self, code):

        row = 1
        col = 1
        pos = 0
        length = len(code)

        self.tokens = []

        while pos < length:

            match = None

            for name, pattern in self.regexPatterns:

                match = pattern.match(code, pos)

                if match:

                    lexeme = match.group(0)

                    if name == "whitespace":
                        pass

                    elif name == "comment_line":
                        pass

                    elif name == "comment_block":
                        pass

                    elif name == "identifier":

                        if lexeme in self.keywords:
                            self.tokens.append(
                                Token(EnumToken.KEYWORD, lexeme, row, col)
                            )
                        else:
                            self.tokens.append(
                                Token(EnumToken.ID, lexeme, row, col)
                            )

                    elif name == "number":
                        self.tokens.append(
                            Token(EnumToken.NUMBER, lexeme, row, col)
                        )

                    elif name == "string":
                        self.tokens.append(
                            Token(EnumToken.STRING, lexeme[1:-1], row, col)
                        )

                    elif name == "regex":
                        self.tokens.append(
                            Token(EnumToken.REGEX, lexeme[1:-1], row, col)
                        )

                    lines = lexeme.split('\n')

                    if len(lines) > 1:
                        row += len(lines) - 1
                        col = len(lines[-1]) + 1
                    else:
                        col += len(lexeme)

                    pos = match.end()
                    break

            if match:
                continue

            matchedOp = None
            for op in sorted(self.operators.keys(), key=len, reverse=True):

                if code.startswith(op, pos):
                    matchedOp = op
                    break

            if matchedOp:
                self.tokens.append(
                    Token(EnumToken.OPERATOR, self.operators[matchedOp], row, col, matchedOp)
                )

                pos += len(matchedOp)
                col += len(matchedOp)
                continue
            
            
            self.tokens.append(
                Token(EnumToken.ERROR, "", row, col)
            )
            for t in self.tokens:
                print(t)
            return

        for t in self.tokens:
            print(t)


def main():

    code = sys.stdin.read()
    lexer = Lexer()
    lexer.tokenize(code)


if __name__ == "__main__":
    main()