import sys
import copy

from tag import Tag
from token import Token
from lexer import Lexer
from no import No

class Parser():

   def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo
      if self.token is None: # erro no Lexer
        sys.exit(0)

   def sinalizaErroSemantico(self, message):
      print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def advance(self):
      # print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()

      if self.token is None: # erro no Lexer
        sys.exit(0)
   
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
         sys.exit(0)

   def Cmd(self):
      tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da segunda regra)

      # Cmd -> if E then { CMD } CMD'
      if(self.eat(Tag.KW_IF)): 

         noE = self.E()
         if noE.tipo != Tag.TIPO_LOGICO:
            self.sinalizaErroSemantico("Expressao mal formada.")

         if(not self.eat(Tag.KW_THEN)):
            self.sinalizaErroSintatico("Esperado \"then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         if(not self.eat(Tag.SMB_AB_CHA)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FE_CHA)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.CmdLinha()
      # Cmd -> id = F Cmd
      elif(self.eat(Tag.ID)):
        if(not self.eat(Tag.OP_ATRIB)):
            self.sinalizaErroSintatico("Esperado \"=\", encontrado " + "\"" + self.token.getLexema() + "\"")
       
        noF = self.F()
        if noF.tipo == Tag.TIPO_INT or noF.tipo == Tag.TIPO_DOUBLE:
          self.lexer.ts.removeToken(tempToken.getLexema())
          tempToken.setTipo(noF.tipo)
          self.lexer.ts.addToken(tempToken.getLexema(), tempToken)
        elif noF.tipo == Tag.TIPO_VAZIO:    
          self.sinalizaErroSemantico("Variavel usada antes de atribuicao.")
        else:
          self.sinalizaErroSemantico("Expressao mal formada na atribuicao.")

        self.Cmd()
      # Cmd -> print T
      elif(self.eat(Tag.KW_PRINT)):
        noT = self.T()
        if(noT.tipo == Tag.TIPO_VAZIO):
          self.sinalizaErroSemantico("Variavel usada antes de atribuicao.")
      else:
         self.skip("Esperado \"if, print, id\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

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
         sys.exit(0)

   # E -> F E'
   def E(self):
      noE = No()
      if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INT or self.token.getNome() == Tag.DOUBLE):
        noF = self.F()
        noELinha = self.ELinha()

        if noELinha.tipo == Tag.TIPO_VAZIO:
          noE.tipo = noF.tipo
        elif noELinha.tipo == noF.tipo and (noF.tipo == Tag.TIPO_INT or noF.tipo == Tag.TIPO_DOUBLE):
          noE.tipo = Tag.TIPO_LOGICO
        else:
          noE.tipo = Tag.TIPO_ERRO
        return noE
      else:
         self.sinalizaErroSintatico("Esperado \"id, int, double\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   '''
   E' --> ">" F E'  | "<" F E' | 
          ">=" F E' | "<=" F E'| 
          "==" F E' | "!=" F E'| epsilon
   '''
   def ELinha(self):
      noELinhaPai = No()

      if(self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MAIOR_IGUAL) or 
         self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE)):
        noF = self.F()
        noELinhaFilho = self.ELinha()

        if noELinhaFilho.tipo == Tag.TIPO_VAZIO and (noF.tipo == Tag.TIPO_INT or noF.tipo == Tag.TIPO_DOUBLE):
          noELinhaPai.tipo = noF.tipo
        elif noELinhaFilho.tipo == noF.tipo and (noF.tipo == Tag.TIPO_INT or noF.tipo == Tag.TIPO_DOUBLE):
          noELinhaPai.tipo = noF.tipo
        else:
          noELinhaPai.tipo = Tag.TIPO_ERRO
        return noELinhaPai
      elif(self.token.getNome() == Tag.KW_THEN):
         return noELinhaPai
      else:
         self.skip("Esperado \">, <, >=, <=, ==, !=, then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   def F(self):
      noF = No()
      if(self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INT or self.token.getNome() == Tag.DOUBLE):
        noT = self.T()
        noFLinha = self.FLinha()

        if noFLinha.tipo == Tag.TIPO_VAZIO:
          noF.tipo = noT.tipo
        elif noFLinha.tipo == noT.tipo and (noT.tipo == Tag.TIPO_INT or noT.tipo == Tag.TIPO_DOUBLE):
          noF.tipo = noT.tipo
        else:
          noF.tipo = Tag.TIPO_ERRO
        return noF
      else:
         self.skip("Esperado \"id, int, double\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   # F'  --> "+" T F' | "-" T F' | epsilon
   def FLinha(self):
      noFLinhaPai = No()
      if(self.eat(Tag.OP_SOMA) or self.eat(Tag.OP_SUB)):
        noT = self.T()
        noFLinhaFilho = self.FLinha()

        if noFLinhaFilho.tipo == Tag.TIPO_VAZIO and (noT.tipo == Tag.TIPO_INT or noT.tipo == Tag.TIPO_DOUBLE):
          noFLinhaPai.tipo = noT.tipo
        elif noFLinhaFilho.tipo == noT.tipo and (noT.tipo == Tag.TIPO_INT or noT.tipo == Tag.TIPO_DOUBLE):
          noFLinhaPai.tipo = noT.tipo
        else:
          noFLinhaPai.tipo = Tag.TIPO_ERRO
        return noFLinhaPai
      elif(self.token.getNome() == Tag.OP_MAIOR or self.token.getNome() == Tag.OP_MENOR or
           self.token.getNome() == Tag.OP_MAIOR_IGUAL or self.token.getNome() == Tag.OP_MENOR_IGUAL or
           self.token.getNome() == Tag.OP_DIFERENTE or self.token.getNome() == Tag.OP_IGUAL or
           self.token.getNome() == Tag.KW_THEN or self.token.getNome() == Tag.KW_IF or
           self.token.getNome() == Tag.KW_PRINT or self.token.getNome() == Tag.ID):
        return noFLinhaPai
      else:
         self.skip("Esperado \"+, -, >, <, >=, <=, ==, !=, then, if, print, id\", encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   # T -> id | num
   def T(self):
      noT = No()
      tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da primeira regra)

      if(self.eat(Tag.ID)):
        if tempToken.getTipo() == Tag.TIPO_VAZIO:
          self.sinalizaErroSemantico("Variavel " + "\"" + tempToken.getLexema() + "\"" + " nao definida.")
          noT.tipo = Tag.TIPO_ERRO
        else:
          noT.tipo = tempToken.getTipo()
      elif(self.eat(Tag.INT)):
        noT.tipo = Tag.TIPO_INT
      elif(self.eat(Tag.DOUBLE)):
        noT.tipo = Tag.TIPO_DOUBLE
      else:
        self.skip("Esperado \"int, double, id\", encontrado "  + "\"" + self.token.getLexema() + "\"");
        sys.exit(0)

      return noT
