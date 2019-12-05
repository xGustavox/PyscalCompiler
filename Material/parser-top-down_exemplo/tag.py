from enum import Enum

class Tag(Enum):
    '''
    Uma representacao em constante de todos os nomes 
    de tokens para a linguagem.
    '''

    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_IF = 1
    KW_ELSE = 2
    KW_THEN = 3
    KW_PRINT = 4

    # Operadores 
    OP_MENOR = 10
    OP_MENOR_IGUAL = 11
    OP_MAIOR_IGUAL = 12
    OP_MAIOR = 13
    OP_IGUAL = 14
    OP_DIFERENTE = 15
    OP_SOMA = 16
    OP_SUB = 17

    # Simbolos
    SMB_AB_CHA = 18
    SMB_FE_CHA = 19
    
    # Identificador
    ID = 20

    # Numeros
    NUM = 30
