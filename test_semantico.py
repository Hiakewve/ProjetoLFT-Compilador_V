from parser import parser
from semantico import SemanticVisitor

def testar_semantica(codigo, descricao):
    print(f"\n--- Teste: {descricao} ---")
    
    # 1. Parsing 
    ast = parser.parse(codigo)
    
    if not ast:
        print("Erro de Sintaxe (Parser falhou).")
        return

    # 2. Análise Semântica 
    semantic_visitor = SemanticVisitor()
    
    # 3. Uso do accept
    erros = ast.accept(semantic_visitor)

    if not erros:
        print("Sucesso! Nenhum erro semântico encontrado.")
    else:
        print(" Erros encontrados:")
        for erro in erros:
            print(f"   - {erro}")

# Casos de Teste 

# Caso 1: Código Correto
codigo_bom = """
fn main() {
    mut x := 10;
    mut y := 20;
    x = y + 5;
}
"""

# Caso 2: Erro de Tipo (Int + String)
codigo_erro_tipo = """
fn main() {
    mut x := 10;
    mut texto := "Ola";
    x = x + texto; 
}
"""

# Caso 3: Variável não declarada
codigo_nao_declarada = """
fn main() {
    x = 10;
}
"""

# Caso 4: Redeclaração de variável (Testando escopo)
codigo_redeclaracao = """
fn main() {
    mut x := 10;
    mut x := 20;
}
"""

if __name__ == "__main__":
    testar_semantica(codigo_bom, "Código Válido")
    testar_semantica(codigo_erro_tipo, "Soma de Tipos Incompatíveis")
    testar_semantica(codigo_nao_declarada, "Variável Não Declarada")
    testar_semantica(codigo_redeclaracao, "Redeclaração de Variável")