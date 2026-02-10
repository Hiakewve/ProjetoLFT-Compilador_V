import ply.lex as lex

# Palavras reservadas
reservadas = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'return': 'RETURN',
    'fn': 'FN',
    'mut': 'MUT',
    'true': 'TRUE',
    'false': 'FALSE',
}

# tokens


tokens = [
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'DECLARE_ASSIGN',
    'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
    'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON',
    'INT', 'FLOAT', 'STRING',
    'ID',
] + list(reservadas.values())

# regras de regex


t_DECLARE_ASSIGN = r':='
t_EQ = r'=='
t_NEQ = r'!='
t_LE = r'<='
t_GE = r'>='
t_AND = r'&&'
t_OR = r'\|\|'

t_ASSIGN = r'='
t_LT = r'<'
t_GT = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_NOT = r'!'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_COMENTARIO_LINHA(t):
    r'//.*'
    pass

def t_COMENTARIO_BLOCO(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_NOVALINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: Caractere inválido '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

t_ignore = ' \t'

if __name__ == "__main__":
    lexer = lex.lex()
    with open("Teste_Léxico.v", "r", encoding = "utf-8") as f:
        lexer.input(f.read())

    print("\n# Lexer output: ")
    for tok in lexer:
        print(tok)

lexer = lex.lex()
