from enum import Enum

class EnumToken(Enum):
    ID = 1
    KEYWORD = 2
    NUMBER = 3
    STRING = 4
    OPERATOR = 5
    REGEX = 6
    ERROR = 7
    END = 8