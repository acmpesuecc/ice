extern printf
extern sprintf
extern malloc
extern exit
global main

segment .bss
$x: resb 1
$i: resb 1
$b: resb 8
$a: resb 8
$c: resb 8

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
_fmt_udstr: db `%llu`, 0
_str: dq 0, 0, 0
_p_str: db `%s`, 0
_p_strln: db `%s\n`, 0
$space: db 32, 0

segment .text
main:
mov rax, 0
mov byte [$x],  al

.L0:
mov  al, byte [$x]
mov rcx, rax
mov rax, 100
xor rbx, rbx
mov  bl,  cl
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L0_end

mov  al, byte [$x]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$x],  al

mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8b, byte [$x]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
jmp .L0
.L0_end:

mov rax, $space
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
mov rax, 0
mov byte [$i],  al

mov rax, 1
mov qword [$b], rax

.L1:
mov  al, byte [$i]
mov rcx, rax
mov rax, 94
xor rbx, rbx
mov  bl,  cl
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L1_end

mov rax, qword [$a]
mov rcx, rax
mov rax, qword [$b]
mov rbx, rcx
add rbx, rax
mov rax, rbx
mov qword [$c], rax

mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8b, byte [$i]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, qword [$a]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
mov rax, qword [$b]
mov qword [$a], rax

mov rax, qword [$c]
mov qword [$b], rax

mov  al, byte [$i]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$i],  al

jmp .L1
.L1_end:

xor rcx, rcx
push rbp
call exit
