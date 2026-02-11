import ply.yacc as yacc
from lexico import tokens
from lexico import lexer
from ast_nodes import *
import sys

precedence = (
    ('left', 'OR'),           # 1
    ('left', 'AND'),          # 2
    ('left', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'), # 3
    ('left', 'PLUS', 'MINUS'), # 4
    ('left', 'TIMES', 'DIVIDE'), # 5
    ('right', 'NOT'),         # 5 (Unário)
)


# Regras:


def p_programa(p):
    'programa : lista_funcoes'
    p[0] = Programa(p[1])

def p_lista_funcoes(p):
    '''lista_funcoes : lista_funcoes funcao
                     | funcao'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_funcao(p):
    '''funcao : FN ID LPAREN params_opt RPAREN bloco'''
    p[0] = Funcao(p[2], p[4], p[6])

def p_params_opt(p):
    '''params_opt : params
                  | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_params(p):
    '''params : params COMMA ID
              | ID'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_bloco(p):
    'bloco : LBRACE lista_comandos RBRACE'
    p[0] = Bloco(p[2])

def p_lista_comandos(p):
    '''lista_comandos : lista_comandos comando
                      | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_comando(p):
    '''comando : declaracao SEMICOLON
               | atribuicao SEMICOLON
               | comando_if
               | comando_for
               | retorno SEMICOLON
               | chamada_func SEMICOLON''' 
    p[0] = p[1]

# Declaração usa := (MUT ID := Expr)
def p_declaracao(p):
    'declaracao : MUT ID DECLARE_ASSIGN expressao'
    p[0] = Declaracao(p[2], p[4])

# Atribuição usa = (ID = Expr)
def p_atribuicao(p):
    'atribuicao : ID ASSIGN expressao'
    p[0] = Atribuicao(p[1], p[3])

# IF conforme documentação (o elif é resolvido aninhando ifs no else)
def p_comando_if(p):
    '''comando_if : IF expressao bloco
                  | IF expressao bloco ELSE bloco'''
    if len(p) == 4:
        p[0] = If(p[2], p[3])
    else:
        p[0] = If(p[2], p[3], p[5])

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

# Chamada de função como comando (ex: print(x);)
def p_chamada_func(p):
    'chamada_func : ID LPAREN args_opt RPAREN'
    p[0] = ChamadaFuncao(p[1], p[3])

def p_args_opt(p):
    '''args_opt : args
                | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_args(p):
    '''args : args COMMA expressao
            | expressao'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# --- Expressões ---

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

def p_expressao_unaria(p):
    'expressao : NOT expressao'
    p[0] = UnaryOp(p[1], p[2])

def p_expressao_group(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]

def p_expressao_atomos(p):
    '''expressao : ID
                 | chamada_func'''
    if isinstance(p[1], ChamadaFuncao):
        p[0] = p[1]
    else:
        p[0] = Identificador(p[1])

def p_expressao_literal(p):
    '''expressao : INT
                 | FLOAT
                 | TRUE
                 | FALSE
                 | STRING'''
    # Detectar tipo baseado no token é ideal, mas aqui faremos inferência básica
    val = p[1]
    tipo = 'UNKNOWN'
    if isinstance(val, int) and val is not True and val is not False: tipo = 'INT'
    elif isinstance(val, float): tipo = 'FLOAT'
    elif isinstance(val, str): tipo = 'STRING'
    elif str(val) == 'true' or str(val) == 'false': tipo = 'BOOL' # String vinda do lexer
    
    # Ajuste para booleanos do lexer que podem vir como string 'true'/'false'
    if p.slice[1].type in ['TRUE', 'FALSE']:
        tipo = 'BOOL'
        val = p.slice[1].value # pegando valor cru

    p[0] = Literal(val, tipo)

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro sintático no token '{p.value}' (linha {p.lineno})")
    else:
        print("Erro sintático no fim do arquivo")

# Criando o parser
parser = yacc.yacc(debug=True, write_tables=True, tabmodule='parser_tab')