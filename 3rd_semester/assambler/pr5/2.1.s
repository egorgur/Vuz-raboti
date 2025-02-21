.section .data

input_a:
    .asciiz "Input A\n"
input_x:
    .asciiz "Input X\n"
new_line:
    .asciiz "\n"
    
print_y1:
    .asciiz "Y1 = "
print_y2:
    .asciiz ", Y2 = "
print_y:
    .asciiz "Y = "
  
.section .text
    .global __start


__start:
    # Напечатать строку 
    li a0, 4
    la a1, input_a
    ecall
    
    # Ввод int
    li a0, 5
    ecall
    
    # Переместить А в t1
    mv t1, a0
    
    # Напечатать строку
    li a0, 4
    la a1, input_x
    ecall
    
    # Ввод int
    li a0, 5
    ecall
    
    # Переместить X в t2
    mv t2, a0
    
    # Индекс
    li t0, 0

loop:
    # Если X больше 1 то по метке
    li t5, 1
    mv t6, t2
    blt t5, t2, over_than_one
    bge t2, zero, make_pos
    neg t6, t2
    make_pos: 
        add s2, t6, t1
    j continue


    
over_than_one:
    # Сделать x + 10 и положить в s2 (Y1)
    li t5, 10
    add s2, t2, t5
 

   
      
continue:
 
    li t5, 4
    # если x больше 4 то по метке
    blt t5, t2, over_than_four
    
    
    # Положить в s3 t2 (x в Y2)
    mv s3, t2
    j result
  
over_than_four:
    # положить 2 в s3 (Y2)
    li s3, 2
  
  
result:
    # Вывести строку
    li a0, 4
    la a1, print_y1
    ecall
    
    # Вывести s2 - Y1
    li a0, 1
    mv a1, s2
    ecall
    
    # Вывести строку
    li a0, 4
    la a1, print_y2
    ecall
    
    # Вывести s3 - Y2
    li a0, 1
    mv a1, s3
    ecall
    
    # Вывести \n
    li a0, 4
    la a1, new_line
    ecall
    
    # остаток от деления s2 на s3 и положить в s4 (Y = Y1 % Y2)
    rem s4, s2, s3
    
    # Вывести строку 
    li a0, 4
    la a1, print_y
    ecall
    
    # Вывести s4 - Y
    li a0, 1
    mv a1, s4
    ecall
    
    # Вывести \n
    li a0, 4
    la a1, new_line
    ecall
    
    # Увеличить X на 1
    addi t2, t2, 1
    # Положить 9 в t4
    li t4, 9
    # Увеличить индекс
    addi t0, t0, 1
    # Если индекс не равен 9 - перейти на loop
    bne t0, t4, loop
    
    # Завершение программы
    li a0, 10
    ecall  