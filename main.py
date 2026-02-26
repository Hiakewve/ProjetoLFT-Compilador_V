from parser import parser
from semantico import SemanticVisitor
from gerador_assembly import AssemblyVisitor

# Códigos de teste:
codigo_fonte = """
fn main() {
    mut contador := 0;
    mut limite := 5;
    mut soma := 0;

    for contador < limite {
        contador = contador + 1;
        soma = soma + contador;
        print(soma); // Deve imprimir 1, 3, 6, 10, 15
    }
}
"""
# Teste de operações
codigo_fonte_2 = """
fn main() {
    mut a := 10;
    mut b := 5;
    
    mut soma := a + b;
    mut sub := a - b;
    mut mult := a * b;
    mut div := a / b;

    print(soma);
    print(sub);
    print(mult);
    print(div);
}
"""
# Teste de condicionais
codigo_fonte_3 = """

fn main() {
    mut num := 7;
    mut temp := num / 2;
    mut teste := temp * 2;

    if teste == num {
        print(1); // 1 = Par
    } else {
        print(0); // 0 = Impar
    }
}

"""
# Teste de escopo e shadowing
codigo_fonte_4 = """
fn main() {

    mut x := 10;
    print(x); // Imprime 10
    
    if 1 == 1 {
        mut x := 20; 
        print(x);    // Imprime 20
        
        mut y := 30;
        print(y);    // Imprime 30
    }
    
    print(x); // Imprime 10
}
"""
print(" Compilador da Linguagem V ")

# 1. Análise Léxica e Sintática
print("1. Executando Parser...")
ast = parser.parse(codigo_fonte_4)

if not ast:
    print(" Erro Sintático: Compilação abortada.")
    exit(1)

# 2. Análise Semântica
print("2. Executando Analisador Semântico...")
semantico = SemanticVisitor()
erros = ast.accept(semantico)

if erros:
    print(" Erros Semânticos Encontrados:")
    for erro in erros:
        print(f"  -> {erro}")
    exit(1)
else:
    print(" Semântica Aprovada !!")

# 3. Geração de Código
print("3. Gerando Assembly MIPS...")
codegen = AssemblyVisitor()
codigo_assembly = ast.accept(codegen)

# 4. Salvar Arquivo
nome_arquivo = "programa5.asm"
with open(nome_arquivo, "w") as f:
    f.write(codigo_assembly)

print(f" Sucesso! Arquivo '{nome_arquivo}' gerado com sucesso.")
print("-" * 40)
print(codigo_assembly)