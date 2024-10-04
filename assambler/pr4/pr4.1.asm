format PE Console 

entry start        

include 'win32a.inc' 

;=======================================================
section '.data' data readable writeable
;=======================================================

        struct ticket
            destiny db 30 dup(0)     ; Поле для хранения пункта назначения (30 символов)
            starting db 30 dup(0)    ; Поле для хранения начального пункта (30 символов)
            date db 30 dup(0)        ; Поле для хранения даты (30 символов)
            cost dd 0                ; Поле для хранения стоимости (4 байта)
        ends

        ; Пустые билеты для последующего заполнения
        tickets ticket ?,?,?,? 
                ticket ?,?,?,? 
                ticket ?,?,?,? 
                ticket ?,?,?,? 
                ticket ?,?,?,? 

        string_input db '%s',0       ; Форматная строка для ввода строк
        int_output db '%d',10,0      ; Форматная строка для вывода чисел
        struct_output db '%s, %s, %s, %d',10,0  ; Форматная строка для вывода билетов

        n dd 5                       ; Количество билетов
        size_of dd 94                ; Размер структуры одного билета
        i dd 0                       ; Индекс для итерации по билетам

        read_file_name db 'in',0     ; Имя файла для чтения (in)
        write_file_name db 'out',0   ; Имя файла для записи (out)
        w_mode db 'w',0              ; Режим записи файла
        r_mode db 'r',0              ; Режим чтения файла
        read_file_descriptor dd 0    ; Дескриптор файла для чтения
        write_file_descriptor dd 0   ; Дескриптор файла для записи
        size dd 0                    ; Переменная для хранения размера при итерации

;=======================================================
section '.code' code readable writeable executable
;=======================================================

start:
        invoke fopen, read_file_name, r_mode
        ; Открытие файла для чтения ('in' в режиме 'r')

        mov [ds:read_file_descriptor], eax
        ; Сохранение дескриптора файла для чтения

        mov eax, [ds:n]
        ; Загрузка количества билетов в регистр EAX

        imul [ds:size_of]
        ; Умножение количества билетов на размер одного билета для вычисления общего объема данных

        mov ecx, 1
        ; Устанавливаем количество объектов для чтения в 1

        invoke fread, tickets, ecx, eax, [ds:read_file_descriptor]
        ; Чтение билетов из файла в структуру tickets

        invoke fclose, [ds:read_file_descriptor]
        ; Закрытие файла для чтения

        invoke fopen, write_file_name, w_mode
        ; Открытие файла для записи ('out' в режиме 'w')

        mov [ds:write_file_descriptor], eax
        ; Сохранение дескриптора файла для записи

        mov [ds:i], 0
        ; Инициализация переменной индекса i для цикла

        looop2:
                mov eax, [ds:i]
                ; Загрузка текущего индекса в EAX

                imul [ds:size_of]
                ; Умножение индекса на размер структуры билета для перехода к нужному билету

                mov edx, eax
                add edx, tickets.cost
                ; Переход к полю стоимости билета

                push eax
                mov eax, 99
                ; Загрузка значения 99 для увеличения стоимости билета

                add eax, [edx]
                ; Увеличение стоимости билета на 99

                mov [edx], eax
                ; Сохранение нового значения стоимости

                pop eax

                inc [ds:i]
                ; Увеличение индекса i

                mov edx, [ds:i]
                cmp edx, 5
                ; Проверка, если все 5 билетов обработаны, выход из цикла

                jne looop2
                ; Если не все, переход к следующей итерации

        ; После обновления стоимости билетов, вывод данных на экран:

        mov eax, [ds:n]
        ; Загрузка количества билетов в регистр EAX

        imul [ds:size_of]
        ; Вычисление общего размера данных для записи

        mov ecx, 1
        ; Количество объектов для записи

        mov [ds:i], 0
        ; Инициализация индекса i для второго цикла

        looop:
                mov eax, [ds:i]
                imul [ds:size_of]
                mov [ds:size], eax
                ; Вычисление смещения для текущего билета

                mov ebx, [ds:size]
                add ebx, tickets.destiny
                ; Получение адреса пункта назначения текущего билета

                mov ecx, [ds:size]
                add ecx, tickets.starting
                ; Получение адреса начального пункта текущего билета

                add eax, tickets.date
                ; Получение адреса даты текущего билета

                mov edx, [ds:size]
                add edx, tickets.cost
                ; Получение адреса стоимости текущего билета

                invoke printf, struct_output, ebx, ecx, eax, [edx]
                ; Вывод информации о билете на экран (пункт назначения, начальный пункт, дата, стоимость)

                inc [ds:i]
                ; Увеличение индекса i

                mov edx, [ds:i]
                cmp edx, 5
                ; Проверка, если все 5 билетов обработаны, выход из цикла

                jne looop
                ; Если не все, переход к следующей итерации

        ; Запись измененных данных билетов обратно в файл:

        invoke fwrite, tickets, ecx, [ds:size], [ds:write_file_descriptor]
        ; Запись обновленных билетов в файл

        invoke fclose, [ds:write_file_descriptor]
        ; Закрытие файла для записи

        invoke getch
        ; Ожидание нажатия клавиши (пауза программы)

        invoke ExitProcess, 0
        ; Завершение программы

;=======================================================
section '.idata' data import readable
;=======================================================

  library kernel, 'kernel32.dll',\
                msvcrt, 'msvcrt.dll'

  import kernel,\
         ExitProcess, 'ExitProcess'

  import msvcrt,\
          printf, 'printf',\
          getch, '_getch', scanf, 'scanf', fopen, 'fopen', fwrite, 'fwrite', fclose, 'fclose', fread, 'fread'
  
