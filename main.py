from tag import Tag
from lexer import Lexer
from colorama import init, Fore, Back, Style
from parser import Parser
import time

# ====================
# GUSTAVO FONTES CAMARGOS
# 117112318
# ====================

if __name__ == "__main__":

  start_time = time.time()
  init()

  lexer = Lexer('HelloWorld.txt')
  parser = Parser(lexer)

  print(Fore.WHITE + '\n====== Pyscal Compiler ======\n')

  parser.Programa()

  print(Fore.LIGHTMAGENTA_EX + '\n====== Tabela de simbolos ======\n')
  lexer.printTS()

  lexer.closeFile()

  print(Fore.LIGHTMAGENTA_EX + '\n====== Fim da compilação ======\n')
  print(str(time.time() - start_time) + ' seg')