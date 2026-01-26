programa        → lista_funcoes
lista_funcoes   → funcao lista_funcoes | funcao

funcao          → FN ID LPAREN RPAREN bloco

bloco           → LBRACE lista_comandos RBRACE
lista_comandos  → comando lista_comandos | ε

comando →
      declaracao SEMICOLON
    | atribuicao SEMICOLON
    | comando_if
    | comando_for
    | retorno SEMICOLON

declaracao      → MUT ID DECLARE_ASSIGN expressao
atribuicao      → ID ASSIGN expressao

comando_if →
      IF expressao bloco
    | IF expressao bloco ELSE bloco

comando_for     → FOR expressao bloco

retorno →
      RETURN
    | RETURN expressao

expressao →
      expressao PLUS expressao
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
    | expressao OR expressao
    | NOT expressao
    | LPAREN expressao RPAREN
    | ID
    | literal

literal → INT | FLOAT | TRUE | FALSE | STRING
