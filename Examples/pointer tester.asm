
; [DEBUG] _header ()
extern printf
extern malloc
extern exit
global main

segment .bss
$pptr: resb 8
$ptr: resb 8
$val: resb 2
$p_val: resb 2


; [DEBUG] _data ()
segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
$p_debug: db `p_val = `
$debug: db `val = `

segment .text
main:

; [DEBUG] _pdref ('ptr',)
mov rax, $ptr
mov qword [$pptr], rax


; [DEBUG] _udref ('val',)
mov rax, $val
mov qword [$ptr], rax

mov rax, 9200
mov word [$val],  ax


; [DEBUG] _pdderef ('pptr',)
mov rax, qword [$pptr]
mov rax, qword [rax]

; [DEBUG] _pdderef ('a',)
mov rax, rax
mov  ax, word [rax]

; [DEBUG] _udneg ('a',)
mov  ax,  ax
neg  ax

; [DEBUG] _udinvert ('a',)
mov  ax,  ax
not  ax
mov word [$p_val],  ax


; [DEBUG] print ('p_debug',)
;; print void 6
mov bl, byte [8*1 + $p_debug - 1]
mov byte [8*1 + $p_debug - 1], 0
mov rcx, $p_debug
push rbp
call printf
pop rbp
mov byte [8*1 + $p_debug - 1], bl

mov byte [_c], bl
mov rcx, _c
push rbp
call printf
pop rbp

; [DEBUG] printnum ('p_val',)
xor rdx, rdx
xor  dx, word [$p_val]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp

; [DEBUG] print ('debug',)
;; print void 6
mov bl, byte [6*1 + $debug - 1]
mov byte [6*1 + $debug - 1], 0
mov rcx, $debug
push rbp
call printf
pop rbp
mov byte [6*1 + $debug - 1], bl

mov byte [_c], bl
mov rcx, _c
push rbp
call printf
pop rbp

; [DEBUG] printnum ('val',)
xor rdx, rdx
xor  dx, word [$val]
xor rax, rax
mov rcx, _p
push rbp
call printf
pop rbp

; [DEBUG] _exit ()
xor rcx, rcx
push rbp
call exit
