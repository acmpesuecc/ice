extern printf
extern malloc
extern exit
global main

segment .bss
$println: resb 1
$println: resb 1
$println: resb 1
$println: resb 2

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
$println: db `Hello, World!`

segment .text
main:
mov rax, 7
mov byte [$println],  al

;; println void 6
mov bl, byte [13*1 + $println - 1]
mov byte [13*1 + $println - 1], 0
mov rcx, $println
push rbp
call printf
pop rbp
mov byte [13*1 + $println - 1], bl

mov byte [_ln], bl
mov rcx, _ln
push rbp
call printf
pop rbp
mov  al, byte [$println]
mov byte [$println],  al

mov rax, 45
mov byte [$println],  al

mov rax, 7
mov byte [$println],  al

mov  al, byte [$println]
mov byte [$println],  al

mov rax, 8
mov rax, 4
xor rax, rax
xor rdx, rdx
mov rax, rax
div rcx
mov  al, byte [$println]
mov rax, rax
add  al,  cl
mov word [$println],  ax

xor rdx, rdx
xor  dx, word [$println]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
xor rdx, rdx
xor  dl, byte [$println]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
mov rax, 9
mov word [$println],  ax

xor rdx, rdx
xor  dx, word [$println]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
mov rax, 55
mov rax, 10
xor rax, rax
xor rdx, rdx
mov rax, rax
div rcx
mov rdx, rax
mov word [$println],  ax

xor rdx, rdx
xor  dx, word [$println]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
xor rcx, rcx
push rbp
call exit
