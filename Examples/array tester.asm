extern _printf
global _main

segment .data
_p: db `%u\n`, 0

segment .bss
v_arr: resw 4
v_i: resb 1
v_e: resw 1
v_z: resb 1

segment .text
_main:

;3: i = 0
mov byte [v_i], 0

;4: arr[i] = 75
mov eax, 75
xor ecx, ecx
mov  cl, byte [v_i]
mov word [ecx * 2 + v_arr],  ax

;5: i = 1
mov byte [v_i], 1

;6: arr[i] = 80
mov eax, 80
xor ecx, ecx
mov  cl, byte [v_i]
mov word [ecx * 2 + v_arr],  ax

;7: i = 2
mov byte [v_i], 2

;8: arr[i] = 85
mov eax, 85
xor ecx, ecx
mov  cl, byte [v_i]
mov word [ecx * 2 + v_arr],  ax

;9: i = 3
mov byte [v_i], 3

;10: arr[i] = 90
mov eax, 90
xor ecx, ecx
mov  cl, byte [v_i]
mov word [ecx * 2 + v_arr],  ax

;12: i = 0
mov byte [v_i], 0

;13: e = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
mov word [v_e],  ax

;14: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;15: i = 1
mov byte [v_i], 1

;16: e = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
mov word [v_e],  ax

;17: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;18: i = 2
mov byte [v_i], 2

;19: e = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
mov word [v_e],  ax

;20: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;21: i = 3
mov byte [v_i], 3

;22: e = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
mov word [v_e],  ax

;23: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;24: e = 2
mov word [v_e], 2

;25: arr[e] = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
xor ecx, ecx
mov  cx, word [v_e]
mov word [ecx * 2 + v_arr],  ax

;27: 3z = 0
mov byte [v_z], 0

;29: print(z)
xor eax, eax
xor  al, byte [v_z]
push eax
push _p
call _printf
add esp, 8

;30: print(z)
xor eax, eax
xor  al, byte [v_z]
push eax
push _p
call _printf
add esp, 8

;32: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;33: e = arr[e]
mov  ax, word [v_e]
mov  ax, word [eax * 2 + v_arr]
mov word [v_e],  ax

;34: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;36: print(i)
xor eax, eax
xor  al, byte [v_i]
push eax
push _p
call _printf
add esp, 8

;37: i = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
mov byte [v_i],  al

;38: print(i)
xor eax, eax
xor  al, byte [v_i]
push eax
push _p
call _printf
add esp, 8
