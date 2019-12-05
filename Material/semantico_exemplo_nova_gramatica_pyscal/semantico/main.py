from tag import Tag
from token import Token
from lexer import Lexer
from parser import Parser

if __name__ == "__main__":
   lexer = Lexer('HelloWorld.txt')
   parser = Parser(lexer)

   parser.Programa()

   parser.lexer.closeFile()

   print("\n=>Tabela de simbolos:")
   lexer.printTS()
   lexer.closeFile()
    
   print('\n=> Fim da compilacao')
