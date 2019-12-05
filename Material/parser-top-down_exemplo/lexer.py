import sys

from ts import TS
from tag import Tag
from token import Token

class Lexer():
   '''
   Classe que representa o Lexer:
   
   [1] Voce devera se preocupar quando incremetar as linhas e colunas,
   assim como quando decrementar ou reinicia-las. Lembre-se, ambas 
   comecam em 1.
   [2] Toda vez que voce encontrar um lexema completo, voce deve retornar
   um objeto Token(Tag, "lexema", linha, coluna). Cuidado com as
   palavras reservadas, que ja sao cadastradas na TS. Essa consulta
   voce devera fazer somente quando encontrar um Identificador.
   [3] Se o caractere lido nao casar com nenhum caractere esperado,
   apresentar a mensagem de erro na linha e coluna correspondente.
   Obs.: lembre-se de usar o metodo retornaPonteiro() quando necessario. 
         lembre-se de usar o metodo sinalizaErroLexico() para mostrar
         a ocorrencia de um erro lexico.
   '''
   def __init__(self, input_file):
      try:
         self.input_file = open(input_file, 'rb')
         self.lookahead = 0
         self.n_line = 1
         self.n_column = 1
         self.ts = TS()
      except IOError:
         print('Erro de abertura do arquivo. Encerrando.')
         sys.exit(0)

   def closeFile(self):
      try:
         self.input_file.close()
      except IOError:
         print('Erro dao fechar arquivo. Encerrando.')
         sys.exit(0)

   def sinalizaErroLexico(self, message):
      print("[Erro Lexico]: ", message, "\n");

   def retornaPonteiro(self):
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()-1)

   def printTS(self):
      self.ts.printTS()

   def proxToken(self):
      estado = 1
      lexema = ""
      c = '\u0000'

      while(True):
         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')

         if(estado == 1):
            if(c == ''):
               return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif(c == ' ' or c == '\t' or c == '\n' or c == '\r'):
               estado = 1
            elif(c == '='):
               estado = 2
            elif(c == '!'):
               estado = 4
            elif(c == '<'):
               estado = 6
            elif(c == '>'):
               estado = 9
            elif(c.isdigit()):
               lexema += c
               estado = 12
            elif(c.isalpha()):
               lexema += c
               estado = 14
            elif(c == '/'):
               estado = 16
            elif(c == '+'):
               return Token(Tag.OP_SOMA, "+", self.n_line, self.n_column)
            elif(c == '-'):
               return Token(Tag.OP_SUB, "-", self.n_line, self.n_column)
            elif(c == '{'):
               return Token(Tag.SMB_AB_CHA, "{", self.n_line, self.n_column)
            elif(c == '}'):
               return Token(Tag.SMB_FE_CHA, "}", self.n_line, self.n_column)
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 2):
            if(c == '='):
               return Token(Tag.OP_IGUAL, "==", self.n_line, self.n_column)
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 4):
            if(c == '='):
               return Token(Tag.OP_DIFERENTE, "!=", self.n_line, self.n_column)
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 6):
            if(c == '='):
               return Token(Tag.OP_MENOR_IGUAL, "<=", self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               return Token(Tag.OP_MENOR, "<", self.n_line, self.n_column)
         elif(estado == 9):
            if(c == '='):
               return Token(Tag.OP_MAIOR_IGUAL, ">=", self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               return Token(Tag.OP_MAIOR, ">", self.n_line, self.n_column)
         elif(estado == 12):
            if(c.isdigit()):
               lexema += c           
            else:
               self.retornaPonteiro()
               return Token(Tag.NUM, lexema, self.n_line, self.n_column)
         elif(estado == 14):
            if(c.isalnum()):
               lexema += c
            else:
               self.retornaPonteiro()
               token = self.ts.getToken(lexema)
               if(token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)
               return token
         elif(estado == 16):
            if(c == '/'):
               estado = 17
            else:
               self.sinalizaErroLexico("Padrao invalido para comentario na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 17):
            if(c == '\n'):
               estado = 1 
         else:
            self.sinalizaErroLexico("Caractere desconhecido na linha " +
            str(self.n_line) + " e coluna " + str(self.n_column))
            return None
         # fim if's de estados
      # fim while
