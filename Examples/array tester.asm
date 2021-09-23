extern _printf
global _main

segment .bss
$mat: resd 35
$i: resb 1
$e: resw 1
$z: resb 1

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
$arr: dw 75, 80, 85, 90

segment .text
_main:

;6: i = 0
mov byte [$i], 0

;7: e = arr[i]
mov  al, byte [$i]
mov  ax, word [eax * 2 + $arr]
mov word [$e],  ax

;8: printnum(e)
xor eax, eax
xor  ax, word [$e]
push eax
push _p
call _printf
add esp, 8

;9: i = 1
mov byte [$i], 1

;10: e = arr[i]
mov  al, byte [$i]
mov  ax, word [eax * 2 + $arr]
mov word [$e],  ax

;11: printnum(e)
xor eax, eax
xor  ax, word [$e]
push eax
push _p
call _printf
add esp, 8

;12: i = 2
mov byte [$i], 2

;13: e = arr[i]
mov  al, byte [$i]
mov  ax, word [eax * 2 + $arr]
mov word [$e],  ax

;14: printnum(e)
xor eax, eax
xor  ax, word [$e]
push eax
push _p
call _printf
add esp, 8

;15: i = 3
mov byte [$i], 3

;16: e = arr[i]
mov  al, byte [$i]
mov  ax, word [eax * 2 + $arr]
mov word [$e],  ax

;17: printnum(e)
xor eax, eax
xor  ax, word [$e]
push eax
push _p
call _printf
add esp, 8

;18: e = 2
mov word [$e], 2

;19: arr[e] = arr[i]
mov  al, byte [$i]
mov  ax, word [eax * 2 + $arr]
xor ecx, ecx
mov  cx, word [$e]
mov word [ecx * 2 + $arr],  ax

;21: 3z = 0
mov byte [$z], 0

;23: printnum(z)
xor eax, eax
xor  al, byte [$z]
push eax
push _p
call _printf
add esp, 8

;24: printnum(z)
xor eax, eax
xor  al, byte [$z]
push eax
push _p
call _printf
add esp, 8

;26: printnum(e)
xor eax, eax
xor  ax, word [$e]
push eax
push _p
call _printf
add esp, 8

;27: e = arr[e]
mov  ax, word [$e]
mov  ax, word [eax * 2 + $arr]
mov word [$e],  ax

;28: printnum(e)
xor eax, eax
xor  ax, word [$e]
push eax
push _p
call _printf
add esp, 8

;30: printnum(i)
xor eax, eax
xor  al, byte [$i]
push eax
push _p
call _printf
add esp, 8

;31: i = arr[i]
mov  al, byte [$i]
mov  ax, word [eax * 2 + $arr]
mov byte [$i],  al

;32: printnum(i)
xor eax, eax
xor  al, byte [$i]
push eax
push _p
call _printf
add esp, 8
