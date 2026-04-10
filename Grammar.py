class Grammar:
    productions = {
        "S": [["A", "uno", "B", "C"], ["S", "dos"]],
        "A": [["B", "C", "D"], ["A", "tres"], ["ε"]],
        "B": [["D", "cuatro", "C", "tres"], ["ε"]],
        "C": [["cinco", "D", "B"], ["ε"]],
        "D": [["seis"], ["ε"]]
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


            
obj = Grammar("S")
obj.computeFirst()
obj.computeNext()
obj.computePred()
# print(obj.firsts)
# print(obj.nexts)
print(obj.pred)