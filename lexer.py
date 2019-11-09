import sys

from ts import TS
from tag import Tag
from ts_token import Token
from colorama import Fore, Back, Style

class Lexer():
   def __init__(self, input_file):
      try:
         self.input_file = open(input_file, 'rb')
         self.lookahead = 0
         self.lookbehind = 0
         self.n_line = 1
         self.n_column = 1
         self.n_erros = 0
         self.modoPanico = False # Indica se o modo pânico está ativo
         self.last_token = None # Armazena o ultimo token retornado
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

   def sinalizaErroLexico(self, message, line = None, coluna = None):
      if (not self.modoPanico):
         self.n_erros += 1
         
         print(Fore.LIGHTRED_EX + '[Erro Lexico]: ', message, 
            '(Ln ' + str(line) + ', Col ' + str(coluna) + ')' if (line and coluna is not None) else '');

         self.modoPanico = True

   # Retorna uma posição no ponteiro e decrementa uma coluna
   def retornaPonteiro(self):
      if (self.lookahead.decode('ascii') != ''):
         self.n_column -= 1
         self.input_file.seek(self.input_file.tell() - 1)

   def printTS(self):
      self.ts.printTS()

   # Adiciona 1 na coluna enquanto não houver quebra de linha
   # Se encontrar quebra de linha, reseta coluna e incrementa linha
   def atualizaLinhaColuna(self, c):

      if (c == '\n'):
         self.n_line += 1
         self.n_column = 1
      else:
         self.n_column += 1

   # Retorna um Token() ou -1
   def proxToken(self):
      estado = 1
      lexema = ''
      c = '\u0000'

      # Utilizado para caracteres inválidos no estado 1
      lexemaError = ''
      ln_erro = 1
      col_erro = 1

      # Armazena a ultima linha e coluna antes da quebra de linha
      last_line = 1
      last_column = 1

      # Token que será retornado
      tok = None

      while(True):

         # Caso seja encontrado 5 erros o lexer para a compilação
         if (self.n_erros == 5):
            return -1

         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')

         # Salva a linha e coluna antes de atualizar a linha e coluna
         last_line = self.n_line
         last_column = self.n_column

         self.atualizaLinhaColuna(c)

         if (estado == 1):
            if (c == ''):
               tok = Token(Tag.EOF, 'EOF', self.n_line, self.n_column)
            elif (c == ' ' or c == '\t' or c == '\n' or c == '\r'):
               estado = 1

               # Caso não exista caminhos a seguir
               if (len(lexemaError) > 0):
                  self.sinalizaErroLexico('Cadeia de caracteres "' + lexemaError + '" inválida!', ln_erro, col_erro)
                  lexemaError = ''
                  self.modoPanico = False

            elif (c.isalpha()):
               lexema += c
               estado = 2
            elif (c.isdigit()):
               lexema += c
               estado = 23
            elif (c == '"'):
               lexema += '"'
               estado = 4
            elif (c == '='):
               estado = 7
            elif (c == '<'):
               estado = 10
            elif (c == '>'):
               estado = 13
            elif (c == '!'):
               estado = 16
            elif (c == '+'):
               tok = Token(Tag.OP_PLUS, '+', self.n_line, self.n_column)
            elif (c == '-'):
               # Se o ultimo token retornado for número ou variavel considera o operador como subtração
               if (self.last_token.value == 44 or self.last_token.value == 45 or self.last_token.value == 41):
                  tok = Token(Tag.OP_MINUS, '-', self.n_line, self.n_column)
               else:
                  tok = Token(Tag.OP_NEGATIVE, '-', self.n_line, self.n_column)
            elif (c == '/'):
               tok = Token(Tag.OP_SLASH, '/', self.n_line, self.n_column)
            elif (c == '*'):
               tok = Token(Tag.OP_TIMES, '*', self.n_line, self.n_column)
            elif (c == ':'):
               tok = Token(Tag.SP_COLONS, ':', self.n_line, self.n_column)
            elif (c == '.'):
               tok = Token(Tag.SP_DOT, '.', self.n_line, self.n_column)
            elif (c == ';'):
               tok = Token(Tag.SP_SEMICOLON, ';', self.n_line, self.n_column)
            elif (c == '('):
               tok = Token(Tag.SP_OPEN_BRAKETS, '(', self.n_line, self.n_column)
            elif (c == ')'):
               tok = Token(Tag.SP_CLOSE_BRAKETS, ')', self.n_line, self.n_column)
            elif (c == '['):
               tok = Token(Tag.SP_OPEN_SQUARE_BRACKET, '[', self.n_line, self.n_column)
            elif (c == ']'):
               tok = Token(Tag.SP_CLOSE_SQUARE_BRACKET, ']', self.n_line, self.n_column)
            elif (c == ','):
               tok = Token(Tag.SP_COMMA, ',', self.n_line, self.n_column)
            elif (c == '#'):
               estado = 36
            else:
               # Concatena todos os caracteres inesperados no estado 1 salvando linha e coluna
               lexemaError += c
               ln_erro = self.n_line
               col_erro = self.n_column - len(lexemaError)
         elif (estado == 7):
            if (c == '='):
               tok = Token(Tag.OP_EQUAL, '==', self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               tok = Token(Tag.OP_ATTRIBUTION, '=', self.n_line, self.n_column)
         elif (estado == 10):
            if (c == '='):
               tok = Token(Tag.OP_LESS_EQUAL, '<=', self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               tok = Token(Tag.OP_LESS, '<', self.n_line, self.n_column)
         elif (estado == 13):
            if (c == '='):
               tok = Token(Tag.OP_GREATER_EQUAL, '>=', self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               tok = Token(Tag.OP_GREATER, '>', self.n_line, self.n_column)
         elif (estado == 16):
            if (c == '='):
               tok = Token(Tag.OP_DIFERENT, '!=', self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               tok = Token(Tag.OP_EXCLAMATION_MARK, '!', self.n_line, self.n_column)
         elif (estado == 2):
            if (c.isalpha() or c.isdigit() or c == '_'):
               lexema += c
            else:
               token = self.ts.getToken(lexema) # Verifica se o token já está na TS
               self.retornaPonteiro()

               # Se token não existir na TS
               if (token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)
               else:
                  token = Token(token.getNome(), token.getLexema(), self.n_line, self.n_column)

               tok = token
         elif (estado == 4):
            if (c == '"'): # Caso a string tenha apenas "" sinaliza o erro e continua a execução
               self.sinalizaErroLexico('A String não pode estar vazia.', self.n_line, self.n_column)
               estado = 1
               tok = None
            elif (c.isascii()):
               lexema += c 
               estado = 5
               self.modoPanico = False
            else:
               self.sinalizaErroLexico('Caracter não pertence à tabela ASCII ' + lexema, self.n_line, self.n_column)
         elif (estado == 5):
            if (c == '"'): # Fecha a string
               lexema += '"'
               tok = Token(Tag.CONST_STRING, lexema, self.n_line, self.n_column)
               self.modoPanico = False
            elif (c.isascii() and c != '\n' and c != ''): # Adiciona caracteres na string
               lexema += c
            else: # Erro de string
               if (c == ''):
                  self.modoPanico = False
                  self.sinalizaErroLexico('A string \'' + lexema + '\' não foi fechada antes do fim do arquivo.', self.n_line, self.n_column)
                  tok = -1 # Retorno de EOF
               elif (c == '\n'):
                  self.sinalizaErroLexico('A string \'' + lexema + '\' não foi fechada antes da quebra de linha.', last_line, last_column)
               elif (not c.isascii()):
                  self.sinalizaErroLexico('Caracter não pertence à tabela ASCII ' + lexema,  self.n_line, self.n_column)
         elif (estado == 23):
            if (c.isdigit()):
               lexema += c
            elif (c == '.'):
               lexema += c
               estado = 25
            else:
               self.retornaPonteiro()
               tok = Token(Tag.CONST_INTEGER, lexema, self.n_line, self.n_column)
         elif (estado == 25):
            if (c.isdigit()):
               lexema += c
               estado = 26
            else:
               self.sinalizaErroLexico('Caracter inesperado próximo à \'' + lexema + '\'! Digito esperado.', last_line, last_column)
         elif (estado == 26):
            if (c.isdigit()):
               lexema += c
            else:
               self.retornaPonteiro()
               tok = Token(Tag.CONST_DOUBLE, lexema, last_line, last_column)
         elif (estado == 36):
            if (c == '\n'):
               estado = 1
               tok = None
         # fim if's

         if (tok is not None):
            if (tok != -1):
               self.last_token = tok.getNome()

            return tok
      # fim while

