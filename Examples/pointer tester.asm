extern printf
extern malloc
extern exit
global main

segment .bss
$println: resb 8
$println: resb 2
$println: resb 2

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
$println: db `val = `
$println: db `p_val = `

segment .text
main:
mov rax, $println
mov qword [$println], rax

mov rax, 9200
mov word [$println],  ax

;; print void 6
mov bl, byte [6*1 + $println - 1]
mov byte [6*1 + $println - 1], 0
mov rcx, $println
push rbp
call printf
pop rbp
mov byte [6*1 + $println - 1], bl

mov byte [_c], bl
mov rcx, _c
push rbp
call printf
pop rbp
xor rdx, rdx
xor  dx, word [$println]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
mov rax, qword [$println]
mov  ax, word [rax]
mov word [$println],  ax

;; print void 6
mov bl, byte [8*1 + $println - 1]
mov byte [8*1 + $println - 1], 0
mov rcx, $println
push rbp
call printf
pop rbp
mov byte [8*1 + $println - 1], bl

mov byte [_c], bl
mov rcx, _c
push rbp
call printf
pop rbp
xor rdx, rdx
xor  dx, word [$println]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp
mov  ax, word [$println]
