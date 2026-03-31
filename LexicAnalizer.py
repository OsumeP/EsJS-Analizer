import re, sys

class LexicAnalizer:

    keywords: set[str]
    operations: dict[str, str]
    lexema: str
    row: int
    column: int
    isComment: bool
    isRegex: bool
    isString: bool
    canBe: bool
    inputCon: str
    index: int
    startLexema: int

    def __init__(self, inputCol: str):
        self.column = 1
        self.row = 1
        self.lexema = ""
        self.isComment = False
        self.isRegex = False
        self.inputCon = inputCol
        self.index = 0
        self.startLexema = 0
        self.canBe = True
        self.isString = False

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
        
        self.operations = {"&&": "and", "||": "or", "...": "spread", ".": "period", ",": "comma", ";": "semicolon", ":": "colon", "{": "opening_key", "}": "closing_key", "[": "opening_bra", "]": "closing_bra", 
                           "(": "opening_par", ")": "closing_par", "++": "increment", "--": "decrement", "%=": "mod_assign", "/=": "div_assign", "*=": "times_assign", "-=": "minus_assign", "+=": "plus_assign",
                           "**=": "power_assign", "+": "plus", "-": "minus", "*": "times", "/": "div", "**": "power", "%": "mod", "==": "equal", "===": "strict_equal", "!=": "neq", "!==": "strict_neq", "<=": "leq", ">=": "geq",
                           ">": "greater", "<": "less", "=": "assign", "=>": "arrow", "!": "not", "?": "ternary", "??": "nulish"}
    
    
    def getToken(self, string: str):
        #End comment
        if self.isComment:
            if re.search(r'\*/$', string):
                self.isComment = False
            return []
        #Start comment
        elif re.fullmatch(r'/\*[\s\S]*', string):
            self.isComment = True
            return []
        #Identifier
        elif re.fullmatch(r'(?:[$A-Za-z_\u00A0-\uFFFF]|\\u[0-9A-Fa-f]{4}|\\u\{[0-9A-Fa-f]+\})(?:[$A-Za-z0-9_\u00A0-\uFFFF]|\\u[0-9A-Fa-f]{4}|\\u\{[0-9A-Fa-f]+\})*',string):
            #Keyword
            if(string in self.keywords):
                return [string]
            else:
                return ["id", string]
        #String
        elif re.fullmatch(r'"(?:\\.|[^"\n])*"|\'(?:\\.|[^\'\n])*\'', string):
            self.isString = False
            return ["tkn_str", string[1:len(string) - 1]]
        #Partial String
        elif re.fullmatch(r'"(?:\\.|[^"\n])*|\'(?:\\.|[^\'\n])*', string) and self.canBe:
            self.isString = True
            return []
        #Number
        elif re.fullmatch(r'\d+\.\d+|\d+', string):
            return ["tkn_num", string]
        #Operations
        elif string in self.operations:
            return ["tkn_" + self.operations.get(string)]
        #One line comments and White spaces, tabs, \n, etc.
        elif re.fullmatch(r'\s+', string) or re.fullmatch(r'//[^\n]*', string) or re.fullmatch(r'(?:[$A-Za-z_\u00A0-\uFFFF]|\\u[0-9A-Fa-f]{0,4}|\\u\{[0-9A-Fa-f]*\})?(?:[$A-Za-z0-9_\u00A0-\uFFFF]|\\u[0-9A-Fa-f]{0,4}|\\u\{[0-9A-Fa-f]*\})*', string):
            return []
        #Regex
        elif re.fullmatch(r'/(.)+/', string):
            self.isRegex = False
            return ["tkn_reg", string[1: len(string) - 1]]
        #Partial Regex
        elif re.fullmatch(r'/(.)+/?', string) and self.canBe:
            self.isRegex = True
            return []
        elif (string == ".." or re.fullmatch(r'\d+\.\d*', string)) and self.canBe:
            return []

        return None
    
    def nextToken(self):

        while self.index < len(self.inputCon) + 1:
            if self.index == len(self.inputCon):
                if self.lexema:
                    token = self.getToken(self.lexema)
                    if token and len(token) > 0:
                        result = [*token, self.row, self.column - len(self.lexema)]
                        self.lexema = ""
                        return result
                return None
            
            char: str = self.inputCon[self.index]
            self.index += 1
            
            flagComment: bool = self.isComment
            flagRegex: bool = self.isRegex
            result = None

            token = self.getToken(self.lexema + char)
            
            if(char == "\n" and self.isRegex):
                self.isRegex = False
                self.canBe = False
                self.column -= len(self.lexema) - 1
                self.index = self.startLexema + 1
                self.lexema = "/"
                continue

            if(char == "\n" and self.isString):
                self.isString = False
                self.canBe = False
                self.column -= len(self.lexema)
                self.index = self.startLexema
                self.lexema = ""
                continue

            if(len(self.lexema) == 2 and self.lexema[0] == "." and self.lexema[0] == "." and token is None):
                self.canBe = False
                self.column -= len(self.lexema)
                self.index = self.startLexema
                self.lexema = ""
                continue

            if(re.fullmatch(r"\d+\.",self.lexema) and not (char >= "0" and char <= "9") ):
                self.canBe = False
                self.column -= len(self.lexema)
                self.index = self.startLexema
                self.lexema = ""
                continue

            if(token is None):
                token = self.getToken(self.lexema)
                lgthLexema: int = len(self.lexema)
                self.lexema = char
                self.startLexema = self.index - 1

                if(token is None):
                    return [self.row, self.column - lgthLexema]

                if(len(token) > 0):
                    result = [*token, self.row, self.column - lgthLexema]
            else:
                self.lexema += char
                if(flagComment and not self.isComment):
                    self.lexema = ""
                if(flagRegex and not self.isRegex):
                    lgthLexema: int = len(self.lexema) - 1
                    result = [*token, self.row, self.column - lgthLexema]
                    self.lexema = ""

            if(char == "\n"):
                self.row += 1
                self.column = 0
            self.column += 1

            if(result is not None):
                self.canBe = True
                return result

def printToken(token):
    result: str = f"<{token[0]},{token[1]},{token[2]}"
    if(len(token) > 3):
        result += "," + str(token[3])
    result += ">"

    print(result)

            
            


obj: LexicAnalizer = LexicAnalizer(sys.stdin.read())
obj.inputCon += "\n"
token = obj.nextToken()

while(token is not None):
    if(len(token) == 2):
        print(f">>> Error lexico (linea: {token[0]}, posicion: {token[1]})")
        break
    printToken(token)
    token = obj.nextToken()