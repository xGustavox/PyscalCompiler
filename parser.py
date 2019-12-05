import sys

from ts import TS
from tag import Tag
from ts_token import Token
from lexer import Lexer
from colorama import Fore, Back, Style

class Parser():

	def __init__(self, lexer):
		self.lexer = lexer
		self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo
		self.numErros = 0

	def sinalizaErroSintatico(self, tokenEsperado, recuperacao):
		if (self.numErros < 5):
			self.numErros += 1
			print((Fore.YELLOW + '[skiped]' if recuperacao == 'skip' else Fore.LIGHTGREEN_EX + '[synced]') + Fore.LIGHTRED_EX + '[Erro Sintatico]: ' + 'Esperado ' + tokenEsperado + ', Encontrado ' + self.token.getLexema() +  ' ' + '(Ln ' + str(self.token.getLinha()) + ', Col ' + str(self.token.getColuna()) + ')\n')
		else:
			print('Abortando compilação. Número de erros excedido')
			sys.exit(0)

	def advance(self):
		self.token = self.lexer.proxToken()

	def skip(self, tokenEsperado, metodoManterPilha):
		self.sinalizaErroSintatico(tokenEsperado, 'skip')
		self.advance()
		if (self.token.getNome() != Tag.EOF): metodoManterPilha()

	def sync(self, tokenEsperado):
		self.sinalizaErroSintatico(tokenEsperado, 'sync')

	def eat(self, t):
		if (self.token.getNome() == t):
			self.advance()
			return True
		else:
			return False

	#=============================
	# Regras
	#=============================

	def Programa(self):
		self.Classe()

		if (self.token.getNome() != Tag.EOF):
			self.sinalizaErroSintatico('EOF', '')

	def Classe(self):
		if (self.eat(Tag.KW_CLASS)): 
			if (not self.eat(Tag.ID)): self.sinalizaErroSintatico('ID', '')

			if (not self.eat(Tag.SP_COLONS)): self.sinalizaErroSintatico(':', '')
			self.ListaFuncao()
			self.Main()
			if (not self.eat(Tag.KW_END)): self.sinalizaErroSintatico('end', '')
			if (not self.eat(Tag.SP_DOT)): self.sinalizaErroSintatico('.', '')
		else:
			if (self.token.getNome() == Tag.EOF):
				self.sync('class')
				return
			else:
				self.skip('class', self.Classe)
			
	def ListaFuncao(self):
		if (self.token.getNome() == Tag.KW_DEF):
			self.ListaFuncaoLinha()
		else:
			if (self.token.getNome() == Tag.KW_DEFSTATIC):
				self.sync('def')
				return
			else:
				self.skip('def', self.ListaFuncao)

	def Main(self):
		if (self.eat(Tag.KW_DEFSTATIC)): 
			if (not self.eat(Tag.KW_VOID)): self.sinalizaErroSintatico('void', '')
			if (not self.eat(Tag.KW_MAIN)): self.sinalizaErroSintatico('main', '')
			if (not self.eat(Tag.SP_OPEN_BRAKETS)): self.sinalizaErroSintatico('(', '')
			if (not self.eat(Tag.KW_STRING)): self.sinalizaErroSintatico('String', '')
			if (not self.eat(Tag.SP_OPEN_SQUARE_BRACKET)): self.sinalizaErroSintatico('[', '')
			if (not self.eat(Tag.SP_CLOSE_SQUARE_BRACKET)): self.sinalizaErroSintatico(']', '')
			if (not self.eat(Tag.ID)): self.sinalizaErroSintatico('ID', '')
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
			if (not self.eat(Tag.SP_COLONS)): self.sinalizaErroSintatico(':', '')
			self.RegexDeclaraId()
			self.ListaCmd()
			if (not self.eat(Tag.KW_END)): self.sinalizaErroSintatico('end', '')
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		elif (self.token.getNome() == Tag.KW_END):
			self.sync('defstatic')
			return
		else:
			self.skip('defstatic', self.Main())
		
	def ListaFuncaoLinha(self):
		if (self.token.getNome() == Tag.KW_DEF):
			self.Funcao()
			self.ListaFuncaoLinha()
		else:
			if (self.token.getNome() == Tag.KW_DEFSTATIC):
				return
			else:
				self.skip('def', self.ListaFuncaoLinha)

	def Funcao(self):
		if (self.eat(Tag.KW_DEF)):
			self.TipoPrimitivo()
			if (not self.eat(Tag.ID)): self.sinalizaErroSintatico('ID', '')
			if (not self.eat(Tag.SP_OPEN_BRAKETS)): self.sinalizaErroSintatico('(', '')
			self.ListaAgr()
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
			if (not self.eat(Tag.SP_COLONS)): self.sinalizaErroSintatico(':', '')
			self.RegexDeclaraId()
			self.ListaCmd()
			self.Retorno()
			if (not self.eat(Tag.KW_END)): self.sinalizaErroSintatico('end', '')
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.KW_DEFSTATIC):
				self.sync('defstatic')
				return
			else:
				self.skip('def, defstatic', self.Funcao)

	def RegexDeclaraId(self):
		if (self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID):
			self.DeclaraId()
			self.RegexDeclaraId()
		else:
			if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or  self.token.getNome() == Tag.KW_RETURN or  self.token.getNome() == Tag.KW_IF or  self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE):
				return
			else:
				self.skip('bool, integer, string, double, void', self.RegexDeclaraId)
			

	def DeclaraId(self):
		if (self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID):
			self.TipoPrimitivo()
			if (not self.eat(Tag.ID)): self.sinalizaErroSintatico('ID', '')
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE):
				self.sync('bool, integer, string, double, void')
				return
			else:
				self.skip('bool, integer, string, double, void', self.DeclaraId)

	def TipoPrimitivo(self):
		if (not self.eat(Tag.KW_BOOL) and not self.eat(Tag.KW_INTEGER) and not self.eat(Tag.KW_STRING) and not self.eat(Tag.KW_DOUBLE) and not self.eat(Tag.KW_VOID)):
			if (self.token.getNome() == Tag.ID):
				self.sync('bool, integer, String, double, void')
				return
			else:
				self.skip('bool, integer, String, double, void', self.TipoPrimitivo)

	def ListaAgr(self):
		if (self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID):
			self.Arg()
			self.ListaArgLinha()
		else:
			if (self.token.getNome() == Tag.SP_CLOSE_BRAKETS):
				self.sync('boo, integer, string, double, void')
				return
			else:
				self.skip('boo, integer, string, double, void', self.ListaAgr)

	def Arg(self):
		if (self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID):
			self.TipoPrimitivo()
			if (not self.eat(Tag.ID)): self.sinalizaErroSintatico('ID', '')
		else:
			if (self.token.getNome() == Tag.SP_COMMA or self.token.getNome() == Tag.SP_CLOSE_BRAKETS):
				self.sync('boo, integer, string, double, void')
				return
			else:
				self.skip('boo, integer, string, double, void', self.Arg)

	def ListaArgLinha(self):
		if (self.eat(Tag.SP_COMMA)):
			self.ListaAgr()
		else:
			if (self.token.getNome() == Tag.SP_CLOSE_BRAKETS):
				return
			else:
				self.skip(',', self.ListaArgLinha)

	def ListaCmd(self):
		if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE):
			self.ListaCmdLinha()
		else:
			self.skip('if, while, ID, write', self.ListaCmdLinha)

	def ListaCmdLinha(self):
		if (self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE):
			self.Cmd()
			self.ListaCmdLinha()
		else:
			if (self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				return
			else:
				self.skip('if, while, ID, write', self.ListaCmdLinha)

	def Cmd(self):
		if (self.token.getNome() == Tag.KW_IF):
			self.CmdIf()
		elif (self.token.getNome() == Tag.KW_WHILE):
			self.CmdWhile()
		elif (self.token.getNome() == Tag.KW_WRITE):
			self.CmdWrite()
		elif (self.eat(Tag.ID)):
			self.CmdAtribuiFunc()
		else:
			if (self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				self.sync('if, while, ID, write')
				return
			else:
				self.skip('if, while, ID, write', self.Cmd)
			
	def CmdIf(self):
		if (self.eat(Tag.KW_IF)):
			if (not self.eat(Tag.SP_OPEN_BRAKETS)): self.sinalizaErroSintatico('(', '')
			self.Expressao()
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
			if (not self.eat(Tag.SP_COLONS)): self.sinalizaErroSintatico(':', '')
			self.ListaCmd()
			self.CmdIfLinha()
		else:
			if (self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				self.sync('if')
				return
			else:
				self.skip('if', self.CmdIf)

	def CmdIfLinha(self):
		if (self.eat(Tag.KW_END)):
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		elif (self.eat(Tag.KW_ELSE)):
			if (not self.eat(Tag.SP_COLONS)): self.sinalizaErroSintatico(':', '')
			self.ListaCmd()
			if (not self.eat(Tag.KW_END)): self.sinalizaErroSintatico('end', '')
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_RETURN  or self.token.getNome() == Tag.KW_IF  or self.token.getNome() == Tag.KW_WHILE  or self.token.getNome() == Tag.KW_WRITE):
				self.sync('end, else')
				return
			else:
				self.skip('end, else', self.CmdIfLinha)

	def CmdWhile(self):
		if (self.eat(Tag.KW_WHILE)):
			if (not self.eat(Tag.SP_OPEN_BRAKETS)): self.sinalizaErroSintatico('(', '')
			self.Expressao()
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
			if (not self.eat(Tag.SP_COLONS)): self.sinalizaErroSintatico(':', '')
			self.ListaCmd()
			if (not self.eat(Tag.KW_END)): self.sinalizaErroSintatico('end', '')
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				self.sync('while')
				return
			else:
				self.skip('while', self.CmdWhile)

	def CmdWrite(self):
		if (self.eat(Tag.KW_WRITE)):
			if (not self.eat(Tag.SP_OPEN_BRAKETS)): self.sinalizaErroSintatico('(', '')
			self.Expressao()
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				self.sync('write')
				return
			else:
				self.skip('write', self.CmdWrite)

	def CmdAtribuiFunc(self):
		if (self.token.getNome() == Tag.OP_ATTRIBUTION):
			self.CmdAtribui()
		elif (self.token.getNome() == Tag.SP_OPEN_BRAKETS):
			self.CmdFuncao()
		else:
			if (self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				self.sync('=, (')
				return
			else:
				self.skip('=, (', self.CmdAtribuiFunc)

	def CmdAtribui(self):
		if (self.eat(Tag.OP_ATTRIBUTION)):
			self.Expressao()
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or 
				self.token.getNome() == Tag.KW_WRITE or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				self.sync('=')
				return
			else:
				self.skip('=', self.CmdAtribui)

	def CmdFuncao(self):
		if (self.eat(Tag.SP_OPEN_BRAKETS)):
			self.RegexExp()
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE or 
				self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_ELSE):
				self.sync('(')
				return
			else:
				self.skip('(', self.CmdFuncao)

	def Retorno(self):
		if (self.eat(Tag.KW_RETURN)):
			self.Expressao()
			if (not self.eat(Tag.SP_SEMICOLON)): self.sinalizaErroSintatico(';', '')
		else:
			if (self.token.getNome() == Tag.KW_END):
				return
			else:
				self.skip('return', self.Retorno)

	def Expressao(self):
		# ID, ConstInteger, ConstDouble, ConstString, "true", "false", "-"(negação) , "!", "("
		if (self.token.getNome() == Tag.ID or 
			self.token.getNome() == Tag.CONST_INTEGER or 
			self.token.getNome() == Tag.CONST_DOUBLE or 
			self.token.getNome() == Tag.CONST_STRING or 
			self.token.getNome() == Tag.KW_TRUE or 
			self.token.getNome() == Tag.KW_FALSE or 
			self.token.getNome() == Tag.OP_NEGATIVE or 
			self.token.getNome() == Tag.OP_EXCLAMATION_MARK or 
			self.token.getNome() == Tag.SP_OPEN_BRAKETS):
			self.Exp1()
			self.ExpLinha()
		else:
			if (self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				self.sync('ID, ConstInteger, ConstDouble, ConstString, true, false, -, !, (')
				return
			else:
				self.skip('ID, ConstInteger, ConstDouble, ConstString, true, false, -, !, (', self.Expressao)

	def Exp1(self):
		# ID, ConstInteger, ConstDouble, ConstString, "true","false", "-"(negação) , "!", "("
		if (self.token.getNome() == Tag.ID or 
			self.token.getNome() == Tag.SP_OPEN_BRAKETS or
			self.token.getNome() == Tag.CONST_INTEGER or 
			self.token.getNome() == Tag.CONST_DOUBLE or 
			self.token.getNome() == Tag.CONST_STRING or 
			self.token.getNome() == Tag.KW_TRUE or 
			self.token.getNome() == Tag.KW_FALSE or 
			self.token.getNome() == Tag.OP_NEGATIVE or 
			self.token.getNome() == Tag.OP_EXCLAMATION_MARK):
			self.Exp2()
			self.Exp1Linha()
		else:
			# "or", "and", ")", ";", ","
			if (self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				self.sync('ID, ConstInteger, ConstDouble, ConstString, true, false, -, !, (')
				return
			else:
				self.skip('ID, ConstInteger, ConstDouble, ConstString, true, false, -, !, (', self.Expressao)

	def ExpLinha(self):
		if (self.eat(Tag.KW_OR) or self.eat(Tag.KW_AND)):
			self.Exp1()
			self.ExpLinha()
		else:
			# ")", ";", ","
			if (self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				return
			else:
				self.skip('or, and', self.ExpLinha)

	def Exp2(self):
		if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.CONST_INTEGER or self.token.getNome() == Tag.CONST_DOUBLE or self.token.getNome() == Tag.CONST_STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATIVE or self.token.getNome() == Tag.OP_EXCLAMATION_MARK or self.token.getNome() == Tag.SP_OPEN_BRAKETS):
			self.Exp3()
			self.Exp2Linha()
		else:
			if (self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFERENT or self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				self.sync('ID, ConstInteger, ConstDouble, ConstString, true, false, - , !, (')
				return
			else:
				self.skip('ID, ConstInteger, ConstDouble, ConstString, true, false, - , !, (', self.Exp2)

	def Exp3(self):
		if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.CONST_INTEGER or self.token.getNome() == Tag.CONST_DOUBLE or self.token.getNome() == Tag.CONST_STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATIVE or self.token.getNome() == Tag.OP_EXCLAMATION_MARK or self.token.getNome() == Tag.SP_OPEN_BRAKETS):
			self.Exp4()
			self.Exp3Linha()
		else:
			if (self.token.getNome() == Tag.OP_PLUS or self.token.getNome() == Tag.OP_MINUS or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFERENT or self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				self.sync('ID, ConstInteger, ConstDouble, ConstString, true, false, - , !, (')
				return
			else:
				self.skip('ID, ConstInteger, ConstDouble, ConstString, true, false, - , !, (', self.Exp3)

	def Exp4(self):
		if (self.eat(Tag.ID)):
			self.Exp4Linha()
		elif (self.eat(Tag.SP_OPEN_BRAKETS)):
			self.Expressao()
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
		elif (self.token.getNome() == Tag.OP_NEGATIVE or self.token.getNome() == Tag.OP_EXCLAMATION_MARK):
			self.OpUnario()
			self.Exp4()
		elif (not self.eat(Tag.CONST_INTEGER) and not self.eat(Tag.CONST_DOUBLE) and not self.eat(Tag.CONST_STRING) and not self.eat(Tag.KW_TRUE) and not self.eat(Tag.KW_FALSE)):
			if (self.token.getNome() == Tag.OP_TIMES or self.token.getNome() == Tag.OP_SLASH or self.token.getNome() == Tag.OP_PLUS or self.token.getNome() == Tag.OP_MINUS or 
				self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or 
				self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFERENT or self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or 
				self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				self.sync('ID, ConstInteger, ConstDouble, ConstString, true, false, - , !, (')
				return
			else:
				self.skip('ID, ConstInteger, ConstDouble, ConstString, true, false, - , !, (', self.Exp4)

	def Exp1Linha(self):
		if (self.eat(Tag.OP_LESS) or self.eat(Tag.OP_LESS_EQUAL) or self.eat(Tag.OP_GREATER) or self.eat(Tag.OP_GREATER_EQUAL) or self.eat(Tag.OP_LESS) or self.eat(Tag.OP_EQUAL) or self.eat(Tag.OP_DIFERENT)):
			self.Exp2()
			self.Exp1Linha()
		else:
			if (self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				return
			else:
				self.skip('<, <=, >, >=, ==, !=', self.Exp1Linha)

	def Exp2Linha(self):
		# "+", "-", “ε”
		if (self.eat(Tag.OP_PLUS) or self.eat(Tag.OP_MINUS)):
			self.Exp3()
			self.Exp2Linha()
		else:
			if (self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFERENT or self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				return
			else:
				self.skip('+, -', self.Exp2Linha)

	def Exp3Linha(self):
		# "*", "/", “ε”
		if (self.eat(Tag.OP_TIMES) or self.eat(Tag.OP_SLASH)):
			self.Exp4()
			self.Exp3Linha()
		else:
			if (self.token.getNome() == Tag.OP_PLUS or self.token.getNome() == Tag.OP_MINUS or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFERENT or self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				return
			else:
				self.skip('*, /', self.Exp3Linha)

	def Exp4Linha(self):
		if (self.eat(Tag.SP_OPEN_BRAKETS)):
			self.RegexExp()
			if (not self.eat(Tag.SP_CLOSE_BRAKETS)): self.sinalizaErroSintatico(')', '')
		else:
			if (self.token.getNome() == Tag.OP_TIMES or self.token.getNome() == Tag.OP_SLASH or self.token.getNome() == Tag.OP_PLUS or self.token.getNome() == Tag.OP_MINUS or 
				self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or 
				self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFERENT or self.token.getNome() == Tag.KW_OR or self.token.getNome() == Tag.KW_AND or 
				self.token.getNome() == Tag.SP_CLOSE_BRAKETS or self.token.getNome() == Tag.SP_SEMICOLON or self.token.getNome() == Tag.SP_COMMA):
				return
			else:
				self.skip('(', self.Exp4Linha)

	def OpUnario(self):
		if (not self.eat(Tag.OP_NEGATIVE) and not self.eat(Tag.OP_EXCLAMATION_MARK)):
			# ID, ConstInteger, ConstDouble, ConstString, "true", "false", "-"(negação) , "!", "("
			if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.CONST_INTEGER or self.token.getNome() == Tag.CONST_DOUBLE or self.token.getNome() == Tag.CONST_STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATIVE or self.token.getNome() == Tag.OP_EXCLAMATION_MARK or self.token.getNome() == Tag.SP_OPEN_BRAKETS):
				self.sync('-, !')
				return
			else:
				self.skip('-, !', self.OpUnario)

	def RegexExp(self):
		if (self.token.getNome() == Tag.ID or self.token.getNome() == Tag.CONST_INTEGER or self.token.getNome() == Tag.CONST_DOUBLE or self.token.getNome() == Tag.CONST_STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATIVE or self.token.getNome() == Tag.OP_EXCLAMATION_MARK or self.token.getNome() == Tag.SP_OPEN_BRAKETS):
			self.Expressao()
			self.RegexExpLinha()
		else:
			if (self.token.getNome() == Tag.SP_CLOSE_BRAKETS):
				return
			else:
				self.skip('ID, ConstInteger, ConstDouble, ConstString, true, false, - , !, (', self.RegexExp)

	def RegexExpLinha(self):
		if (self.eat(Tag.SP_COMMA)):
			self.Expressao()
			self.RegexExpLinha()
		else:
			if (self.token.getNome() == Tag.SP_CLOSE_BRAKETS):
				return
			else:
				self.skip(',', self.RegexExpLinha)