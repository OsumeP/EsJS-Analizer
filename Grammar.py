class Grammar:
    productions = {
        "S": [["A", "uno", "B", "C"], ["S", "dos"]],
        "A": [["B", "C", "D"], ["A", "tres"], ["ε"]],
        "B": [["D", "cuatro", "C", "tres"], ["ε"]],
        "C": [["cinco", "D", "B"], ["ε"]],
        "D": [["seis"], ["ε"]]
    }

    firsts: dict[str, set[str]]

    startSimb: str

    def __init__(self, startSimb: str):
        self.startSimb = startSimb
        self.firsts = {noTerminal: set() for noTerminal in self.productions}

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
            
obj = Grammar("S")
obj.computeFirst()
print(obj.firsts)