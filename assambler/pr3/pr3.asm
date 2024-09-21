format PE Console
entry start
include 'win32a.inc'

;=================================================
section '.data' data readable writeable
;=================================================

        input_n db 'Enter number of columns: ',0
        input_m db 'Enter number of rows: ',0
        input_item db 'Enter a[%d][%d]: ',0
        scan_int db '%d',0
        output_matrix db 'Final matrix:',0
        output_int_matrix db '%4d ',0
        output_max db 'Maximum item occuring more than once: %d',0
        newline db 10,0

        n dd 0
        m dd 0
        len dd 0
        matrix dd 100 dup(0)
        count dd 100 dup(0)

        i dd 0
        j dd 0
        k dd 0
        kk dd 0
        c dd 0
        max dd 0
        temp dd 0

;=================================================
section '.code' code readable writeable executable
;=================================================

start:
        invoke printf, input_n
        invoke scanf, scan_int, n
        invoke printf, input_m
        invoke scanf, scan_int, m
        invoke printf, newline

        mov eax, [n]
        imul eax, [m]
        mov [len], eax
        cmp [len], 0
        jle exit
        cmp [len], 100
        ja exit

        ; for i in (1:m) for j in (1:n)
        lea esi, [matrix]
        for_input_row:
                mov eax, [k]
                cmp eax, [len]
                je for_input_end

                mov eax, [i]
                inc eax
                mov [i], eax
                mov [j], 0
                for_input_item:
                        mov eax, [j]
                        inc eax
                        mov [j], eax
                        for_input_again:
                        invoke printf, input_item, [i], [j]
                        invoke scanf, scan_int, temp

                        cmp [temp], 1
                        jl for_input_again
                        cmp [temp], 99
                        ja for_input_again

                        mov eax, [temp]
                        mov [esi], eax
                        add esi, 4

                        mov eax, [k]
                        inc eax
                        mov [k], eax

                        mov eax, [j]
                        cmp eax, [n]
                        je for_input_row
                        jmp for_input_item

for_input_end:
        invoke printf, newline
        ; matrix output
        invoke printf, output_matrix
        lea esi, [matrix]
        mov [j], 0
        mov [k], 0
        for_output_row:
                mov eax, [k]
                cmp eax, [len]
                je for_output_end

                mov [j], 0
                invoke printf, newline
                for_output_item:
                        mov eax, [j]
                        inc eax
                        mov [j], eax
                        
                        invoke printf, output_int_matrix, [esi]
                        add esi, 4

                        mov eax, [k]
                        inc eax
                        mov [k], eax

                        mov eax, [j]
                        cmp eax, [n]
                        je for_output_row
                        jmp for_output_item

for_output_end:
        invoke printf, newline
        invoke printf, newline
        ; find max
        mov [k], 0
        lea esi, [matrix]
        for_fill_count:
                mov eax, [esi]
                imul eax, 4
                add eax, count
                mov ebx, [eax]
                inc ebx
                mov [eax], ebx

                mov eax, [k]
                inc eax
                mov [k], eax
                add esi, 4
                mov eax, [k]
                cmp eax, [len]
                jl for_fill_count
        
        mov [k], 0
        lea esi, [matrix]
        for_find_max:
                mov eax, [esi]
                imul eax, 4
                add eax, count
                mov ebx, [eax]
                cmp ebx, 1
                jle for_find_max_skip
                mov eax, [esi]
                cmp eax, [max]
                jle for_find_max_skip
                mov [max], eax
        for_find_max_skip:
                mov eax, [k]
                inc eax
                mov [k], eax
                add esi, 4
                mov eax, [k]
                cmp eax, [len]
                jl for_find_max
                
        invoke printf, output_max, [max]

exit:
        invoke getch
        invoke ExitProcess, 0

;=================================================
section '.idata' data import readable
;=================================================

        library kernel, 'kernel32.dll',\
                msvcrt, 'msvcrt.dll'
  
        import kernel,\
                ExitProcess, 'ExitProcess'
          
        import msvcrt,\
                printf, 'printf',\
                getch, '_getch',\
                scanf, 'scanf'