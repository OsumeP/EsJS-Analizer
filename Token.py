from EnumTokenModule import EnumToken
class Token:
    type: EnumToken
    name: str
    row: int
    col: int
    operation: str

    def __init__(self, type: EnumToken, name: str, row: int, col: int, operation: str = ""):
        self.type = type
        self.name = name
        self.row = row
        self.col = col
        self.operation = operation
    

    
    def __str__(self):
        if(self.type == EnumToken.KEYWORD):
            return f"<{self.name},{self.row},{self.col}>"
        if(self.type == EnumToken.ID):
            return f"<id,{self.name},{self.row},{self.col}>"
        if(self.type == EnumToken.NUMBER):
            return f"<tkn_num,{self.name},{self.row},{self.col}>"
        if(self.type == EnumToken.STRING):
            return f"<tkn_str,{self.name},{self.row},{self.col}>"
        if(self.type == EnumToken.OPERATOR):
            return f"<tkn_{self.name},{self.row},{self.col}>"
        if(self.type == EnumToken.REGEX):
            return f"<tkn_reg,{self.name},{self.row},{self.col}>"
        if(self.type == EnumToken.ERROR):
            return f">>> Error lexico (linea: {self.row}, posicion: {self.col})"