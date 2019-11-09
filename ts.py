from tag import Tag
from ts_token import Token
from colorama import Fore, Back, Style

class TS:
   '''
   Classe para a tabela de simbolos representada por um dicionario: {'chave' : 'valor'}
   '''
   def __init__(self):
      self.ts = {}

      self.ts['class'] = Token(Tag.KW_CLASS, 'class', 0, 0)
      self.ts['end'] = Token(Tag.KW_END, 'end', 0, 0)
      self.ts['def'] = Token(Tag.KW_DEF, 'def', 0, 0)
      self.ts['return'] = Token(Tag.KW_RETURN, 'return', 0, 0)
      self.ts['defstatic'] = Token(Tag.KW_DEFSTATIC, 'defstatic', 0, 0)
      self.ts['void'] = Token(Tag.KW_VOID, 'void', 0, 0)
      self.ts['main'] = Token(Tag.KW_MAIN, 'main', 0, 0)
      self.ts['String'] = Token(Tag.KW_STRING, 'String', 0, 0)
      self.ts['bool'] = Token(Tag.KW_BOOL, 'bool', 0, 0)
      self.ts['integer'] = Token(Tag.KW_INTEGER, 'integer', 0, 0)
      self.ts['double'] = Token(Tag.KW_DOUBLE, 'double', 0, 0)
      self.ts['if'] = Token(Tag.KW_IF, 'if', 0, 0)
      self.ts['else'] = Token(Tag.KW_ELSE, 'else', 0, 0)
      self.ts['while'] = Token(Tag.KW_WHILE, 'while', 0, 0)
      self.ts['write'] = Token(Tag.KW_WRITE, 'write', 0, 0)
      self.ts['true'] = Token(Tag.KW_TRUE, 'true', 0, 0)
      self.ts['false'] = Token(Tag.KW_FALSE, 'false', 0, 0)
      self.ts['or'] = Token(Tag.KW_OR, 'or', 0, 0)
      self.ts['and'] = Token(Tag.KW_AND, 'and', 0, 0)
      
      self.ts['='] = Token(Tag.OP_ATTRIBUTION, '=', 0, 0)
      self.ts['=='] = Token(Tag.OP_EQUAL, '==', 0, 0)
      self.ts['<'] = Token(Tag.OP_LESS, '<', 0, 0)
      self.ts['<='] = Token(Tag.OP_LESS_EQUAL, '<=', 0, 0)
      self.ts['>'] = Token(Tag.OP_GREATER, '>', 0, 0)
      self.ts['>='] = Token(Tag.OP_GREATER_EQUAL, '>=', 0, 0)
      self.ts['!'] = Token(Tag.OP_EXCLAMATION_MARK, '!', 0, 0)
      self.ts['!='] = Token(Tag.OP_DIFERENT, '!=', 0, 0)
      self.ts['/'] = Token(Tag.OP_SLASH, '/', 0, 0)
      self.ts['*'] = Token(Tag.OP_TIMES, '*', 0, 0)
      self.ts['-'] = Token(Tag.OP_MINUS, '-', 0, 0)
      self.ts['+'] = Token(Tag.OP_PLUS, '+', 0, 0)
      
      self.ts[':'] = Token(Tag.SP_COLONS, ':', 0, 0)
      self.ts['.'] = Token(Tag.SP_DOT, '.', 0, 0)
      self.ts[';'] = Token(Tag.SP_SEMICOLON, ';', 0, 0)
      self.ts['('] = Token(Tag.SP_OPEN_BRAKETS, '(', 0, 0)
      self.ts[')'] = Token(Tag.SP_CLOSE_BRAKETS, ')', 0, 0)
      self.ts[','] = Token(Tag.SP_COMMA, ',', 0, 0)
      self.ts['['] = Token(Tag.SP_OPEN_SQUARE_BRACKET, '[', 0, 0)
      self.ts[']'] = Token(Tag.SP_CLOSE_SQUARE_BRACKET, ']', 0, 0)
      
   def getToken(self, lexema):
      token = self.ts.get(lexema)
      return token

   def addToken(self, lexema, token):
      self.ts[lexema] = token

   def printTS(self):
      for key, token in (self.ts.items()):
         print(Fore.GREEN + key, Fore.WHITE + "->", token.toString())
