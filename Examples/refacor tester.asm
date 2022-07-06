extern printf
extern malloc
extern exit
global main

segment .bss
$x: resb 1
$y: resb 1
$z: resb 1
$out: resb 2

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
$hello: db `Hello, World!`
_name_x: db `x: %lld\n`, 0
_name_hello: db `hello: %lld\n`, 0
_name_y: db `y: %lld\n`, 0
_name_z: db `z: %lld\n`, 0
_name_out: db `out: %lld\n`, 0

segment .text
main:
mov rax, 7
mov byte [$x],  al

mov  al, byte [$x]
neg  al
mov byte [$x],  al

mov rax, 45
mov byte [$y],  al

mov rax, 7
mov byte [$z],  al

mov  al, byte [$z]
neg  al
mov byte [$z],  al

mov  al, byte [$y]
mov rcx, rax
mov  al, byte [$z]
neg  al
mov  al,  al
mul  cl
mov rcx, rax
mov  al, byte [$x]
mov  al,  al
add  al,  cl
mov word [$out],  ax

push rbp
mov rcx, _name_x
mov edx, 0
mov  dl, byte [$x]
xor rax, rax
call printf
mov rcx, _name_hello
mov edx, 0
mov rdx, qword [$hello]
xor rax, rax
call printf
mov rcx, _name_y
mov edx, 0
mov  dl, byte [$y]
xor rax, rax
call printf
mov rcx, _name_z
mov edx, 0
mov  dl, byte [$z]
xor rax, rax
call printf
mov rcx, _name_out
mov edx, 0
mov  dx, word [$out]
xor rax, rax
call printf
pop  rbp
xor rcx, rcx
push rbp
call exit
