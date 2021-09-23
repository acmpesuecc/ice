extern _printf
extern _malloc
global _main

segment .bss
$pointer: resd 1

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0

segment .text
_main:

;2: pointer = 5
push 1
call _malloc
mov dword [$pointer], eax
mov byte [eax], 5

;3: printnum(pointer)
xor eax, eax
xor eax, dword [$pointer]
push eax
push _p
call _printf
add esp, 8
