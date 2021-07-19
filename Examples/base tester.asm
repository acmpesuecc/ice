extern _printf
global _main

segment .data
_p: db `%u\n`, 0

segment .bss
v_var: resd 1
v_arg: resd 1
v_dest: resd 1
v_sum: resb 1
v_h: resb 1
v_i: resb 1

segment .text
_main:

;4: arg = 355
mov dword [v_arg], 355

;6: 5dest = var - arg
mov eax, dword [v_var]
sub eax, dword [v_arg]
mov dword [v_dest], eax

;8: h = 9
mov byte [v_h], 9

;9: i = 246
mov byte [v_i], 246

;11: 3sum = h+i
mov  al, byte [v_h]
add  al, byte [v_i]
mov byte [v_sum],  al

;13: print(sum)
xor eax, eax
xor  al, byte [v_sum]
push eax
push _p
call _printf
add esp, 8

;14: print(dest)
xor eax, eax
xor eax, dword [v_dest]
push eax
push _p
call _printf
add esp, 8
