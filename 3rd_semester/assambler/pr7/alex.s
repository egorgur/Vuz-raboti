.text

@ Input string via stdin
mov r0, #1
ldr r1, =CharArray
mov r2, #80
swi 0x6a

@ Print help string for stdout
mov r0, #1
ldr r1, =lower_str
swi 0x69

ldr r2, =CharArray
mov r4, #0 @ Total words len
mov r5, #1 @ Toggle 1 if previous char was space | 0 if previous char not a space

find_space:
    ldrb r6, [r2], #1
    cmp r6, #0 @ проверка, является ли текущий символ концом строки
    beq row_end

    cmp r6, #' ' @ сравнение с ASCII-кодом пробела
    beq space_found

    b find_space

space_found:
    @ Указатель начала строки смещается на следующий символ после пробела
    add r2, r2, #0

check_char:
    ldrb r6, [r2], #1
    cmp r6, #0 @ проверка, является ли текущий символ концом строки
    beq row_end

    cmp r6, #'A' @ сравнение с ASCII-кодом заглавной буквы 'A'
    blt not_uppercase @ если символ не заглавная буква, пропустить
    cmp r6, #'Z' @ сравнение с ASCII-кодом заглавной буквы 'Z'
    bgt not_uppercase @ если символ не заглавная буква, пропустить
    sub r6, r6, #'A' - 'a' @ конвертация в нижний регистр

not_uppercase:
    add r4, r4, #1

    ldr r8, =Char_output
    str r6, [r8] @ сохранение символа в памяти

    mov r0, #1
    ldr r1, =Char_output @ печать текущего символа из памяти
    swi 0x69

    b check_char

row_end:
    @ output blank line 

    mov r0, #1
    ldr r1, =blank_line
    swi 0x69

swi 0x11

.data
CharArray: .asciz "Hello World, This is a sample sentence."
Char_output: .skip 10
symbol_space_output: .asciz " "
blank_line: .asciz "\n"
lower_str: .asciz "String with all lowercase letters:\n"