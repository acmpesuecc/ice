extern printf
extern malloc
extern exit
global main

segment .bss
$pointer: resb 8
$val: resb 1

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
_name_pointer: db `pointer: %lld\n`, 0
_name_val: db `val: %lld\n`, 0

segment .text
main:
mov rax, 79
mov byte [$val],  al

mov rax, $val
mov qword [$pointer], rax

push rbp
mov rcx, _name_pointer
mov edx, 0
mov rdx, qword [$pointer]
xor rax, rax
call printf
mov rcx, _name_val
mov edx, 0
mov  dl, byte [$val]
xor rax, rax
call printf
pop  rbp
xor rcx, rcx
push rbp
call exit
