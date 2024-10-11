.globl __start


.data
  maxItem:          .word -1000
  indexColMaxItem:  .word 0
  indexRowMaxItem:  .word 0
  minItem:          .word 1000
  currentRow:       .word 0


.bss
  array:            .zero 35  ; 7*5 по 1 байту


.rodata
  O_READONLY:       .word 0b0000001
  path:             .string "output.txt"
  size_arr:         .word  35  ; 7*5
  N:                .word 5  ; колонки
  M:                .word 7  ; строки
  item_msg:         .string "Item is: "
  index_col_msg:    .string "Index column is: "
  index_row_msg:    .string "Index row is: "


.text


func:
  mv t1, a0 ; t1: адресс входного массива
  li t3, 0 ; текущая строка
  arr_row:
    lw t2, N
    li t4, 0 ; t4: текущий столбец
    arr_col:
      mv t5, t3 ; t5: смещение
      mul t5, t5, t2
      add t5, t5, t4

      mv t0, t1
      add t0, t0, t5
      lb t6, 0(t0) ; t6 - текущий элемент

      ; Сравнение текущего элемента с максимальным элементом строки
      la a1, maxItem
      lw t0, 0(a1)
      
      la a0, indexColMaxItem
      la a2, indexRowMaxItem
      
      blt t6, t0, not_max
      sw t6, 0(a1)
      sw t4, 0(a0)
      sw t3, 0(a2)

      not_max:

      addi t4, t4, 1
      blt t4, t2, arr_col
    
    la a1, currentRow
    sw t3, 0(a1)
    
    li t3, 0

    la a1, indexColMaxItem
    lw t4, 0(a1)

    check_min_by_index_max:
        mv t5, t3 ; t5: смещение
        mul t5, t5, t2
        add t5, t5, t4

        mv t0, t1
        add t0, t0, t5
        lb t6, 0(t0) ; t6 - текущий элемент
        
        ; проходимся по элемента столбца
        la a1, minItem
        lw t5, 0(a1)  
        
        bgt t6, t5, not_min
        sw t6, 0(a1)

        not_min:

        addi t3, t3, 1
        lw t0, M
        blt t3, t0, check_min_by_index_max
    
    lw t5, minItem
    lw t6, maxItem

    bne t5, t6, not_equal

    li a0, 4 ; 4 - вывод строки на экран
    la a1, item_msg
    ecall

    li a0, 1 ; 1 - вывод целых чисел
    lw a1, minItem
    ecall

    li a0, 11
    li a1, '\n'
    ecall
    
    li a0, 4 ; 4 - вывод строки на экран
    la a1, index_col_msg
    ecall

    li a0, 1 ; 1 - вывод целых чисел
    lw a1, indexColMaxItem
    ecall

    li a0, 11
    li a1, '\n'
    ecall
    
    li a0, 4 ; 4 - вывод строки на экран
    la a1, index_row_msg
    ecall

    li a0, 1 ; 1 - вывод целых чисел
    lw a1, indexRowMaxItem
    ecall

    li a0, 11
    li a1, '\n'
    ecall

    not_equal:
    
    lw t3, currentRow
    
    li t6, 0
    la a0, indexColMaxItem
    la a2, indexRowMaxItem
    sw t6, 0(a0)
    sw t6, 0(a2)
    
    li t6, -1000
    la a1, maxItem
    sw t6, 0(a1)
    
    la a1, minItem
    li t6, 1000
    sw t6, 0(a1)

    addi t3, t3, 1
    lw t0, M
    blt t3, t0, arr_row
  li a0, 11
  li a1, '\n'
  ecall
  ret
        
      
print_arr:
  mv t1, a0  ; t1: адресс входного массива
  li t3, 0  ; текущая строка
  print_arr_row:
    lw t2, N
    li t4, 0  ; t4: текущий столбец
    print_arr_col:
      mv t5, t3  ; t5: смещение
      mul t5, t5, t2
      add t5, t5, t4
      
      mv  t0, t1
      add t0, t0, t5
      lb t6, 0(t0)
  
      li a0, 1  ; вывод числа
      mv a1, t6
      ecall   
      li a0, 11
      li a1, ' '
      ecall
      
      addi t4, t4, 1
      blt t4, t2, print_arr_col
    
    li a0, 11  ; переход на следующую строку
    li a1, '\n'
    ecall

    addi t3, t3, 1
    lw t0, M
    blt t3, t0, print_arr_row
  li a0, 11
  li a1, '\n'
  ecall
  ret


__start:
  li a0, 13  ; 13 - open
  la a1, path
  lw a2, O_READONLY  ; только чтение
  ecall
  mv s0, a0  ; s0 - file descriptor
  
  li a0, 14  ; чтение
  mv a1, s0
  la a2, array
  lw a3, size_arr
  ecall

  la a0, array
  call print_arr
  
  la a0, array
  call func  ; задание
  
  li a0, 10
  ecall