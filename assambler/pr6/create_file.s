.data
filename:   .string "F:/Работа/вуз/Vuz-raboti/assambler/pr6/random_numbers.txt"    # ПУТЬ ФАЙЛА
array_size: .word 25                        # Размер массива
array:      .space 100                      # Массив случайных чисел (25 чисел по 4 байта)
new_line:    .string  "\n"

.text
.globl _start

# SysCalls https://github.com/TheThirdOne/rars/wiki/Environment-Calls

_start:
    # Генерация случайных чисел и запись их в массив
    li      t0, 25           # Количество чисел для генерации
    la      t1, array        # Указатель на начало массива
    
    # Создание файла
    li      a7, 1024
    la      a0, filename
    li      a1, 1
    ecall
    mv      s0, a0
    
    

generate_random_loop:
    li      a7, 41           # Системный вызов RandInt
    li      a0, 1            # Флаг для генерации одного случайного числа
    ecall

    li      a7, 1
    ecall                    # PrintInt

    sw      a0, 0(t1)        # Запись случайного числа в массив
    
    li      a7, 4
    la      a0, new_line
    ecall
    
    addi    t1, t1, 4        # Переход к следующему элементу массива
    addi    t0, t0, -1       # Уменьшение счетчика
    bnez    t0, generate_random_loop

    # Запись массива в файл
    mv      a0, s0           # Файловый дескриптор
    la      a1, array        # Указатель на данные для записи
    li      a2, 100          # Размер данных (25 * 4 байта)
    li      a7, 64           # Системный вызов write
    ecall

    # Закрытие файла
    mv      a0, s0           # Файловый дескриптор
    li      a7, 57           # Системный вызов close
    ecall

    # Завершение программы
    li      a7, 93           # Системный вызов exit
    li      a0, 0            # Код завершения программы
    ecall
