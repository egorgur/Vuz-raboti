.data
    prompt_a:  .string "Enter A: "
    prompt_x:  .string "Enter X: "
    result_1:  .string "Y for X = "
    result_2:  .string " is: "
    new_line:  .string "\n"
.text
.globl _start

_start:
    # Получаем значение A
    la   a0, prompt_a          # Загружаем строку запроса в a0
    li   a7, 4                 # Системный вызов write
    ecall                      # Вызов ядра для вывода
    li   a7, 5                 # Системный вызов read integer
    ecall                      # Чтение целого числа A
    mv   s0, a0                # Сохраняем A в s0

    # Получаем значение X
    la   a0, prompt_x          # Загружаем строку запроса в a0
    li   a7, 4                 # Системный вызов write
    ecall                      # Вызов ядра для вывода
    li   a7, 5                 # Системный вызов read integer
    ecall                      # Чтение целого числа X
    mv   s1, a0                # Сохраняем начальный X в s1
    
    #-------------# Сохранили старый Х для сравнения
    mv   s2, a0                
    #-------------#

loop:
    # y1 = 10 + X если X > 1, иначе y1 = |X| + A
    mv   t0, s1                # Копируем X в t0
    li   t1, 1                 # t1 = 1
    blt  t0, t1, calc_y1_abs   # Если X <= 1, переходим к |X| + A
    li   t1, 10                # t1 = 10
    add  t2, t1, s1            # t2 = 10 + X
    j    calc_y2               # Переходим к вычислению y2

calc_y1_abs:
    mv   t0, s1                # Копируем X в t0
    blt  t0, zero, negate_x    # Если X < 0, делаем его положительным
    add  t2, s1, s0            # t2 = |X| + A
    j    calc_y2

negate_x:
    neg  t0, t0                # Делаем X положительным
    add  t2, t0, s0            # t2 = |X| + A

calc_y2:
    # y2 = 2 если X > 4, иначе y2 = X
    li   t1, 4                 # t1 = 4
    blt  s1, t1, set_y2_x      # Если X <= 4, y2 = X
    li   t3, 2                 # t3 = 2
    j    calc_y

set_y2_x:
    mv   t3, s1                # y2 = X

calc_y:
    # Y = y1 % y2
    rem  t4, t2, t3            # t4 = y1 % y2

    # Вывод результата ===============================================
    la   a0, result_1          # Загружаем половину строки результата
    li   a7, 4                 # Системный вызов write
    ecall                      # Выводим результат


    mv   a0, s1	               # Переменная Х
    li   a7, 1                 # Системный вызов write
    ecall                      # Выводим результат
    
    la   a0, result_2          # Загружаем is:
    li   a7, 4                 # Системный вызов write
    ecall                      # Выводим результат
    
    
    mv   a0, t4                # Второй аргумент - Y
    li   a7, 1                 # Системный вызов write
    ecall                      # Выводим результат
 
    la   a0, result_2          # Загружаем is:
    li   a7, 4                 # Системный вызов write
    ecall                      # Выводим результат
    
    la   a0, new_line          # Загружаем is:
    li   a7, 4                 # Системный вызов write
    ecall                      # Выводим результат
    # ================ ===============================================

    # Увеличиваем X на 1
    li   t0, 1                 # t5 = 1
    add  s1, s1, t0            # Увеличиваем X на 1

    # Проверяем, достигли ли X + 9
    li   t5, 10                 # t5 = 9
    add  t6, s2, t5            # t6 = X + 9
    blt  s1, t6, loop          # Повторяем, если X <= X + 9

    # Завершение программы
    li   a7, 93                # Системный вызов для завершения
    ecall                      # Завершаем программу
