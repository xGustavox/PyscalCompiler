from tag import Tag
from lexer import Lexer
from colorama import init, Fore, Back, Style
import time

# ====================
# GUSTAVO FONTES CAMARGOS
# 117112318
# ====================

if __name__ == "__main__":

  start_time = time.time()
  init()

  lexer = Lexer('HelloWorld.txt')

  print(Fore.LIGHTMAGENTA_EX + '\n====== Lista de Tokens ======\n')
  token = lexer.proxToken()

  while (token is not -1 and token.getNome() != Tag.EOF):
    print(Fore.CYAN + token.toString(), Fore.WHITE + '(Ln ' + str(token.getLinha()) + ', Col ' + str(token.getColuna()) + ')')
    token = lexer.proxToken()

  print(Fore.LIGHTMAGENTA_EX + '\n====== Tabela de simbolos ======\n')
  lexer.printTS()

  lexer.closeFile()

  print(Fore.LIGHTMAGENTA_EX + '\n====== Fim da compilação ======\n')
  print(str(time.time() - start_time) + ' seg')