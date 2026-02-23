from ast_nodes import *

class Visitor:
    """
    Classe base para os Visitors.
    Define a interface que deve ser implementada para percorrer a AST.
    """
    def visit_Programa(self, node): pass
    def visit_Funcao(self, node): pass
    def visit_Bloco(self, node): pass
    def visit_Declaracao(self, node): pass
    def visit_Atribuicao(self, node): pass
    def visit_If(self, node): pass
    def visit_For(self, node): pass
    def visit_Return(self, node): pass
    def visit_ChamadaFuncao(self, node): pass
    def visit_BinOp(self, node): pass
    def visit_UnaryOp(self, node): pass
    def visit_Literal(self, node): pass
    def visit_Identificador(self, node): pass

class PrettyPrinter(Visitor):
    """
    Reconstrói o código fonte a partir da AST.
    """
    def __init__(self):
        self.indent_level = 0

    def _indent(self):
        """Gera a string de indentação baseada no nível atual."""
        return "    " * self.indent_level

    def visit_Programa(self, node):
        resultado = ""
        # node.funcoes
        for func in node.funcoes:
            resultado += func.accept(self) + "\n\n"
        return resultado

    def visit_Funcao(self, node):
        # node.params 
        params_str = ", ".join(node.params)
        # Visita o bloco da função
        bloco_str = node.bloco.accept(self)
        return f"fn {node.nome}({params_str}) {bloco_str}"

    def visit_Bloco(self, node):
        self.indent_level += 1
        comandos_str = ""
        for cmd in node.comandos:
            # cmd.accept(self) visita o comando específico 
            comandos_str += self._indent() + cmd.accept(self) + "\n"
        self.indent_level -= 1
        return "{\n" + comandos_str + self._indent() + "}"

    def visit_Declaracao(self, node):
        # Formato: mut ID := expressao;
        return f"mut {node.nome} := {node.expr.accept(self)};"

    def visit_Atribuicao(self, node):
        # Formato: ID = expressao;
        return f"{node.nome} = {node.expr.accept(self)};"

    def visit_If(self, node):
        # Reconstrói: if condicao TRECHO else TRECHO
        resultado = f"if {node.condicao.accept(self)} {node.bloco_then.accept(self)}"
        if node.bloco_else:
            resultado += f" else {node.bloco_else.accept(self)}"
        return resultado

    def visit_For(self, node):
        # Reconstrói: for condicao TRECHO
        return f"for {node.condicao.accept(self)} {node.bloco.accept(self)}"

    def visit_Return(self, node):
        if node.expr:
            return f"return {node.expr.accept(self)};"
        return "return;"

    def visit_ChamadaFuncao(self, node):
        # Reconstrói: funcao(arg1, arg2)
        args_str = ", ".join([arg.accept(self) for arg in node.args])
        return f"{node.nome}({args_str})"

    def visit_BinOp(self, node):
        # Adicao do parenteses para melhoria visual
        return f"{node.esquerda.accept(self)} {node.op} {node.direita.accept(self)}"

    def visit_UnaryOp(self, node):
        return f"{node.op}{node.operand.accept(self)}"

    def visit_Literal(self, node):
        # Tratamento para garantir que strings tenham aspas
        # e booleanos sejam minúsculos 
        if node.tipo == 'STRING':
            return f'"{node.valor}"'
        elif node.tipo == 'BOOL':
            return str(node.valor).lower()
        return str(node.valor)

    def visit_Identificador(self, node):
        return node.nome

# TESTE 

if __name__ == "__main__":
    import sys
    try:
        from parser import parser
    except ImportError:
        print("Erro: Arquivo 'parser.py' não encontrado.")
        sys.exit(1)

    codigo_teste = """
    fn main() {
        mut x := 10;
        mut mensagem := "Ola Mundo";
        
        if x > 5 {
            x = x + 1;
        } else {
            x = 0;
        }

        for x < 20 {
            print(x);
            x = x + 1;
        }
        
        return x;
    }
    """

    print("Código Fonte Original")
    print(codigo_teste.strip())
    print("\n Processando... ")

    ast = parser.parse(codigo_teste)

    if ast:
        printer = PrettyPrinter()
        codigo_gerado = ast.accept(printer)
        print("\n--- Código Gerado pelo Visitor (PrettyPrinter) ---")
        print(codigo_gerado)
    else:
        print("Erro: O parser retornou None. Verifique se há erros de sintaxe.")