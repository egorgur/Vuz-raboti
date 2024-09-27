format PE console 4.0

entry start

include 'win32a.inc'

; Определение размера буфера для ввода строки
define  string_buf  512

;=======================================================
section '.data' data readable writable
;=======================================================

        char_print         db   '%c', 0                     ; Формат для вывода символа
        msg_string         db   'Enter string: ', 10, 0     ; Сообщение для пользователя при запросе строки
        input_string       db   string_buf dup(0)           ; Буфер для хранения введенной строки
        offset_long_word   dd   0                           ; Смещение самого длинного слова в строке
        len_string         dd   0                           ; Длина строки

;=======================================================
section '.code' code readable executable
;=======================================================


; Процедура для поиска самого длинного слова в строке
find_long_word:
    cld ; DL = 0                ; Очищаем флаг направления для корректного движения по строке
    mov   ax, ds                ; Сохраняем сегмент данных в ES
    mov   es, ax 
    lea   edi, [input_string]   ; Загружаем адрес строки в регистр EDI
    mov   al, 0                 ; Устанавливаем значение AL в 0 для поиска конца строки (null-символа)
    mov   ecx, string_buf       ; Устанавливаем размер буфера ECX для поиска конца строки
    repnz scasb                 ; Ищем null-символ в строке

   
    mov   eax, string_buf       ; Рассчитываем длину строки
    sub   eax, ecx
    mov   [len_string], eax     ; Сохраняем длину строки
    mov   ecx, eax              ; Загружаем длину строки в ECX для дальнейшей работы
    mov   ebx, ecx              ; Сохраняем начальное значение ECX в EBX (нужно для расчета длины слов)
    mov   edx, 0                ; Инициализируем максимальную длину слова в EDX (пока 0)
    lea   edi, [input_string]   ; Снова загружаем адрес строки в EDI для начала поиска слов
    
    ; Цикл поиска слов
    find_word:
      mov   al,  32             ; Устанавливаем AL равным пробелу (код символа 32)
      repnz scasb               ; Ищем следующий пробел или конец строки
      mov   eax, ebx            ; Рассчитываем длину текущего слова
      sub   eax, ecx
      dec   eax 
      cmp   eax, edx            ; Сравниваем длину текущего слова с максимальной длиной (EDX)
      
      jle   skip_set_best_len   ; Если длина текущего слова меньше или равна, пропускаем обновление
      
      mov   edx, eax            ; Если длина больше, обновляем максимальную длину слова
      
      mov   eax, [len_string]   ; Сохраняем смещение для самого длинного слова
      sub   eax, ebx
      mov   [offset_long_word], eax


      skip_set_best_len:
      mov   ebx, ecx            ; Сохраняем текущее значение ECX в EBX для следующей итерации
      
      cmp   ecx, 0              ; Если конец строки не достигнут, продолжаем цикл
      jne   find_word 
      ret                       

; Процедура для вывода самого длинного слова
print_long_word:
    cld
    mov   eax, [offset_long_word]   ; Загружаем смещение самого длинного слова в EAX
    mov   eax, [offset_long_word]   ; Загружаем адрес самого длинного слова в ESI
    lea   esi, [input_string+eax] 
   
    mov   eax, [len_string]         ; Рассчитываем длину самого длинного слова
    sub   eax, [offset_long_word]
    mov   ecx, eax
    dec   ecx  

    ; Цикл для вывода каждого символа самого длинного слова
    print_each_symb:
      xor eax, eax                  ; Очищаем EAX и загружаем следующий символ в AL
      lodsb 
      
      cmp al,  32                   ; Если встретили пробел, завершаем вывод
      je end_print 
      push ecx                      ; Выводим символ на экран
      cinvoke printf, char_print, eax
      pop ecx
      loop print_each_symb          ; Переходим к следующему символу  

    end_print:
    ; Выводим символ новой строки
    mov   eax, 10
    cinvoke printf, char_print, eax  
    ret
    
; точка входа    
start:
    
    cinvoke printf, msg_string      ; Выводим сообщение для ввода строки
    cinvoke gets, input_string      ; Получаем ввод от пользователя
    call    find_long_word          ; Вызываем процедуру поиска самого длинного слова
    call    print_long_word         ; Вызываем процедуру вывода самого длинного слова  
    invoke getch                    ; Ожидание нажатия клавиши
    invoke ExitProcess, 0           ; Завершаем программу

;=======================================================
section '.idata' import data readable
;=======================================================
 
        library msvcrt,'MSVCRT.DLL',\
                kernel32,'KERNEL32.DLL'
 
        import kernel32,\
            ExitProcess, 'ExitProcess',\
               sleep,'Sleep'
 
        import msvcrt,\
               gets,'gets',\
               printf,'printf', \
               getch, '_getch'