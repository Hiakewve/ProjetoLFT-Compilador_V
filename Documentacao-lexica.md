# Especificações Léxicas – Linguagem V

A **V** é uma linguagem compilada estática que prioriza a manutenção de código e segurança. Diferente de linguagens de script, seu léxico é desenhado para permitir uma compilação de passagem única extremamente veloz.

---

## 1. Keywords Centrais (Vocabulário Nativo)

Estes termos são os pilares da gramática da linguagem. Por serem reservados para a lógica interna do compilador, não podem ser reutilizados para nomear funções ou variáveis.

| Categoria | Palavras-chave |
| :--- | :--- |
| **Controle e Fluxo** | `if`, `else`, `for`, `match`, `break`, `continue`, `return`, `defer`, `goto` |
| **Definições e Visibilidade** | `fn`, `const`, `mut`, `pub`, `shared`, `static` |
| **Outros** | `as`, `asm`, `assert`, `in`, `is`, `none`, `or`, `sizeof`, `typeof`, `false`, `true` |

---

## 2. Lógica e Aritmética (Operadores)

A V utiliza símbolos específicos para manipulação de dados. Uma característica única é a ausência de incrementos como `++` em expressões para evitar ambiguidades.

### 1. Operadores Unários (Maior Precedência)
* `! ~ -` : Negação lógica, NOT de bits e sinal negativo.

### 2. Exponenciação
* `**` : Cálculo de potência.

### 3. Operadores Multiplicativos e de Bits
* `* / %` : Multiplicação, divisão e resto.
* `<< >>` : Deslocamento de bits (Shifts).
* `&` : AND de bits.

### 4. Operadores Aditivos e de Bits
* `+ -` : Soma e subtração.
* `| ^` : OR e XOR de bits.

### 5. Comparações e Validação
* `== !=` : Igualdade e desigualdade.
* `< > <= >=` : Comparação de magnitude.

### 6. Operações Lógicas
* `&&` : E lógico.
* `||` : OU lógico.

### 7. Atribuição (Menor Precedência)
* `:=` : Declaração com inferência de tipo.
* `=` : Atribuição simples.
* `+= -= *= /=` : Atribuições compostas.

---

## 3. Sinalização Estrutural (Delimitadores)

Símbolos que organizam a hierarquia e o escopo do código:

* `{ }` : Envolvem blocos de código e corpos de funções.
* `[ ]` : Utilizados para indexação e definição de arrays/mapas.
* `( )` : Agrupam expressões e delimitam parâmetros de funções.
* `? !` : Marcadores de tipos opcionais ou que podem retornar erros.

---

## 4. Padrões de Nomeação (Identificadores)

Regras para a criação de nomes por parte do desenvolvedor:

* **Formato:** Devem obrigatoriamente começar com letra ou underline (`_`).
* **Estilo:** A linguagem V incentiva estritamente o `snake_case` (ex: `meu_valor`, `calcular_area`).
* **Restrição:** Não são permitidos caracteres especiais ou espaços.

---

## 5. Representação de Texto (Strings)

Diferente de linguagens como Lua, a V trata strings de forma muito específica:

* **Aspas Simples (`' '`):** É o padrão da linguagem para strings.
* **Aspas Duplas (`" "`):** Também permitidas, geralmente usadas se a string contiver aspas simples.
* **Interpolação:** Usa-se o cifrão dentro da string para injetar valores: `'Olá, $nome'`.

---

## 6. Literais e Formatação Numérica

* **Inteiros:** `100`, `-5`. Permite o uso de underscores para legibilidade: `1_000_000`.
* **Decimais:** `3.14`, `.5`.
* **Bases Especiais:** `0x` (Hex), `0b` (Binário), `0o` (Octal).

---

## 7. Documentação de Código (Comentários)

Essenciais para a leitura humana, são ignorados pelo processo de compilação:

```
// Comentário de linha única.

/* Comentário de múltiplas 
   linhas ou blocos.
*/
```
---
## 8. Diagnóstico de Integridade (Erros)

O compilador atua como a primeira linha de defesa contra bugs:

* **Erro de Lexer** : Caractere inválido ou não reconhecido.
* **Erro de Mutabilidade** : Tentar alterar uma variável sem o modificador `mut`.
* **Aviso de Variável Não Utilizada** : A V **não compila** se houver variáveis declaradas que não são usadas (garantia de código limpo).
