extern printf
extern malloc
extern exit
global main

segment .bss

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
$hello: db `Hello, World!`
_name_hello: db `hello: %lld\n`, 0

segment .text
main:
;; println void 6
mov bl, byte [13*1 + $hello - 1]
mov byte [13*1 + $hello - 1], 0
mov rcx, $hello
push rbp
call printf
pop rbp
mov byte [13*1 + $hello - 1], bl

mov byte [_ln], bl
mov rcx, _ln
push rbp
call printf
pop rbp
xor rcx, rcx
push rbp
call exit
