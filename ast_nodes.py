# ast_nodes.py
from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

# --- Estrutura Geral ---

class Programa(Node):
    def __init__(self, funcoes):
        self.funcoes = funcoes

    def accept(self, visitor):
        return visitor.visit_Programa(self)

class Funcao(Node):
    def __init__(self, nome, params, bloco):
        self.nome = nome
        self.params = params  # Lista de strings (IDs)
        self.bloco = bloco

    def accept(self, visitor):
        return visitor.visit_Funcao(self)

class Bloco(Node):
    def __init__(self, comandos):
        self.comandos = comandos

    def accept(self, visitor):
        return visitor.visit_Bloco(self)

# --- Comandos (Statements) ---

class Declaracao(Node):
    def __init__(self, nome, expr):
        self.nome = nome
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_Declaracao(self)

class Atribuicao(Node):
    def __init__(self, nome, expr):
        self.nome = nome
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_Atribuicao(self)

class If(Node):
    def __init__(self, condicao, bloco_then, bloco_else=None):
        self.condicao = condicao
        self.bloco_then = bloco_then
        self.bloco_else = bloco_else # Pode ser None

    def accept(self, visitor):
        return visitor.visit_If(self)

class For(Node):
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

    def accept(self, visitor):
        return visitor.visit_For(self)

class Return(Node):
    def __init__(self, expr=None):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_Return(self)

class ChamadaFuncao(Node):
    def __init__(self, nome, args):
        self.nome = nome
        self.args = args

    def accept(self, visitor):
        return visitor.visit_ChamadaFuncao(self)

# --- Expressões ---

class BinOp(Node):
    def __init__(self, esquerda, op, direita):
        self.esquerda = esquerda
        self.op = op
        self.direita = direita

    def accept(self, visitor):
        return visitor.visit_BinOp(self)

class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_UnaryOp(self)

class Literal(Node):
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo # 'INT', 'FLOAT', 'BOOL', 'STRING'

    def accept(self, visitor):
        return visitor.visit_Literal(self)

class Identificador(Node):
    def __init__(self, nome):
        self.nome = nome

    def accept(self, visitor):
        return visitor.visit_Identificador(self)