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

;7: 3x = 0
mov rax, 0
mov byte [$x],  al
.L0:

;8: while x < 100:
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


;9: x = x + 1
mov  al, byte [$x]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$x],  al

;10: println(x)
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

;15: println(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

;22: 3i = 0
mov rax, 0
mov byte [$i],  al

;23: 6b = 1
mov rax, 1
mov qword [$b], rax
.L1:

;25: while i < 94:
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


;26: c = a+b
mov rax, qword [$a]
mov rcx, rax
mov rax, qword [$b]
mov rbx, rcx
add rbx, rax
mov rax, rbx
mov qword [$c], rax

;27: print(i)
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

;28: print(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;29: println(a)
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

;30: a = b
mov rax, qword [$b]
mov qword [$a], rax

;31: b = c
mov rax, qword [$c]
mov qword [$b], rax

;32: i = i + 1
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
