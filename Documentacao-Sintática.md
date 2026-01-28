# Linguagem V — Documentação Sintática

# 1. Introdução

Este documento descreve a sintaxe do subconjunto da linguagem V definido para fins didáticos na disciplina de Linguagens Formais e Tradutores.

A sintaxe especifica como os tokens produzidos pelo analisador léxico podem ser organizados para formar programas válidos. A linguagem utiliza uma sintaxe estruturada, baseada em blocos delimitados por chaves ({}) e comandos terminados obrigatoriamente por ponto e vírgula (;).

# 2. Estrutura Geral do Programa

Um programa é composto por uma ou mais declarações de função.
A função main é obrigatória e representa o ponto de entrada do programa.

programa -> lista_funcoes

# 3. Funções

Funções são declaradas utilizando a palavra-chave fn, seguidas de um identificador, lista de parâmetros (opcional) e um bloco de comandos.

funcao -> fn ID ( ) bloco

# 4. Blocos de Comandos

Blocos são sequências de comandos delimitadas por chaves {}.

bloco -> { lista_comandos }

# 5. Comandos

Os comandos suportados pela linguagem são:

- Declaração de variável
- Atribuição
- Estrutura condicional (if)
- Estrutura de repetição (for)
- Retorno de função
- Chamada de Função
- Comando vazio (opcional)

Todos os comandos devem terminar com ponto e vírgula (;), exceto blocos.

comando →
    declaracao ;
  | atribuicao ;
  | comando_if
  | comando_for
  | retorno ;

# 6. Declaração e Atribuição

declaracao → mut ID := expressao
atribuicao → ID = expressao

# 7. Estruturas de Controle
## 7.1 Condicional

comando_if →
    if expressao bloco
  | if expressao bloco else bloco

## 7.2 Repetição

comando_for → for expressao bloco

# 8. Retorno

retorno →
    return
  | return expressao

# 9. Expressões

A linguagem suporta expressões aritméticas, relacionais e lógicas.

expressao →
    expressao + expressao
  | expressao - expressao
  | expressao * expressao
  | expressao / expressao
  | expressao == expressao
  | expressao != expressao
  | expressao < expressao
  | expressao <= expressao
  | expressao > expressao
  | expressao >= expressao
  | expressao && expressao
  | expressao || expressao
  | ! expressao
  | ( expressao )
  | ID
  | literal

# 10. Literais

literal → INT | FLOAT | TRUE | FALSE | STRING

# 11. Exemplos de Código
## Programa Válido
fn main() {
    mut x := 10;
    if x > 5 {
        x = x + 1;
    }
    return;
}

## Exemplo com laço For
fn main() {
    mut x := 0;
    for x < 10 {
        x = x + 1;
    }
    return;
}
