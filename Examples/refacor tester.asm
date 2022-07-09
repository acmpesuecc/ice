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

segment .text
main:
mov rax, 7
mov byte [$x],  al

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

mov rax, 8
mov rcx, rax
mov rax, 4
xor rax, rax
xor rdx, rdx
mov rax, rax
div rcx
mov rcx, rax
mov  al, byte [$x]
mov rax, rax
add rax, rcx
mov word [$out],  ax

xor rdx, rdx
xor  dx, word [$out]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
xor rdx, rdx
xor  dl, byte [$x]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
mov rax, 9
mov word [$out],  ax

xor rdx, rdx
xor  dx, word [$out]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
mov rax, 55
mov rcx, rax
mov rax, 10
xor rax, rax
xor rdx, rdx
mov rax, rax
div rcx
mov rdx, rax
mov word [$out],  ax

xor rdx, rdx
xor  dx, word [$out]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
xor rcx, rcx
push rbp
call exit
