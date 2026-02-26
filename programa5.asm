.data
newline: .asciiz "\n"

.text
.globl main

main:
    addi $sp, $sp, -8        # Abre espaco para $fp e $ra
    sw $fp, 4($sp)           # Salva $fp antigo
    sw $ra, 0($sp)           # Salva retorno ($ra)
    move $fp, $sp            # Atualiza Frame Pointer
    li $a0, 10               # Carrega INT 10
    sw $a0, -4($fp)          # Guarda var 'x'
    addi $sp, $sp, -4        # Protege memoria da variavel local
    lw $a0, -4($fp)          # Le variavel 'x'
    li $v0, 1                # Syscall: Print Integer
    syscall                  
    la $a0, newline          # Carrega '\n'
    li $v0, 4                # Syscall: Print String
    syscall                  
    li $a0, 1                # Carrega INT 1
    addi $sp, $sp, -4        # Abre espaco na pilha
    sw $a0, 0($sp)           # Push $a0
    li $a0, 1                # Carrega INT 1
    lw $t1, 0($sp)           # Pop para $t1
    addi $sp, $sp, 4         # Restaura espaco na pilha
    seq $a0, $t1, $a0        # Igual
    beqz $a0, L_0            # Se falso, pula para ELSE
    li $a0, 20               # Carrega INT 20
    sw $a0, -8($fp)          # Guarda var 'x'
    addi $sp, $sp, -4        # Protege memoria da variavel local
    lw $a0, -8($fp)          # Le variavel 'x'
    li $v0, 1                # Syscall: Print Integer
    syscall                  
    la $a0, newline          # Carrega '\n'
    li $v0, 4                # Syscall: Print String
    syscall                  
    li $a0, 30               # Carrega INT 30
    sw $a0, -12($fp)         # Guarda var 'y'
    addi $sp, $sp, -4        # Protege memoria da variavel local
    lw $a0, -12($fp)         # Le variavel 'y'
    li $v0, 1                # Syscall: Print Integer
    syscall                  
    la $a0, newline          # Carrega '\n'
    li $v0, 4                # Syscall: Print String
    syscall                  
    j L_1                    # Pula para o FIM do IF
L_0:
L_1:
    lw $a0, -4($fp)          # Le variavel 'x'
    li $v0, 1                # Syscall: Print Integer
    syscall                  
    la $a0, newline          # Carrega '\n'
    li $v0, 4                # Syscall: Print String
    syscall                  
end_main:
    li $v0, 10               # Syscall: Exit
    syscall                  