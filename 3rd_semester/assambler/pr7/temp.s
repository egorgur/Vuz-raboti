    .data
input_str:   .asciz "Hello World from ARM"  @ Входная строка для теста
buffer:      .space 100                      @ Буфер для изменения строки

    .text
    .global _start

_start:
    LDR R0, =input_str                       @ Загружаем адрес строки в R0
    LDR R1, =buffer                          @ Загружаем адрес буфера в R1
    BL remove_first_word                     @ Удаляем первое слово
    BL to_lower_case                         @ Преобразуем оставшуюся строку в нижний регистр

    MOV R7, #4                               @ Системный вызов write для вывода строки
    MOV R0, #1                               @ Дескриптор stdout
    LDR R1, =buffer                          @ Адрес буфера с результирующей строкой
    MOV R2, #100                             @ Длина буфера
    SVC #0

    MOV R7, #1                               @ Системный вызов выхода
    MOV R0, #0
    SVC #0

remove_first_word:
    LDRB R2, [R0], #1                        @ Читаем байт и продвигаем указатель
check_space:
    CMP R2, #' '                             @ Проверка на пробел
    BEQ start_copy                           @ Если пробел, начинаем копировать
    LDRB R2, [R0], #1                        @ Если не пробел, читаем следующий байт
    B check_space

start_copy:
copy_loop:
    LDRB R2, [R0], #1                        @ Читаем байт и продвигаем указатель
    STRB R2, [R1], #1                        @ Копируем байт в буфер и продвигаем указатель
    CMP R2, #0                               @ Проверка на конец строки
    BNE copy_loop
    BX LR

to_lower_case:
    LDR R1, =buffer                          @ Адрес буфера
lower_loop:
    LDRB R2, [R1]                            @ Читаем байт
    CMP R2, #0                               @ Проверка на конец строки
    BEQ end_lower                            @ Если конец строки, выходим
    CMP R2, #'A'                             @ Проверяем, если символ >= 'A'
    BLT next_char                            @ Если меньше, переходим к следующему символу
    CMP R2, #'Z'                             @ Проверяем, если символ <= 'Z'
    BGT next_char                            @ Если больше, переходим к следующему символу
    ADD R2, R2, #32                          @ Преобразуем в нижний регистр
    STRB R2, [R1]                            @ Записываем измененный байт
next_char:
    ADD R1, R1, #1                           @ Переходим к следующему символу
    B lower_loop
end_lower:
    BX LR
