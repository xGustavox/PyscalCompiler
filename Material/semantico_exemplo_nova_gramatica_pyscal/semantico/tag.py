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
    OP_ATRIB = 18

    # Simbolos
    SMB_AB_CHA = 100
    SMB_FE_CHA = 101
    
    # Identificador
    ID = 20

    # Numeros
    INT = 30
    DOUBLE = 31

    # Constantes para tipos
    TIPO_VAZIO   = 1000;
    TIPO_LOGICO  = 1001;
    TIPO_INT     = 1002;
    TIPO_DOUBLE  = 1003;
    TIPO_ERRO    = 1004;
