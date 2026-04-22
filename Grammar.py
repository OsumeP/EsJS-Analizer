from SintacticGenerator import SintacticGenerator
from EnumTokenModule import EnumToken
class Grammar:
    EPSILON = ["ε"]

    productions = {
 
    # ─── Programa ────────────────────────────────────────────────────────────
    "Programa": [
        ["ListaDeclaraciones"],
    ],
 
    # ─── Lista de declaraciones ───────────────────────────────────────────────
    # ListaDeclaraciones → Declaracion ListaDeclaraciones | ε
    "ListaDeclaraciones": [
        ["Declaracion", "ListaDeclaraciones"],
        EPSILON,
    ],
 
    # ─── Declaracion ─────────────────────────────────────────────────────────
    "Declaracion": [
        ["DeclVar"],
        ["DeclConst"],
        ["DeclFuncion"],
        ["SentSi"],
        ["SentMientras"],
        ["SentHacerMientras"],
        ["SentPara"],
        ["SentElegir"],
        ["SentRetornar"],
        ["SentRomper"],
        ["SentContinuar"],
        ["Bloque"],
        ["SentExpr"],
    ],
 
    # ─── Variables ───────────────────────────────────────────────────────────
    # DeclVar → mut ID InicOpcional RestDeclaradores ;
    # DeclVar → var ID InicOpcional RestDeclaradores ;
    #
    # Esto cubre tanto la declaración simple:
    #   mut x = 1;
    # como la declaración múltiple en una sola línea:
    #   mut mistake, identif;
    #   mut a = 1, b = 2, c;
    "DeclVar": [
        ["mut", EnumToken.ID, "InicOpcional", "RestDeclaradores", ";"],
        ["var", EnumToken.ID, "InicOpcional", "RestDeclaradores", ";"],
    ],
 
    # RestDeclaradores → , ID InicOpcional RestDeclaradores | ε
    # Permite encadenar más declaradores separados por coma.
    "RestDeclaradores": [
        [",", EnumToken.ID, "InicOpcional", "RestDeclaradores"],
        EPSILON,
    ],
 
    # DeclConst → const ID = Expresion ;
    "DeclConst": [
        ["const", EnumToken.ID, "=", "Expresion", ";"],
    ],
 
    # InicOpcional → = Expresion | ε
    "InicOpcional": [
        ["=", "Expresion"],
        EPSILON,
    ],
 
    # ─── Funciones ───────────────────────────────────────────────────────────
    # DeclFuncion → funcion ID ( ListaParams ) Bloque
    "DeclFuncion": [
        ["funcion", EnumToken.ID, "(", "ListaParams", ")", "Bloque"],
    ],
 
    # ListaParams → ID RestParams | ε
    "ListaParams": [
        [EnumToken.ID, "RestParams"],
        EPSILON,
    ],
 
    # RestParams → , ID RestParams | ε
    "RestParams": [
        [",", EnumToken.ID, "RestParams"],
        EPSILON,
    ],
 
    # ─── Bloque ──────────────────────────────────────────────────────────────
    "Bloque": [
        ["{", "ListaDeclaraciones", "}"],
    ],
 
    # ─── Retornar ────────────────────────────────────────────────────────────
    "SentRetornar": [
        ["retornar", "ExprOpcional", ";"],
    ],
 
    # ExprOpcional → Expresion | ε
    "ExprOpcional": [
        ["Expresion"],
        EPSILON,
    ],
 
    # ─── Control de flujo ────────────────────────────────────────────────────
    # SentSi → si ( Expresion ) Bloque SinoOpcional
    "SentSi": [
        ["si", "(", "Expresion", ")", "Bloque", "SinoOpcional"],
    ],
 
    # SinoOpcional → sino Bloque | ε
    "SinoOpcional": [
        ["sino", "Bloque"],
        EPSILON,
    ],
 
    # SentMientras → mientras ( Expresion ) Bloque
    "SentMientras": [
        ["mientras", "(", "Expresion", ")", "Bloque"],
    ],
 
    # SentHacerMientras → hacer Bloque mientras ( Expresion ) ;
    "SentHacerMientras": [
        ["hacer", "Bloque", "mientras", "(", "Expresion", ")", ";"],
    ],
 
    # SentPara → para ( InicPara CondPara ; ActPara ) Bloque
    "SentPara": [
        ["para", "(", "InicPara", "CondPara", ";", "ActPara", ")", "Bloque"],
    ],
 
    # InicPara → DeclVarSinPuntoComa ; | Expresion ; | ;
    "InicPara": [
        ["DeclVarSinPuntoComa", ";"],
        ["Expresion", ";"],
        [";"],
    ],
 
    # DeclVarSinPuntoComa → mut ID InicOpcional RestDeclaradores
    #                      | var ID InicOpcional RestDeclaradores
    # Se reutiliza RestDeclaradores para que el for también pueda tener
    # múltiples declaradores: para (mut i = 0, j = 1; ...)
    "DeclVarSinPuntoComa": [
        ["mut", EnumToken.ID, "InicOpcional", "RestDeclaradores"],
        ["var", EnumToken.ID, "InicOpcional", "RestDeclaradores"],
    ],
 
    # CondPara → Expresion | ε
    "CondPara": [
        ["Expresion"],
        EPSILON,
    ],
 
    # ActPara → Expresion | ε
    "ActPara": [
        ["Expresion"],
        EPSILON,
    ],
 
    # ─── Elegir (switch) ─────────────────────────────────────────────────────
    # SentElegir → elegir ( Expresion ) { ListaCasos PorDefectoOpc }
    "SentElegir": [
        ["elegir", "(", "Expresion", ")", "{", "ListaCasos", "PorDefectoOpc", "}"],
    ],
 
    # ListaCasos → Caso ListaCasos | ε
    "ListaCasos": [
        ["Caso", "ListaCasos"],
        EPSILON,
    ],
 
    # Caso → caso Expresion : ListaDeclaraciones
    "Caso": [
        ["caso", "Expresion", ":", "ListaDeclaraciones"],
    ],
 
    # PorDefectoOpc → porDefecto : ListaDeclaraciones | ε
    "PorDefectoOpc": [
        ["porDefecto", ":", "ListaDeclaraciones"],
        EPSILON,
    ],
 
    # ─── Romper / Continuar ──────────────────────────────────────────────────
    "SentRomper": [
        ["romper", ";"],
    ],
 
    "SentContinuar": [
        ["continuar", ";"],
    ],
 
    # ─── Sentencia expresión ─────────────────────────────────────────────────
    "SentExpr": [
        ["Expresion", ";"],
    ],
 
    # ─── Jerarquía de expresiones ────────────────────────────────────────────
    # Expresion → ExpAsign
    "Expresion": [
        ["ExpAsign"],
    ],
 
    # ExpAsign → ExpOr RestAsign
    "ExpAsign": [
        ["ExpOr", "RestAsign"],
    ],
 
    # RestAsign → = ExpAsign | += ExpAsign | -= ExpAsign
    #           | *= ExpAsign | /= ExpAsign | %= ExpAsign | ε
    "RestAsign": [
        ["=",  "ExpAsign"],
        ["+=", "ExpAsign"],
        ["-=", "ExpAsign"],
        ["*=", "ExpAsign"],
        ["/=", "ExpAsign"],
        ["%=", "ExpAsign"],
        EPSILON,
    ],
 
    # ExpOr → ExpAnd RestOr
    "ExpOr": [
        ["ExpAnd", "RestOr"],
    ],
 
    # RestOr → || ExpAnd RestOr | ε
    "RestOr": [
        ["||", "ExpAnd", "RestOr"],
        EPSILON,
    ],
 
    # ExpAnd → ExpIgualdad RestAnd
    "ExpAnd": [
        ["ExpIgualdad", "RestAnd"],
    ],
 
    # RestAnd → && ExpIgualdad RestAnd | ε
    "RestAnd": [
        ["&&", "ExpIgualdad", "RestAnd"],
        EPSILON,
    ],
 
    # ExpIgualdad → ExpRelac RestIgualdad
    "ExpIgualdad": [
        ["ExpRelac", "RestIgualdad"],
    ],
 
    # RestIgualdad → === ExpRelac RestIgualdad | !== ExpRelac RestIgualdad
    #              | ==  ExpRelac RestIgualdad | !=  ExpRelac RestIgualdad | ε
    "RestIgualdad": [
        ["===", "ExpRelac", "RestIgualdad"],
        ["!==", "ExpRelac", "RestIgualdad"],
        ["==",  "ExpRelac", "RestIgualdad"],
        ["!=",  "ExpRelac", "RestIgualdad"],
        EPSILON,
    ],
 
    # ExpRelac → ExpAdic RestRelac
    "ExpRelac": [
        ["ExpAdic", "RestRelac"],
    ],
 
    # RestRelac → < ExpAdic RestRelac | > ExpAdic RestRelac
    #           | <= ExpAdic RestRelac | >= ExpAdic RestRelac | ε
    "RestRelac": [
        ["<",  "ExpAdic", "RestRelac"],
        [">",  "ExpAdic", "RestRelac"],
        ["<=", "ExpAdic", "RestRelac"],
        [">=", "ExpAdic", "RestRelac"],
        EPSILON,
    ],
 
    # ExpAdic → ExpMult RestAdic
    "ExpAdic": [
        ["ExpMult", "RestAdic"],
    ],
 
    # RestAdic → + ExpMult RestAdic | - ExpMult RestAdic | ε
    "RestAdic": [
        ["+", "ExpMult", "RestAdic"],
        ["-", "ExpMult", "RestAdic"],
        EPSILON,
    ],
 
    # ExpMult → ExpUnaria RestMult
    "ExpMult": [
        ["ExpUnaria", "RestMult"],
    ],
 
    # RestMult → * ExpUnaria RestMult | / ExpUnaria RestMult
    #          | % ExpUnaria RestMult | ε
    "RestMult": [
        ["*", "ExpUnaria", "RestMult"],
        ["/", "ExpUnaria", "RestMult"],
        ["%", "ExpUnaria", "RestMult"],
        EPSILON,
    ],
 
    # ExpUnaria → ! ExpUnaria | - ExpUnaria | tipoDe ExpUnaria | ExpPostfija
    "ExpUnaria": [
        ["!",      "ExpUnaria"],
        ["-",      "ExpUnaria"],
        ["tipoDe", "ExpUnaria"],
        ["ExpPostfija"],
    ],
 
    # ExpPostfija → ExpPrimaria RestPostfija
    "ExpPostfija": [
        ["ExpPrimaria", "RestPostfija"],
    ],
 
    # RestPostfija → [ Expresion ] RestPostfija
    #              | . ID RestPostfija
    #              | ( ListaArgs ) RestPostfija
    #              | ε
    "RestPostfija": [
        ["[", "Expresion", "]", "RestPostfija"],
        [".", EnumToken.ID,     "RestPostfija"],
        ["(", "ListaArgs", ")", "RestPostfija"],
        EPSILON,
    ],
 
    # ─── Expresiones primarias ────────────────────────────────────────────────
    # Se agrega ExpArrow como alternativa que comienza con "(" para cubrir:
    #   (a, b) => a + b          — cuerpo expresión
    #   (a, b) => { retornar a + b; }  — cuerpo bloque
    #
    # NOTA LL(1): tanto "( Expresion )" como "( ListaParams ) =>" empiezan
    # con "(". Para mantener el determinismo se factoriza en ExpPrimParentesis,
    # que tras consumir "(" decide por lookahead interno en el parser.
    # La gramática aquí refleja las dos formas; el parser usa la tabla de
    # predicción basada en el token que sigue al ")" para elegir entre
    # expresión agrupada y arrow function.
    #
    # ExpPrimaria → ID
    #             | Literal
    #             | ExpPrimParentesis    ← agrupa "( Expr )" y "( Params ) =>"
    #             | LiteralArreglo
    #             | LiteralObjeto
    #             | funcion IDOpcional ( ListaParams ) Bloque
    #             | crear ExpPostfija
    "ExpPrimaria": [
        [EnumToken.ID],
        ["Literal"],
        ["ExpPrimParentesis"],
        ["LiteralArreglo"],
        ["LiteralObjeto"],
        ["funcion", "IDOpcional", "(", "ListaParams", ")", "Bloque"],
        ["crear", "ExpPostfija"],
    ],
 
    # ExpPrimParentesis → ( ContenidoParentesis )  RestArrow
    # RestArrow decide si es arrow ( => CuerpoArrow ) o expresión agrupada (ε).
    # Así se factoriza el prefijo común "(" y se mantiene LL(1).
    "ExpPrimParentesis": [
        ["(", "ContenidoParentesis", ")", "RestArrow"],
    ],
 
    # ContenidoParentesis → ListaParams   (sirve tanto para parámetros como
    #                                      para una expresión simple, ya que
    #                                      un ID solo es válido en ambos casos)
    # En el caso de expresión agrupada: "( Expresion )" → ListaParams = ID,
    # y RestArrow = ε, por lo que se trata como expresión.
    # En el caso arrow: "( a, b ) =>" → ListaParams = ID RestParams, y
    # RestArrow = => CuerpoArrow.
    "ContenidoParentesis": [
        ["ListaParams"],
    ],
 
    # RestArrow → => CuerpoArrow | ε
    # Si el token siguiente al ")" es "=>", es una arrow function.
    # Si no, es una expresión agrupada normal.
    "RestArrow": [
        ["=>", "CuerpoArrow"],
        EPSILON,
    ],
 
    # CuerpoArrow → Bloque | Expresion
    # Arrow con cuerpo bloque:      (a, b) => { retornar a + b; }
    # Arrow con cuerpo expresión:   (a, b) => a + b
    "CuerpoArrow": [
        ["Bloque"],
        ["Expresion"],
    ],
 
    # IDOpcional → ID | ε
    "IDOpcional": [
        [EnumToken.ID],
        EPSILON,
    ],
 
    # ─── Literales ────────────────────────────────────────────────────────────
    # Literal → NUMERO | CADENA | verdadero | falso | nulo | indefinido
    "Literal": [
        [EnumToken.NUMBER],
        [EnumToken.STRING],
        ["verdadero"],
        ["falso"],
        ["nulo"],
        ["indefinido"],
    ],
 
    # LiteralArreglo → [ ListaElems ]
    "LiteralArreglo": [
        ["[", "ListaElems", "]"],
    ],
 
    # ListaElems → Expresion RestElems | ε
    "ListaElems": [
        ["Expresion", "RestElems"],
        EPSILON,
    ],
 
    # RestElems → , Expresion RestElems | ε
    "RestElems": [
        [",", "Expresion", "RestElems"],
        EPSILON,
    ],
 
    # LiteralObjeto → { ListaPropiedades }
    "LiteralObjeto": [
        ["{", "ListaPropiedades", "}"],
    ],
 
    # ListaPropiedades → Propiedad RestPropiedades | ε
    "ListaPropiedades": [
        ["Propiedad", "RestPropiedades"],
        EPSILON,
    ],
 
    # Propiedad → ClaveProp : Expresion
    "Propiedad": [
        ["ClaveProp", ":", "Expresion"],
    ],
 
    # ClaveProp → ID | CADENA | NUMERO
    "ClaveProp": [
        [EnumToken.ID],
        [EnumToken.STRING],
        [EnumToken.NUMBER],
    ],
 
    # RestPropiedades → , Propiedad RestPropiedades | ε
    "RestPropiedades": [
        [",", "Propiedad", "RestPropiedades"],
        EPSILON,
    ],
 
    # ─── Argumentos de llamada ────────────────────────────────────────────────
    # ListaArgs → Expresion RestArgs | ε
    "ListaArgs": [
        ["Expresion", "RestArgs"],
        EPSILON,
    ],
 
    # RestArgs → , Expresion RestArgs | ε
    "RestArgs": [
        [",", "Expresion", "RestArgs"],
        EPSILON,
    ],
}

    firsts: dict[str, set[str]]
    nexts: dict[str, set[str]]
    pred: dict[str, list[set[str]]]

    startSimb: str

    def __init__(self, startSimb: str):
        self.startSimb = startSimb
        self.firsts = {noTerminal: set() for noTerminal in self.productions}
        self.nexts = {noTerminal: set() for noTerminal in self.productions}
        self.pred = {noTerminal: [] for noTerminal in self.productions}

    def computeFirst(self):
        change = True

        while change:
            change = False

            for noTerminal in self.productions:
                productionList = self.productions[noTerminal]
                currFirst = self.firsts[noTerminal]
                size = len(currFirst)

                for sequence in productionList:
                    currFirst.update(self.getFirst(sequence))

                if(len(currFirst) > size):
                    change = True


    def getFirst(self, sequence):
        result = set()

        for symbol in sequence:
            
            #Terminal
            if(symbol not in self.productions):
                result.add(symbol)
                return result
            
            firstAdd = self.firsts[symbol]
            result.update(firstAdd)
            result.discard("ε")

            if("ε" not in firstAdd):
                return result
        #First(sequence) contains ε
        result.add("ε")
        return result
    
    def computeNext(self):
        self.nexts[self.startSimb].add("$")

        changed = True

        while(changed):
            changed = False

            for noTerminal in self.productions:
                productionList = self.productions[noTerminal]

                for production in productionList:

                    for i in range(len(production)):
                        symbol = production[i]

                        #No Terminal
                        if symbol in self.productions:
                            size = len(self.nexts[symbol])

                            if(i + 1 < len(production)):
                                addFirst = self.getFirst(production[i+1:])
                                self.nexts[symbol].update(addFirst)
                                self.nexts[symbol].discard("ε")

                                if "ε" in addFirst:
                                    self.nexts[symbol].update(self.nexts[noTerminal])
                            else:
                                self.nexts[symbol].update(self.nexts[noTerminal])
                            
                            if len(self.nexts[symbol]) > size:
                                changed = True

    def computePred(self):
        for symbol in self.productions:
            productionList = self.productions[symbol]
            predictList = self.pred[symbol]
            for production in productionList:
                firstS = self.getFirst(production)
                setAdded = set()
                if "ε" in firstS:
                    setAdded.update(firstS - {"ε"})
                    setAdded.update(self.nexts[symbol])
                else:
                    setAdded.update(firstS)
                predictList.append(setAdded)


            
obj = Grammar("Programa")
obj.computeFirst()
obj.computeNext()
obj.computePred()
sg = SintacticGenerator(obj.productions, obj.pred)
sg.generate_parser()
# print(obj.firsts)
# print(obj.nexts)
# print("Producciones")
# print(obj.productions)
# print("Predeccion")
# print(obj.pred)