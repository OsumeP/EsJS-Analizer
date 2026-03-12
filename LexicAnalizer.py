import re

class LexicAnalizer:

    keywords: set[str]
    operations: dict[str, str]

    def __init__(self):
        self.keywords = {
                    #Control Keywords
                    'capturar', 'caso', 'con', 'continuar', 'crear', 'elegir', 'elegir', 'mientras', 'para', 'retornar', 'sino', 'si', 'constructor', 'eliminar', 'extiende', 'finalmente', 'instanciaDe',
                    'intentar', 'lanzar', 'longitud', 'romper', 'simbolo', 'subcad', 'tipoDe', 'vacio', 'ambiente', 'super', 'de', 'en', 'clase', 'const', 'var', 'mut', 'porDefecto', 'funcion',
                    #Language Constants
                    'falso', 'nulo', 'verdadero', 'indefinido', 'Infinito', 'NuN', 
                    #Support Functions
                    'consola', 'Fecha', 'Numero', 'Mate', 'Matriz', 'Arreglo', 'Booleano', 'Cadena', 'Funcion', 
                    #Console Object
                    'afirmar', 'limpiar', 'listar', 'listarXml', 'error',
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
                           "**=": "power_assign", "+": "plus", "-": "minus", "*": "times", "/": "div", "%": "mod", "==": "equal", "===": "strict_equal", "!=": "neq", "!==": "strict_neq", "<=": "leq", ">=": "geq",
                           ">": "greater", "<": "less", "=": "assign", "=>": "arrow", "!": "not", "?": "ternary", "??": "nulish"}
    
    def verifyRegex(self, string: str):
        #Identifier
        if re.fullmatch(r'(?!\d)[$\w_][\w$]*',string):
            #Keyword
            if(string in self.keywords):
                print("KeyWord")
            else:
                print("Identificador")
        #String
        elif re.fullmatch(r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'', string):
            print("str")
        #Number
        elif re.fullmatch(r'\d+\.\d+|\d+|\.\d+|\d+\.\d*', string):
            print("num")
        #Operations
        elif string in self.operations:
            print(self.operations.get(string))
        #Regex
        elif re.fullmatch(r'/([^/\\]|\\.)+/[gimuy]*', string):
            print("reg")

obj: LexicAnalizer = LexicAnalizer()

obj.verifyRegex(".3")