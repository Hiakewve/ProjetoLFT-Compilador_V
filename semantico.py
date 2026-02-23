from ast_nodes import *
from visitor import Visitor

class TabelaSimbolos:
    def __init__(self):
        # Pilha de escopos. O índice 0 é o global.
        self.scopes = [{}] 

    def enter_scope(self):
        """Cria um novo escopo (ex: entrar em uma função ou bloco)"""
        self.scopes.append({})

    def exit_scope(self):
        """Sai do escopo atual."""
        self.scopes.pop()

    def define(self, nome, tipo, mutavel=False):
        """Registra uma variável no escopo atual"""
        escopo_atual = self.scopes[-1]
        if nome in escopo_atual:
            return False # Erro: Variável já declarada neste escopo
        escopo_atual[nome] = {'tipo': tipo, 'mut': mutavel}
        return True

    def lookup(self, nome):
        """Busca uma variável do escopo atual até o global"""
        for escopo in reversed(self.scopes):
            if nome in escopo:
                return escopo[nome]
        return None

class SemanticVisitor(Visitor):
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.erros = [] # Lista para acumular erros semânticos

    def log_erro(self, msg):
        self.erros.append(msg)

    #  Estrutura Geral 

    def visit_Programa(self, node):
        # Registra funções antes de visitar o corpo (para permitir recursão)
        # Por simplicidade, assumimos que funções são globais
        for func in node.funcoes:
            # Aqui poderíamos registrar a assinatura da função na tabela
            func.accept(self)
        
        # Se houver erros, retornamos a lista
        return self.erros

    def visit_Funcao(self, node):
        self.tabela.enter_scope() # Novo escopo para parâmetros e corpo
        
        # Registrar parâmetros
        # Como a gramática simplificada não tem tipo explícito no param,
        # assumimos 'ANY'
        for param in node.params:
            self.tabela.define(param, 'ANY')

        node.bloco.accept(self)
        self.tabela.exit_scope()

    def visit_Bloco(self, node):
        for cmd in node.comandos:
            cmd.accept(self)

    #  Declarações e Comandos 

    def visit_Declaracao(self, node):
        # Inferência de tipo
        tipo_expr = node.expr.accept(self) # Visita a expressão para descobrir o tipo
        
        if tipo_expr:
            sucesso = self.tabela.define(node.nome, tipo_expr, mutavel=True)
            if not sucesso:
                self.log_erro(f"Erro Semântico: Variável '{node.nome}' já declarada neste escopo.")
        
    def visit_Atribuicao(self, node):
        # Regra: x = 20; (x deve existir e tipos devem bater)
        info_var = self.tabela.lookup(node.nome)
        
        if not info_var:
            self.log_erro(f"Erro Semântico: Variável '{node.nome}' não declarada.")
            return

        tipo_expr = node.expr.accept(self)
        
        # Verificação de Tipo (Ignora se for ANY ou UNKNOWN para evitar erros em cascata)
        if info_var['tipo'] != 'ANY' and tipo_expr != 'UNKNOWN' and tipo_expr != info_var['tipo']:
            # Permite coerção simples (int -> float) 
            # Exceto se um for float e outro int, talvez queira permitir. 
            self.log_erro(f"Erro de Tipo: Atribuindo {tipo_expr} para variável '{node.nome}' ({info_var['tipo']}).")

    def visit_If(self, node):
        tipo_cond = node.condicao.accept(self)
        if tipo_cond != 'BOOL' and tipo_cond != 'ANY' and tipo_cond != 'UNKNOWN':
             # Opcional: Warning ou Erro se condição não for booleana
             pass 
        
        node.bloco_then.accept(self)
        if node.bloco_else:
            node.bloco_else.accept(self)

    def visit_For(self, node):
        node.condicao.accept(self)
        node.bloco.accept(self)

    def visit_Return(self, node):
        if node.expr:
            node.expr.accept(self)

    def visit_ChamadaFuncao(self, node):
        # Aqui verificaríamos se a função existe e se os args batem
        for arg in node.args:
            arg.accept(self)
        return 'ANY' # Retorna ANY pois não temos tabela de funções completa ainda

    # Expressões (Retornam TIPOS)

    def visit_BinOp(self, node):
        esq_tipo = node.esquerda.accept(self)
        dir_tipo = node.direita.accept(self)

        # Se algum lado já tem erro, propaga o erro
        if esq_tipo == 'ERROR' or dir_tipo == 'ERROR':
            return 'ERROR'

        # Regra: Operações aritméticas exigem tipos iguais
        if node.op in ['+', '-', '*', '/']:
            if esq_tipo == dir_tipo:
                return esq_tipo # INT + INT = INT
            elif esq_tipo == 'ANY' or dir_tipo == 'ANY':
                return 'ANY'
            else:
                self.log_erro(f"Erro de Tipo: Operação '{node.op}' entre {esq_tipo} e {dir_tipo}.")
                return 'ERROR'
        
        # Regra: Operações relacionais retornam BOOL
        if node.op in ['>', '<', '>=', '<=', '==', '!=']:
            if esq_tipo == dir_tipo or esq_tipo == 'ANY' or dir_tipo == 'ANY':
                return 'BOOL'
            else:
                self.log_erro(f"Erro de Tipo: Comparação '{node.op}' entre {esq_tipo} e {dir_tipo}.")
                return 'ERROR'
        
        # Operadores Lógicos
        if node.op in ['&&', '||']:
            return 'BOOL'

        return 'UNKNOWN'

    def visit_UnaryOp(self, node):
        tipo = node.operand.accept(self)
        if node.op == '!':
            return 'BOOL'
        return tipo

    def visit_Literal(self, node):
        # O nó literal já tem o tipo salvo pelo Parser
        return node.tipo

    def visit_Identificador(self, node):
        info = self.tabela.lookup(node.nome)
        if info:
            return info['tipo']
        else:
            self.log_erro(f"Erro Semântico: Variável '{node.nome}' usada antes da declaração.")
            return 'ERROR'