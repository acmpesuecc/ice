extern _printf
global _main

segment .bss
v_mat: resd 35
v_e: resw 1
v_i: resb 1
v_z: resb 1

segment .data
_p: db `%u\n`, 0
_c: dw 0
v_arr: dw 75, 80, 85, 90

segment .text
_main:

;15: i = 0
mov byte [v_i], 0

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

;18: i = 1
mov byte [v_i], 1

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

;21: i = 2
mov byte [v_i], 2

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

;24: i = 3
mov byte [v_i], 3

;25: e = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
mov word [v_e],  ax

;26: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;27: e = 2
mov word [v_e], 2

;28: arr[e] = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
xor ecx, ecx
mov  cx, word [v_e]
mov word [ecx * 2 + v_arr],  ax

;30: 3z = 0
mov byte [v_z], 0

;32: print(z)
xor eax, eax
xor  al, byte [v_z]
push eax
push _p
call _printf
add esp, 8

;33: print(z)
xor eax, eax
xor  al, byte [v_z]
push eax
push _p
call _printf
add esp, 8

;35: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;36: e = arr[e]
mov  ax, word [v_e]
mov  ax, word [eax * 2 + v_arr]
mov word [v_e],  ax

;37: print(e)
xor eax, eax
xor  ax, word [v_e]
push eax
push _p
call _printf
add esp, 8

;39: print(i)
xor eax, eax
xor  al, byte [v_i]
push eax
push _p
call _printf
add esp, 8

;40: i = arr[i]
mov  al, byte [v_i]
mov  ax, word [eax * 2 + v_arr]
mov byte [v_i],  al

;41: print(i)
xor eax, eax
xor  al, byte [v_i]
push eax
push _p
call _printf
add esp, 8
