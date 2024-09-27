format PE console

entry start

include 'win32ax.inc'

;=======================================================
section '.data' data readable writeable
;=======================================================
matrix db 5, 0, 1, 5 ; Матрица, заданная в коде. 
       db 3, 4, 2, 4 ; Размер матрицы 4x4 (4 строки, 4 столбца).
       db 5, 8, 6, 0
       db 1, 2, 1, 0

matrix_rows equ 4      ; Количество строк матрицы.
matrix_cols equ 4      ; Количество столбцов матрицы.
n dd 3                 ; Переменная для итераций по строкам (n = 3).
m dd 3                 ; Переменная для итераций по столбцам (m = 3).

;=======================================================
section '.text' code readable executable
;=======================================================
start:

;==================== Поиск строк =====================

row:
mov esi, 0             ; Инициализация счетчика строк (i = 0).
mov edi, 0             ; Инициализация счетчика столбцов (j = 0).
mov ebp, 1             ; Инициализация вспомогательного счетчика для сравнения (k = 1).
mov edx, 0             ; Счетчик количества строк с одинаковыми элементами.

loop_i_row:
        ; Получаем элемент строки (matrix[i][j]).
        mov eax, esi
        imul eax, matrix_cols
        add eax, edi 
        movzx ebx, byte [matrix + eax]

loop_j_row:
        ; Получаем следующий элемент для сравнения.
        mov eax, esi
        imul eax, matrix_cols
        add eax, ebp
        movzx ecx, byte [matrix + eax]   ; Загружаем элемент matrix[i][k] в ecx.
        cmp ebx, ecx                     ; Сравниваем элементы.
        jne unequal_row                  ; Если элементы различны, переход.
        inc edx                          ; Увеличиваем счетчик одинаковых строк.
        jmp next_row                     ; Переходим к следующей строке.

unequal_row:
        cmp ebp, [m]                     ; Проверяем, достигнут ли конец строки.
        jae equals_row                   ; Если да, проверяем строку на уникальность.
        inc ebp                          ; Увеличиваем счетчик сравниваемых элементов.
        jmp loop_j_row                   ; Продолжаем цикл по столбцам.

equals_row:
        mov eax, [m]                     ; Проверка, все ли столбцы пройдены.
        cmp edi, eax
        jae next_row
        inc edi
        cmp edi, eax
        jae next_row
        mov ebp, edi
        inc ebp
        jmp loop_i_row

next_row:
        mov eax, [n]                     ; Проверка, все ли строки пройдены.
        cmp esi, eax
        jae print_count_row
        inc esi
        mov edi, 0
        mov ebp, 1
        jmp loop_i_row

print_count_row:
        ; Печать количества строк с уникальными элементами.
        mov eax, [n]
        sub eax, edx
        inc eax
        cinvoke printf, "%d row ", eax   ; Вывод количества уникальных строк.

col:
        mov esi, 0                       ; Инициализация счетчика строк (i = 0).
        mov edi, 0                       ; Инициализация счетчика столбцов (j = 0).
        mov ebp, 1                       ; Инициализация вспомогательного счетчика (k = 1).
        mov edx, 0                       ; Счетчик количества столбцов с одинаковыми элементами.

loop_i_col:
        ; Получаем элемент столбца (matrix[i][j]).
        mov eax, esi
        imul eax, matrix_cols
        add eax, edi
        movzx ebx, byte [matrix + eax]

loop_j_col:
        ; Получаем следующий элемент столбца для сравнения.
        mov eax, ebp
        imul eax, matrix_cols
        add eax, edi
        movzx ecx, byte [matrix + eax]   ; Загружаем элемент matrix[k][j] в ecx.
        cmp ebx, ecx                     ; Сравниваем элементы.
        jne unequal_col                  ; Если элементы различны, переход.
        inc edx                          ; Увеличиваем счетчик одинаковых столбцов.
        jmp next_col                     ; Переход к следующему столбцу.

unequal_col:
        cmp ebp, [n]                     ; Проверяем, достигнут ли конец столбца.
        jae equals_col
        inc ebp
        jmp loop_j_col

equals_col:
        mov eax, [n]                     ; Проверка, все ли строки пройдены.
        cmp esi, eax
        jae next_col
        inc esi
        cmp esi, eax
        jae next_col
        mov ebp, esi
        inc ebp
        jmp loop_i_col

next_col:
        mov eax, [m]                     ; Проверка, все ли столбцы пройдены.
        cmp edi, eax
        jae print_count_col
        inc edi
        mov esi, 0
        mov ebp, 1
        jmp loop_i_col

print_count_col:
        ; Печать количества столбцов с уникальными элементами.
        mov eax, [m]
        sub eax, edx
        inc eax
        cinvoke printf, "%d col", eax   ; Вывод количества уникальных столбцов.

invoke getch                             ; Ожидание нажатия клавиши.
invoke ExitProcess, 0                    ; Завершение программы.

;=======================================================
section '.idata' import readable writable
;=======================================================
library kernel32, 'KERNEL32.DLL',\
user32, 'USER32.DLL',\
msvcrt, 'msvcrt.dll'

include 'api\kernel32.inc'
include 'api\user32.inc'
import msvcrt, printf, 'printf', \
scanf, 'scanf', getch, '_getch'