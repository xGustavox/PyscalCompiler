import sys

from ts import TS
from tag import Tag
from token import Token
from lexer import Lexer

"""
 * *
 * [TODO]: tratar retorno 'None' do Lexer que esta sem Modo Panico
 *
 *
 * Modo Pânico do Parser: 
    * Para tomar a decisao de escolher uma das regras (quando mais de uma disponivel),
    * o parser usa incialmente o FIRST(), e para alguns casos, FOLLOW(). Essa informacao eh dada pela TP.
    * Caso nao existe a regra na TP que corresponda ao token da entrada,
    * informa-se uma mensagem de erro e inicia-se o Modo Panico:
    * [1] calcula-se o FOLLOW do NAO-TERMINAL (a esquerda) da regra atual: esse NAO-TERMINAL estara no topo da pilha;
    * [2] se o token da entrada estiver neste FOLLOW, desempilha-se o nao-terminal atual - metodo synch() - retorna da recursao;
    * [3] caso contrario, a entrada eh avancada para uma nova comparacao e mantem-se o nao-terminal no topo da pilha 
    * (se for a pilha recursiva, mantem o procedimento no topo da recursao) - metodo skip().
    * 
    * O Modo Panico encerra-se, 'automagicamente', quando um token esperado aparece.
    * Para NAO implementar o Modo Panico, basta sinalizar erro quando nao
    * for possivel utilizar alguma das regras. Em seguida, encerrar a execucao usando sys.exit(0).
"""

class Parser():

   def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
   
   def skip(self, message):
      self.sinalizaErroSintatico(message)
      self.advance()

   # verifica token esperado t 
   def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False

   """
   LEMBRETE:
   Todas as decisoes do Parser, sao guiadas pela Tabela Preditiva (TP)
   """

   # Programa -> CMD EOF
   def Programa(self):
      self.Cmd()
      if(self.token.getNome() != Tag.EOF):
         self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")

   def Cmd(self):
      # Cmd -> if E then { CMD } CMD'
      if(self.eat(Tag.KW_IF)): 
         self.E()

         """
         ATENCAO: no caso 'terminal esperado' vs 'terminal na entrada', o 'terminal esperado' 
         não casou com o terminal da entrada, dai vamos simular o 'desempilha terminal',
         isto eh, continue a varredura, mantendo a entrada.
         */
         """
         if(not self.eat(Tag.KW_THEN)):
            self.sinalizaErroSintatico("Esperado \"then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         if(not self.eat(Tag.SMB_AB_CHA)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FE_CHA)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.CmdLinha()
      # Cmd -> print T
      elif(self.eat(Tag.KW_PRINT)):
         self.T()
      else:
         """
         Percebemos na TP que os metodos skip() ou synch() podem ser executados. 
         A ideia do skip() eh avancar a entrada sem retirar Cmd() da pilha(recursiva). Porem chegamos ao fim 
         do metodo Cmd(). Como podemos mante-lo na pilha recursiva? Simples, chamamos o proprio metodo Cmd().
         A ideia do synch() eh tirar Cmd() da pilha(recursiva), pois apos esse procedimento, algum simbolo
         na pilha ira resolver a entrada. Como retirar esse procedimento da pilha? Um simples 'return'. 
         Lembres-se que o synch() tem preferencia em ser executado em relacao ao skip().
         */
         """

         # synch: FOLLOW(Cmd)
         if(self.token.getNome() == Tag.SMB_FE_CHA or self.token.getNome() == Tag.EOF):
            self.sinalizaErroSintatico("Esperado \"if, print\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return
         else:
            self.skip("Esperado \"if, print\", encontrado " + "\"" + self.token.getLexema() + "\"")
            if(self.token.getNome() != Tag.EOF): self.Cmd()

   def CmdLinha(self):
      # CmdLinha -> else { CMD }
      if(self.eat(Tag.KW_ELSE)):
         if(not self.eat(Tag.SMB_AB_CHA)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FE_CHA)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
      # CmdLinha -> epsilon
      elif(self.token.getNome() == Tag.SMB_FE_CHA or self.token.getNome() == Tag.EOF):
         return
      else:
         self.skip("Esperado \"else, }\", encontrado " + "\"" + self.token.getLexema() + "\"")
         if(self.token.getNome() != Tag.EOF): self.CmdLinha()

   # E -> F E'
   def E(self):
      if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.NUM):
         self.F()
         self.ELinha()
      else:
         # synch: FOLLOW(E)
         if(self.token.getNome() == Tag.KW_THEN):
            self.sinalizaErroSintatico("Esperado \"id, num\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return
         else:
            self.skip("Esperado \"id, num\", encontrado " + "\"" + self.token.getLexema() + "\"")
            if(self.token.getNome() != Tag.EOF): self.E()

   '''
   E' --> ">" F E'  | "<" F E' | 
          ">=" F E' | "<=" F E'| 
          "==" F E' | "!=" F E'| epsilon
   '''
   def ELinha(self):
      if(self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MAIOR_IGUAL) or 
         self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE)):
         self.F()
         self.ELinha()
      elif(self.token.getNome() == Tag.KW_THEN):
         return
      else:
         self.skip("Esperado \">, <, >=, <=, ==, !=, then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         if(self.token.getNome() != Tag.EOF): self.ELinha();

   def F(self):
      if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.NUM):
         self.T()
         self.FLinha()
      else:
         # synch: FOLLOW(F)
         if(self.token.getNome() == Tag.KW_THEN or self.token.getNome() == Tag.OP_MENOR or
            self.token.getNome() == Tag.OP_MAIOR or self.token.getNome() == Tag.OP_MENOR_IGUAL or
            self.token.getNome() == Tag.OP_MAIOR_IGUAL or self.token.getNome() == Tag.OP_IGUAL or
            self.token.getNome() == Tag.OP_DIFERENTE):
            self.sinalizaErroSintatico("Esperado \"id, num\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return
         else:
            self.skip("Esperado \"id, num\", encontrado " + "\"" + self.token.getLexema() + "\"")
            if(self.token.getNome() != Tag.EOF): self.F()

   # F'  --> "+" T F' | "-" T F' | epsilon
   def FLinha(self):
      if(self.eat(Tag.OP_SOMA) or self.eat(Tag.OP_SUB)):
         self.T()
         self.FLinha()
      elif(self.token.getNome() == Tag.OP_MAIOR or self.token.getNome() == Tag.OP_MENOR or
           self.token.getNome() == Tag.OP_MAIOR_IGUAL or self.token.getNome() == Tag.OP_MENOR_IGUAL or
           self.token.getNome() == Tag.OP_DIFERENTE or self.token.getNome() == Tag.OP_IGUAL or
           self.token.getNome() == Tag.KW_THEN):
         return
      else:
         self.skip("Esperado \"+, -, >, <, >=, <=, ==, !=, then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         if(self.token.getNome() != Tag.EOF): self.FLinha()

   # T -> id | num
   def T(self):
      if(not self.eat(Tag.ID) and not self.eat(Tag.NUM)):
         # synch: FOLLOW(T)
         if(self.token.getNome() == Tag.OP_MAIOR or self.token.getNome() == Tag.OP_MENOR or
            self.token.getNome() == Tag.OP_MAIOR_IGUAL or self.token.getNome() == Tag.OP_MENOR_IGUAL or
            self.token.getNome() == Tag.OP_DIFERENTE or self.token.getNome() == Tag.OP_IGUAL or
            self.token.getNome() == Tag.KW_THEN or self.token.getNome() == Tag.OP_SOMA or
            self.token.getNome() == Tag.OP_SUB):
            self.sinalizaErroSintatico("Esperado \"num, id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            return
         else:
            self.skip("Esperado \"num, id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
            if(self.token.getNome() != Tag.EOF): self.T()
