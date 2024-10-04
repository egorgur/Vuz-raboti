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

        ; Определение нескольких билетов с конкретными значениями
        tickets ticket 'to1','from1','date1',100
                ticket 'to2','from2','date2',110
                ticket 'to3','from3','date3',120
                ticket 'to4','from4','date4',130
                ticket 'to5','from5','date5',140

        string_input db '%s',0       ; Форматная строка для ввода строк
        int_output db '%d',15,0      ; Форматная строка для вывода чисел
        n dd 5                       ; Количество билетов
        size_of dd 94                ; Размер структуры одного билета

        write_file_name db 'in',0    ; Имя файла для записи (in)
        w_mode db 'w',0              ; Режим записи файла
        file_d dd 0                  ; Дескриптор файла

;=======================================================
section '.code' code readable writeable executable
;=======================================================
; Секция кода программы

start:
        invoke fopen, write_file_name, w_mode
        ; Открытие файла 'in' в режиме записи

        mov [ds:file_d], eax
        ; Сохранение дескриптора файла в переменной file_d

        mov eax, [ds:n]
        ; Загружаем количество билетов в регистр EAX

        imul [ds:size_of]
        ; Умножаем количество билетов на размер одного билета, чтобы получить общий размер данных для записи

        mov ecx, 1
        ; Устанавливаем ECX в 1 для передачи количества объектов (структур) fwrite

        invoke fwrite, tickets, ecx, eax, [ds:file_d]
        ; Запись структуры билетов в файл

        invoke fclose, [ds:file_d]
        ; Закрытие файла

        invoke getch
        ; Ожидание нажатия клавиши (пауза программы)

        invoke ExitProcess, 0
        ; Завершение работы программы

;=======================================================
section '.idata' data import readable
;=======================================================

  library kernel, 'kernel32.dll',\
                msvcrt, 'msvcrt.dll'

  import kernel,\
         ExitProcess, 'ExitProcess'

  import msvcrt,\
          printf, 'printf',\
          getch, '_getch', scanf, 'scanf', fopen, 'fopen', fwrite, 'fwrite', fclose, 'fclose'
  
