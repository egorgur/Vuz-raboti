.data
filename:    .string "F:/Работа/вуз/Vuz-raboti/assambler/pr6/random_numbers.txt"  # ПУТЬ ФАЙЛА
buffer:      .space 100           # буфер для чтения данных из файла
matrix:      .space 100           # матрица (25 элементов по 4 байта)

.text
.global _start

# SysCalls https://github.com/TheThirdOne/rars/wiki/Environment-Calls

_start:
        # Открываем файл на чтение
        la a0, filename           # имя файла
        li a1, 0                  # режим чтения
        li a7, 1024               # syscall open
        ecall
        mv t0, a0                 # сохраняем файловый дескриптор

        # Читаем данные из файла в буфер
        mv a0, t0                 # дескриптор
        la a1, buffer             # адрес буфера
        li a2, 100                # сколько байт прочитать
        li a7, 63                 # syscall Read
        ecall

        # Закрываем файл
        mv a0, t0                 # файловый дескриптор
        li a7, 57                 # syscall close
        ecall

        # Преобразуем данные из буфера в матрицу
        la t1, buffer             # указатель на буфер
        li t2, 0                  # индекс строки
        li t3, 0                  # индекс столбца
        la t4, matrix             # указатель на матрицу

parse_buffer:
        # Если все данные считаны, продолжаем работу с матрицей
        li t5, 25                 # всего 25 элементов
        beq t2, t5, process_matrix

        lb t6, 0(t1)              # считываем элемент из буфера
        sb t6, 0(t4)              # сохраняем элемент в матрицу

        addi t1, t1, 4            # смещаем указатель буфера
        addi t4, t4, 4            # смещаем указатель матрицы
        addi t2, t2, 1            # увеличиваем индекс
        j parse_buffer

process_matrix:
        # Теперь матрица заполнена, выполняем замену элементов на 0 внутри ромба
        li t2, 0                  # счётчик строк
        li t3, 0                  # счётчик столбцов

iterate_rows:
        # Если все строки обработаны, выводим результат
        li t0, 5                  # размер матрицы 5x5
        beq t2, t0, print_matrix

        li t3, 0                  # обнуляем счётчик столбцов

iterate_cols:
        # Если все столбцы в строке обработаны, переходим к следующей строке
        beq t3, t0, next_row

        # Условие для обнуления
        add t4, t2, t3            # t4 = i + j
        li t5, 4                  # n - 1 (для побочной диагонали)
        beq t4, t5, skip_zero     # i + j == n - 1, не обнуляем
        beq t2, t3, skip_zero     # i == j, не обнуляем

        # Обнуляем элемент
        slli t6, t2, 2            # смещаем строку (t2 * 4)
        add t6, t6, t2            # t6 = t2 * 5 (адрес нужного элемента)
        add t6, t6, t3            # добавляем столбец (индекс элемента t2*5 + t3)
        slli t6, t6, 2            # умножаем на 4 (слово = 4 байта)
        la t5, matrix             # указатель на начало матрицы
        add t5, t5, t6            # получаем адрес элемента
        sb zero, 0(t5)            # записываем 0

skip_zero:
        addi t3, t3, 1            # переходим к следующему столбцу
        j iterate_cols

next_row:
        addi t2, t2, 1            # переходим к следующей строке
        j iterate_rows

print_matrix:
        li t2, 0                  # обнуляем счётчик строк

print_rows:
        beq t2, t0, exit          # если все строки выведены, завершение программы

        li t3, 0                  # обнуляем счётчик столбцов

print_cols:
        beq t3, t0, next_print_row

        slli t6, t2, 2            # смещаем строку (t2 * 4)
        add t6, t6, t2            # t6 = t2 * 5 (адрес нужного элемента)
        add t6, t6, t3            # добавляем столбец (индекс элемента t2*5 + t3)
        slli t6, t6, 2            # умножаем на 4 (слово = 4 байта)
        la t1, matrix             # указатель на начало матрицы
        add t1, t1, t6            # получаем адрес элемента
        lb a0, 0(t1)              # загружаем элемент
        li a7, 1                  # syscall 1 - вывод числа
        ecall

        li a0, ' '                # вывод пробела
        li a7, 11                 # syscall 11 - вывод символа
        ecall

        addi t3, t3, 1            # переходим к следующему столбцу
        j print_cols

next_print_row:
        li a0, 10                 # вывод новой строки
        li a7, 11                 # syscall 11 - вывод символа
        ecall

        addi t2, t2, 1            # переходим к следующей строке
        j print_rows

exit:
        li a7, 10                 # syscall 10 - завершение программы
        ecall


