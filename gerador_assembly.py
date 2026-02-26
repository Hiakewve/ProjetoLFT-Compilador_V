from ast_nodes import *
from visitor import Visitor

class AssemblyVisitor(Visitor):
    def __init__(self):
        self.code = []           
        self.data = []           
        self.label_count = 0     
        
        # (Lista de dicionários)
        self.scopes = [{}]       
        self.current_offset = 0  

    def lookup_offset(self, nome):
        """Busca a posição da variável do escopo mais interno para o externo."""
        for scope in reversed(self.scopes):
            if nome in scope:
                return scope[nome]
        raise Exception(f"Erro Crítico: Variável '{nome}' ")
    
    #  Funções Auxiliares 

    def emit(self, instruction, comment=""):
        """Adiciona uma instrução ao buffer de código."""
        linha = f"    {instruction:<25}"
        if comment:
            linha += f"# {comment}"
        self.code.append(linha)

    def new_label(self):
        """Gera um rótulo único para saltos (ifs, loops)."""
        lbl = f"L_{self.label_count}"
        self.label_count += 1
        return lbl

    def push_a0(self):
        """Empilha o valor de $a0 na pilha do sistema."""
        self.emit("addi $sp, $sp, -4", "Abre espaco na pilha")
        self.emit("sw $a0, 0($sp)", "Push $a0")

    def pop_t1(self):
        """Desempilha o topo da pilha para $t1."""
        self.emit("lw $t1, 0($sp)", "Pop para $t1")
        self.emit("addi $sp, $sp, 4", "Restaura espaco na pilha")

    # Estrutura do Programa 

    def visit_Programa(self, node):
        self.data.append(".data")
        self.data.append('newline: .asciiz "\\n"') 
        
        self.code.append(".text")
        self.code.append(".globl main")
        
        for func in node.funcoes:
            func.accept(self)
            
        # Junta os segmentos .data e .text
        str_data = "\n".join(self.data)
        str_text = "\n".join(self.code)
        return f"{str_data}\n\n{str_text}"

    def visit_Funcao(self, node):
        self.code.append(f"\n{node.nome}:")
        
        # Uso da abordagem Stack Frame.
        self.emit("addi $sp, $sp, -8", "Abre espaco para $fp e $ra")
        self.emit("sw $fp, 4($sp)", "Salva $fp antigo")
        self.emit("sw $ra, 0($sp)", "Salva retorno ($ra)")
        self.emit("move $fp, $sp", "Atualiza Frame Pointer")
        
        # RESETA A PILHA DE ESCOPOS 
        self.scopes = [{}]
        self.current_offset = -4 

        node.bloco.accept(self)

        self.code.append(f"end_{node.nome}:")
        if node.nome == "main":
            self.emit("li $v0, 10", "Syscall: Exit")
            self.emit("syscall")
        else:
            self.emit("move $sp, $fp", "Restaura Stack Pointer")
            self.emit("lw $ra, 0($sp)", "Restaura $ra")
            self.emit("lw $fp, 4($sp)", "Restaura $fp antigo")
            self.emit("addi $sp, $sp, 8", "Desaloca frame")
            self.emit("jr $ra", "Retorna para o chamador")

    def visit_Bloco(self, node):
        # Cria um novo escopo de memória para o bloco
        self.scopes.append({}) 
        
        for cmd in node.comandos:
            cmd.accept(self)
            
        # Destrói o mapa de nomes do bloco. 
        # (A memória no $fp continua alocada, mas o nome fica inacessível)
        self.scopes.pop()

    # Variáveis 

    def visit_Declaracao(self, node):
        node.expr.accept(self)
        
        # Salva a variável no ESCOPO ATUAL 
        self.scopes[-1][node.nome] = self.current_offset
        self.emit(f"sw $a0, {self.current_offset}($fp)", f"Guarda var '{node.nome}'")
        
        # Avisa o sistema para mover a ponta da pilha para baixo
        self.emit("addi $sp, $sp, -4", "Protege memoria da variavel local")

        self.current_offset -= 4


    def visit_Atribuicao(self, node):
        node.expr.accept(self)
    #busca
        offset = self.lookup_offset(node.nome)
        self.emit(f"sw $a0, {offset}($fp)", f"Atualiza var '{node.nome}'")

    # Fluxo de Controle

    def visit_If(self, node):
        lbl_else = self.new_label()
        lbl_fim = self.new_label()

        node.condicao.accept(self)
        # Se falso (0), pula pro else
        self.emit(f"beqz $a0, {lbl_else}", "Se falso, pula para ELSE")
        
        # Bloco THEN
        node.bloco_then.accept(self)
        self.emit(f"j {lbl_fim}", "Pula para o FIM do IF")
        
        # Bloco ELSE
        self.code.append(f"{lbl_else}:")
        if node.bloco_else:
            node.bloco_else.accept(self)
            
        self.code.append(f"{lbl_fim}:")

    def visit_For(self, node):
        lbl_inicio = self.new_label()
        lbl_fim = self.new_label()

        self.code.append(f"{lbl_inicio}:")
        
        # Avalia condição
        node.condicao.accept(self)
        self.emit(f"beqz $a0, {lbl_fim}", "Se falso, sai do FOR")
        
        # Executa bloco
        node.bloco.accept(self)
        
        # Volta pro início
        self.emit(f"j {lbl_inicio}", "Volta para o inicio do FOR")
        self.code.append(f"{lbl_fim}:")

    #  Expressões MIPS (Máquina de Pilha) 

    def visit_BinOp(self, node):
        # 1. Avalia lado esquerdo e Empilha
        node.esquerda.accept(self)
        self.push_a0()
        
        # 2. Avalia lado direito (Fica em $a0)
        node.direita.accept(self)
        
        # 3. Desempilha o lado esquerdo para $t1
        self.pop_t1()
        
        # Agora: $t1 = Esquerda | $a0 = Direita
        op = node.op
        if op == '+': self.emit("add $a0, $t1, $a0", "Soma")
        elif op == '-': self.emit("sub $a0, $t1, $a0", "Subtracao")
        elif op == '*': self.emit("mul $a0, $t1, $a0", "Multiplicacao")
        elif op == '/': 
            self.emit("div $t1, $a0", "Divisao")
            self.emit("mflo $a0", "Pega o quociente")
        
        # Relacionais (Retornam 1 se verdadeiro, 0 se falso)
        elif op == '==': self.emit("seq $a0, $t1, $a0", "Igual")
        elif op == '!=': self.emit("sne $a0, $t1, $a0", "Diferente")
        elif op == '<':  self.emit("slt $a0, $t1, $a0", "Menor que")
        elif op == '>':  self.emit("sgt $a0, $t1, $a0", "Maior que")
        elif op == '<=': self.emit("sle $a0, $t1, $a0", "Menor ou igual")
        elif op == '>=': self.emit("sge $a0, $t1, $a0", "Maior ou igual")

    def visit_Literal(self, node):
        if node.tipo == 'INT':
            self.emit(f"li $a0, {node.valor}", f"Carrega INT {node.valor}")
        elif node.tipo == 'BOOL':
            val = 1 if node.valor else 0
            self.emit(f"li $a0, {val}", f"Carrega BOOL {node.valor}")
        elif node.tipo == 'STRING':
            lbl_str = self.new_label()
            self.data.append(f'{lbl_str}: .asciiz "{node.valor}"')
            self.emit(f"la $a0, {lbl_str}", "Carrega endereco da STRING")

    def visit_Identificador(self, node):
        # Usa a busca inteligente
        offset = self.lookup_offset(node.nome)
        self.emit(f"lw $a0, {offset}($fp)", f"Le variavel '{node.nome}'")

    def visit_ChamadaFuncao(self, node):
        # Implementação embutida para o comando print()
        if node.nome == "print":
            # Avalia o argumento (resultado vai para $a0)
            node.args[0].accept(self)
            
            # Syscall 1 imprime inteiros. 
            self.emit("li $v0, 1", "Syscall: Print Integer")
            self.emit("syscall")
            
            # Imprime quebra de linha
            self.emit("la $a0, newline", "Carrega '\\n'")
            self.emit("li $v0, 4", "Syscall: Print String")
            self.emit("syscall")