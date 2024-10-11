.globl __start            
  
.rodata
  O_RDWR:    .word 0b0000100  ; 4
  O_CREAT:   .word 0b0100000  ; 64
  path:      .string "output.txt"
  ; array:     .byte 23, 4, 20, 13, 17, 27, 11, 21, 3, 9, 25, 18, 31, 1, 7, 10, 14, 26, 19, 16, 2, 24, 6, 35, 12, 34, 29, 32, 5, 33, 8, 15, 22, 28, 30
  array:     .byte 11, 7, 8, 9, 15, 12, 2, 3, 4, 13, 12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35
  size_arr:  .word  35 # 7*5

.text
__start:
  li a0, 13  ; 13 - open
  la a1, path
  lw a2, O_RDWR
  lw t0, O_CREAT
  or a2, a2, t0  ; a2 = O_RDWR | O_CREAT
  ecall  ; открытие: путь, флаги открытия
  mv s0, a0  ; s0 - file descriptor

  li a0, 15  ; 15 - write
  mv a1, s0
  la a2, array
  lw a3, size_arr
  ecall  ; запись: дескриптор, что записывать, сколько записывать

  li a0, 16  ; 16 - close file
  mv a1, s0
  ecall  ; закрытие: дескриптор

  li a0, 10
  ecall
  