import re as r

class LexicAnalizer:

    keywords: set[str]

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