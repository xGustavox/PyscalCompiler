from enum import Enum

class Tag(Enum):
    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_CLASS = 1
    KW_END = 2
    KW_DEF = 3
    KW_RETURN = 4
    KW_DEFSTATIC = 5
    KW_VOID = 6
    KW_MAIN = 7
    KW_STRING = 8
    KW_BOOL = 9
    KW_INTEGER = 10
    KW_DOUBLE = 12
    KW_IF = 13
    KW_ELSE = 14
    KW_WHILE = 15
    KW_WRITE = 16
    KW_TRUE = 17
    KW_FALSE = 18
    KW_OR = 20
    KW_AND = 21

    # Operadores 
    OP_ATTRIBUTION = 19 
    OP_LESS = 22
    OP_LESS_EQUAL = 23
    OP_GREATER = 24
    OP_GREATER_EQUAL = 25
    OP_EQUAL = 26
    OP_DIFERENT = 27
    OP_SLASH = 28
    OP_TIMES = 29
    OP_MINUS = 30
    OP_NEGATIVE = 47
    OP_PLUS = 31
    OP_EXCLAMATION_MARK = 32

    # Separators
    SP_COLONS = 33
    SP_DOT = 34
    SP_SEMICOLON = 35
    SP_OPEN_BRAKETS = 36
    SP_CLOSE_BRAKETS = 37
    SP_COMMA = 38
    SP_OPEN_SQUARE_BRACKET = 39
    SP_CLOSE_SQUARE_BRACKET = 40

    # Identificador / Strings
    ID = 41
    CONST_STRING = 42

    # Numeros
    NUM = 43
    CONST_INTEGER = 44
    CONST_DOUBLE = 45

    #Comment
    COMMENT = 46

    EMPTY_TYPE = 1000
    LOGIC_TYPE = 1001
    INT_TYPE = 1002
    DOUBLE_TYPE = 1003
    ERRO_TYPE = 1004
