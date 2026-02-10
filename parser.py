import ply.yacc as yacc
from lexico import tokens
from lexico import lexer
import sys


# =========================
# AST — CLASSES
# =========================


class Programa:
    def __init__(self, funcoes):
        self.funcoes = funcoes

    

class Funcao:
    def __init__(self, nome, parametros, bloco):
        self.nome = nome
        self.parametros = parametros
        self.bloco = bloco

    

class Bloco:
    def __init__(self, comandos):
        self.comandos = comandos

   


class Declaracao:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    


class Atribuicao:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

   


class If:
    def __init__(self, condicao, bloco_then, elifs, bloco_else):
        self.condicao = condicao
        self.bloco_then = bloco_then
        self.elifs = elifs          
        self.bloco_else = bloco_else


class ElseIf:
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

   


class For:
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

   


class Return:
    def __init__(self, valor):
        self.valor = valor

    


class BinOp:
    def __init__(self, esquerda, op, direita):
        self.esquerda = esquerda
        self.op = op
        self.direita = direita

    


class Not:
    def __init__(self, expr):
        self.expr = expr

    


class Identificador:
    def __init__(self, nome):
        self.nome = nome

    


class Literal:
    def __init__(self, valor):
        self.valor = valor

    


# =========================
# Precedência
# =========================

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),
)

# =========================
# Gramática
# =========================

def p_programa(p):
    'programa : lista_funcoes'
    p[0] = Programa(p[1])

def p_lista_funcoes(p):
    '''lista_funcoes : funcao lista_funcoes
                     | funcao'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_funcao(p):
    '''funcao : FN ID LPAREN param RPAREN bloco
              | FN ID LPAREN RPAREN bloco'''
    if len(p) == 6:
        p[0] = Funcao(p[2], [], p[5])
    else:
        p[0] = Funcao(p[2], p[4], p[6])

def p_param_simples(p):
    'param : ID'
    p[0] = [p[1]]

def p_param_varios(p):
    'param : ID COMMA param'
    p[0] = [p[1]] + p[3]




def p_bloco(p):
    'bloco : LBRACE lista_comandos RBRACE'
    p[0] = Bloco(p[2])

def p_lista_comandos(p):
    '''lista_comandos : comando lista_comandos
                      | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []



def p_comando(p):
    '''comando : declaracao SEMICOLON
                | atribuicao SEMICOLON
                | comando_if
                | comando_for
                | retorno SEMICOLON'''
    p[0] = p[1]

def p_declaracao(p):
    'declaracao : MUT ID DECLARE_ASSIGN expressao'
    p[0] = Declaracao(p[2], p[4])

def p_atribuicao(p):
    'atribuicao : ID ASSIGN expressao'
    p[0] = Atribuicao(p[1], p[3])

    
 #Tem que testar ai dps
def p_comando_if(p):
    '''comando_if : IF expressao bloco
                   | IF expressao bloco ELSE bloco
                   | IF expressao bloco elseIfList
                   | IF expressao bloco elseIfList ELSE bloco'''
    
    if len(p) == 4:
        p[0] = If(p[2], p[3], [], None)

    elif len(p) == 6 and p[4] == 'else':
        p[0] = If(p[2], p[3], [], p[5])

    elif len(p) == 5:
        p[0] = If(p[2], p[3], p[4], None)

    elif len(p) == 7:
        p[0] = If(p[2], p[3], p[4], p[6])


def p_elseIfList_simples(p):
    'elseIfList : ELSE IF expressao bloco'
    p[0] = [ElseIf(p[3], p[4])]


def p_elseIfList_varios(p):
    'elseIfList : ELSE IF expressao bloco elseIfList'
    p[0] = [ElseIf(p[3], p[4])] + p[5]



def p_comando_for(p):
    'comando_for : FOR expressao bloco'
    p[0] = For(p[2], p[3])

def p_retorno(p):
    '''retorno : RETURN
               | RETURN expressao'''
    if len(p) == 2:
        p[0] = Return(None)
    else:
        p[0] = Return(p[2])

def p_expressao_binaria(p):
    '''expressao : expressao PLUS expressao
                 | expressao MINUS expressao
                 | expressao TIMES expressao
                 | expressao DIVIDE expressao
                 | expressao EQ expressao
                 | expressao NEQ expressao
                 | expressao LT expressao
                 | expressao LE expressao
                 | expressao GT expressao
                 | expressao GE expressao
                 | expressao AND expressao
                 | expressao OR expressao'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expressao_not(p):
    'expressao : NOT expressao'
    p[0] = Not(p[2])

def p_expressao_group(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]

def p_expressao_id(p):
    'expressao : ID'
    p[0] = Identificador(p[1])

def p_expressao_literal(p):
    '''expressao : INT
                 | FLOAT
                 | TRUE
                 | FALSE
                 | STRING'''
    p[0] = Literal(p[1])

def p_error(p):
    if p:
        print(f"Erro sintático em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático no fim do arquivo")

parser = yacc.yacc()

# =========================
# Execução
# =========================

if __name__ == "__main__":
    filename = "Teste_Léxico.v"

    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    ast = parser.parse(source, lexer=lexer)

    print("\n# AST gerada:")
    print(ast)