extern printf
extern sprintf
extern malloc
extern exit
global main

segment .bss
$x: resb 8

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
_fmt_udstr: db `%llu`, 0
_str: dq 0, 0, 0
_p_str: db `%s`, 0
_p_strln: db `%s\n`, 0
$char_arr: db 72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33, 0

segment .text
main:

;6: @str x = &char_arr
mov rax, $char_arr
mov qword [$x], rax

;7: println(x)
mov rax, qword [$x]
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

;10: println(x)
mov rax, qword [$x]
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
xor rcx, rcx
push rbp
call exit
