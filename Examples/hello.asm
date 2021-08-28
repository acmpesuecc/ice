extern _printf
global _main

segment .bss

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
v_hello: db 72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33

segment .text
_main:

;1: println(hello)
mov bl, byte [(13*1) + (v_hello-1)]
mov byte [(13*1) + (v_hello-1)], 0
push v_hello
call _printf
add esp, 4
mov byte [(13*1) + (v_hello-1)], bl

mov byte [_ln], bl
push _ln
call _printf
add esp, 4
