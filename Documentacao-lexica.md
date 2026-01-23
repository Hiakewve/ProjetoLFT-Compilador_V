# Documentação Léxica – Linguagem V

## 1. Introdução

Este documento descreve os elementos léxicos de um subconjunto da linguagem de programação V, definido para fins didáticos no contexto da disciplina de Linguagens Formais e Tradutores.

A linguagem V é uma linguagem compilada e estaticamente tipada, projetada para oferecer simplicidade, desempenho e segurança. Para viabilizar a implementação de um compilador completo dentro do escopo acadêmico da disciplina, foi definido um subconjunto da linguagem original, preservando suas principais características sintáticas e semânticas.

A análise léxica é a primeira etapa do processo de compilação e tem como objetivo transformar o código-fonte em uma sequência de tokens, que serão utilizados pelas fases subsequentes do compilador.

## 2. Palavras Reservadas

As palavras reservadas são identificadores com significado especial na linguagem e não podem ser utilizadas como nomes de variáveis, funções ou outros símbolos definidos pelo programador.

### 2.1. Literais Booleanos

true — representa o valor booleano verdadeiro.

false — representa o valor booleano falso.

### 2.2. Controle de Fluxo

if — inicia uma estrutura condicional.

else — define o bloco executado quando a condição do if é falsa.

for — inicia uma estrutura de repetição.

return — retorna um valor a partir de uma função.

### 2.3. Definição de Funções e Variáveis

fn — declara uma função.

mut — indica que uma variável é mutável.

## 3. Operadores

Os operadores definem as operações que podem ser realizadas sobre valores e variáveis. A tabela a seguir apresenta os operadores suportados, organizados por categoria, precedência e associatividade.

### 3.1. Operadores Aritméticos
| Operador | Descrição     | Precedência | Associatividade |
| :------: | ------------- | :---------: | :-------------: |
|    `+`   | Adição        |      4      |     Direita     |
|    `-`   | Subtração     |      4      |     Direita     |
|    `*`   | Multiplicação |      5      |     Direita     |
|    `/`   | Divisão       |      5      |     Direita     |
### 3.2. Operadores de Atribuição
| Operador | Descrição                                     | Precedência | Associatividade |
| :------: | --------------------------------------------- | :---------: | :-------------: |
|    `=`   | Atribuição simples                            |      1      |     Direita     |
|   `:=`   | Declaração de variável com inferência de tipo |      1      |     Direita     |
### 3.3. Operadores de Comparação
| Operador | Descrição        | Precedência | Associatividade |
| :------: | ---------------- | :---------: | :-------------: |
|   `==`   | Igualdade        |      3      |     Direita     |
|   `!=`   | Diferença        |      3      |     Direita     |
|    `<`   | Menor que        |      3      |     Direita     |
|   `<=`   | Menor ou igual a |      3      |     Direita     |
|    `>`   | Maior que        |      3      |     Direita     |
|   `>=`   | Maior ou igual a |      3      |     Direita     |
### 3.4. Operadores Lógicos
| Operador | Descrição      | Precedência | Associatividade |
| :------: | -------------- | :---------: | :-------------: |
|   `&&`   | E lógico       |      2      |     Direita     |
|  `\|\|`  | OU lógico      |      1      |     Direita     |
|    `!`   | Negação lógica |      5      |     Esquerda    |
## 4. Delimitadores

Os delimitadores são símbolos utilizados para estruturar o código-fonte, organizar expressões e definir blocos de comandos.

Parênteses () — utilizados para agrupamento de expressões e chamadas de função.

Chaves {} — delimitam blocos de código, como corpos de funções, condicionais e laços.

Colchetes [] — utilizados para indexação de estruturas e definição de listas.

Vírgula , — separa argumentos em chamadas de função e listas de elementos.

Ponto e vírgula ; — opcional, podendo ser utilizado para separar comandos explicitamente.

## 5. Identificadores

Identificadores são nomes atribuídos a variáveis, funções e outros elementos definidos pelo programador.

### 5.1. Regras de Formação

Devem iniciar com uma letra (a-z ou A-Z) ou sublinhado (_).

Podem conter letras, números (0-9) e sublinhados após o primeiro caractere.

São sensíveis a maiúsculas e minúsculas (case-sensitive).

Não podem coincidir com palavras reservadas da linguagem.

Não podem conter espaços ou caracteres especiais.

### 5.2. Exemplos Válidos

contador

_total

valor1

MinhaFuncao

## 6. Literais Numéricos

A linguagem suporta literais numéricos inteiros e de ponto flutuante, escritos na base decimal.

### 6.1. Inteiros

Representam números inteiros sem parte fracionária.

Exemplos: 0, 10, 42, 1000

### 6.2. Ponto Flutuante

Representam números reais com parte fracionária.

Exemplos: 3.14, 0.5, 10.0

## 7. Literais de String

Literais de string representam sequências de caracteres e podem ser delimitados por aspas simples (' ') ou aspas duplas (" ").

Sequências de escape comuns são reconhecidas, como:

\n — nova linha

\t — tabulação

\" — aspas duplas

\' — aspas simples

Exemplo
mensagem := "Olá, mundo!\n"

## 8. Comentários

Comentários são ignorados pelo compilador e utilizados apenas para documentação do código.

Comentário de linha: inicia com // e termina no fim da linha.

Comentário de bloco: delimitado por /* e */.

## 9. Erros Léxicos

Um erro léxico ocorre quando o analisador léxico encontra uma sequência de caracteres que não corresponde a nenhum token válido da linguagem.

Exemplos de erros léxicos incluem:

Uso de caracteres inválidos.

Identificadores iniciados por números.

Literais mal formados.

Espaços em branco, tabulações e quebras de linha são ignorados durante o reconhecimento de tokens, sendo utilizados apenas para rastreamento de posição (linha e coluna) com o objetivo de fornecer mensagens de erro precisas.

## 10. Considerações Finais

Esta especificação léxica define um subconjunto da linguagem V suficientemente expressivo para permitir a construção de programas funcionais, ao mesmo tempo em que mantém a complexidade necessária para a implementação de um compilador completo em ambiente acadêmico.
