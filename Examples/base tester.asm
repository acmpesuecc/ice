extern _printf
global _main

segment .bss
$var: resd 1
$arg: resd 1
$dest: resd 1
$sum: resb 1
$h: resb 1
$i: resb 1

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0

segment .text
_main:

;4: arg = 355
mov dword [$arg], 355

;6: 5dest = var - arg
mov eax, dword [$var]
sub eax, dword [$arg]
mov dword [$dest], eax

;8: h = 9
mov byte [$h], 9

;9: i = 246
mov byte [$i], 246

;11: 3sum = h+i
mov  al, byte [$h]
add  al, byte [$i]
mov byte [$sum],  al

;15: printnum(sum)
xor eax, eax
xor  al, byte [$sum]
push eax
push _p
call _printf
add esp, 8

;16: printnum(dest)
xor eax, eax
xor eax, dword [$dest]
push eax
push _p
call _printf
add esp, 8
