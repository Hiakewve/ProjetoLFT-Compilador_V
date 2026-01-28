import ply.yacc as yacc
from lexico import tokens
from lexico import lexer
import sys

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
    p[0] = ('programa', p[1])

def p_lista_funcoes(p):
    '''lista_funcoes : funcao lista_funcoes
                      | funcao'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]



# ANALISAR ESSA FUNÇÃO AI DPS

#def p_funcao(p):
 #   '''funcao : FN ID LPAREN param RPAREN bloco
 #             | FN ID LPAREN RPAREN bloco'''
  #  
 #   if len(p) == 6:  # FN ID LPAREN RPAREN bloco
 #       p[0] = ('funcao', p[2], [], p[5])  # sem parâmetros
 #   else:            # FN ID LPAREN param RPAREN bloco
 #       p[0] = ('funcao', p[2], p[4], p[6])  # com parâmetros



#def p_param_simples(p):
 #   'param : ID'
 #   p[0] = [p[1]]  # lista com 1 parâmetro

#def p_param_varios(p):
#    'param : ID COMMA param'
#    p[0] = [p[1]] + p[3]  # concatena recursivamente





def p_funcao(p):
    'funcao : FN ID LPAREN RPAREN bloco'
    p[0] = ('funcao', p[2], p[5])

def p_bloco(p):
    'bloco : LBRACE lista_comandos RBRACE'
    p[0] = p[2]

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
    p[0] = ('decl', p[2], p[4])

def p_atribuicao(p):
    'atribuicao : ID ASSIGN expressao'
    p[0] = ('assign', p[1], p[3])

    
 #Tem que testar ai dps
def p_comando_if(p):
    '''comando_if : IF expressao bloco
                   | IF expressao bloco ELSE bloco
                   | IF expressao bloco elseIfList
                   | IF expressao bloco elseIfList ELSE bloco'''
    
    if len(p) == 4:
        # if simples
        p[0] = ('if', p[2], p[3])
    
    elif len(p) == 6 and p[1] == 'if':
        # if ... else ...
        p[0] = ('if_else', p[2], p[3], p[5])
    
    elif len(p) == 5:
        # if ... else if ...
        p[0] = ('if_elseif', p[2], p[3], p[4])
    
    elif len(p) == 7:
        # if ... else if ... else ...
        p[0] = ('if_elseif_else', p[2], p[3], p[4], p[6])


def p_elseIfList_simples(p):
    'elseIfList : ELSE IF expressao bloco'
    p[0] = [('elseif', p[3], p[4])]

def p_elseIfList_varios(p):
    'elseIfList : ELSE IF expressao bloco elseIfList'
    p[0] = [('elseif', p[3], p[4])] + p[5]




def p_comando_for(p):
    'comando_for : FOR expressao bloco'
    p[0] = ('for', p[2], p[3])

def p_retorno(p):
    '''retorno : RETURN
                | RETURN expressao'''
    if len(p) == 2:
        p[0] = ('return', None)
    else:
        p[0] = ('return', p[2])

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
    p[0] = ('binop', p[2], p[1], p[3])

def p_expressao_not(p):
    'expressao : NOT expressao'
    p[0] = ('not', p[2])

def p_expressao_group(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]

def p_expressao_id(p):
    'expressao : ID'
    p[0] = ('id', p[1])

def p_expressao_literal(p):
    '''expressao : INT
                  | FLOAT
                  | TRUE
                  | FALSE
                  | STRING'''
    p[0] = ('literal', p[1])

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