import sys
from lexico import lexer
from parser import parser


# CÓDIGO FONTE DE TESTE 

codigo_fonte = """
fn main() {
    mut x := 10;
    mut y := 20.5;

    // Testando condicional
    if x < y {
        x = x + 1;
    } else {
        x = 0;
    }

    /* Testando 
       Loop */
    for x < 50 {
        x = x * 2;
    }

    return x;
}
"""

def teste_lexico(source):
    print("\n=== 1. TESTE LÉXICO (TOKENS) ===")
    lexer.input(source)
    while True:
        tok = lexer.token()
        if not tok:
            break      # Sem mais dados
        print(f"Token: {tok.type:<15} Valor: {tok.value:<10} Linha: {tok.lineno}")

def teste_parser_raw(source):
    print("\n=== 2. TESTE PARSER (AST BRUTA) ===")
    ast = parser.parse(source, lexer=lexer)
    if ast:
        print(ast)
    else:
        print("Erro: AST retornou None (Falha de sintaxe).")


if __name__ == "__main__":
    
     teste_lexico(codigo_fonte)
     teste_parser_raw(codigo_fonte)
