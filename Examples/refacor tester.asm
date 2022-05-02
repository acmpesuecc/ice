extern printf
extern malloc
global main

segment .bss

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0

segment .text
_main:
