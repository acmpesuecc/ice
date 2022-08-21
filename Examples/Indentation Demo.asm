extern printf
extern sprintf
extern malloc
extern exit
global main

segment .bss
$i: resb 4
$k: resb 1
$a: resb 8
$b: resb 8
$c: resb 8
$j: resb 1
$n: resb 1

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
_fmt_udstr: db `%llu`, 0
_str: dq 0, 0, 0
_p_str: db `%s`, 0
_p_strln: db `%s\n`, 0
$vbig: db 97, 32, 118, 101, 114, 121, 32, 98, 105, 103, 32, 0
$big: db 97, 32, 98, 105, 103, 32, 0
$space: db 32, 0

segment .text
main:

;3: 5i = 0
mov rax, 0
mov dword [$i], eax
.L0:

;8: while i < 20:
mov eax, dword [$i]
mov rcx, rax
mov rax, 20
xor rbx, rbx
mov ebx, ecx
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L0_end


;9: if i < 5:
mov eax, dword [$i]
mov rcx, rax
mov rax, 5
xor rbx, rbx
mov ebx, ecx
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L1_0_else


;10: println(i)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8d, dword [$i]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
jmp .L1_end
.L1_0_else:

;11: elif i < 15:
mov eax, dword [$i]
mov rcx, rax
mov rax, 15
xor rbx, rbx
mov ebx, ecx
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L1_1_else


;12: print(big)
mov rax, $big
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;13: println(i)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8d, dword [$i]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

;14: if i&1:
mov eax, dword [$i]
mov rcx, rax
mov rax, 1
mov ebx, ecx
and rbx, rax
mov rax, rbx
test eax, -1
setnz al
test al, al
jz .L2_0_else


;15: println(22)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, 22
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
jmp .L2_end
.L2_0_else:


;17: 3k = 0
mov rax, 0
mov byte [$k],  al
.L3:

;18: while k < 4:
mov  al, byte [$k]
mov rcx, rax
mov rax, 4
xor rbx, rbx
mov  bl,  cl
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L3_end


;19: print(k)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8b, byte [$k]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;20: print(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;21: k = k + 1
mov  al, byte [$k]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$k],  al
jmp .L3
.L3_end:

;22: println(11)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, 11
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
.L2_1_else:
.L2_end:
jmp .L1_end
.L1_1_else:


;24: print(vbig)
mov rax, $vbig
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;25: println(i)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8d, dword [$i]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
.L1_2_else:
.L1_end:

;26: i = i + 1
mov eax, dword [$i]
mov rcx, rax
mov rax, 1
mov ebx, ecx
add rbx, rax
mov rax, rbx
mov dword [$i], eax
jmp .L0
.L0_end:

;30: println(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

;32: a = 1
mov rax, 1
mov qword [$a], rax

;33: b = 1
mov rax, 1
mov qword [$b], rax

;35: 3j = 0
mov rax, 0
mov byte [$j],  al
.L4:

;36: while j < 93:
mov  al, byte [$j]
mov rcx, rax
mov rax, 93
xor rbx, rbx
mov  bl,  cl
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L4_end


;37: print(j)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8b, byte [$j]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;38: print(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;39: println(a)
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

;40: c = a
mov rax, qword [$a]
mov qword [$c], rax

;41: a = b
mov rax, qword [$b]
mov qword [$a], rax

;42: b = b + c
mov rax, qword [$b]
mov rcx, rax
mov rax, qword [$c]
mov rbx, rcx
add rbx, rax
mov rax, rbx
mov qword [$b], rax

;43: j = j + 1
mov  al, byte [$j]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$j],  al
jmp .L4
.L4_end:

;45: println(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

;47: 3n = 0
mov rax, 0
mov byte [$n],  al
.L5:

;48: while n < 16:
mov  al, byte [$n]
mov rcx, rax
mov rax, 16
xor rbx, rbx
mov  bl,  cl
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L5_end


;49: print(n)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8b, byte [$n]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;50: print(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;51: if n&1:
mov  al, byte [$n]
mov rcx, rax
mov rax, 1
mov  bl,  cl
and rbx, rax
mov rax, rbx
test  al, -1
setnz al
test al, al
jz .L6_0_else


;52: println(2)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, 2
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
jmp .L6_end
.L6_0_else:


;54: println(1)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, 1
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
.L6_1_else:
.L6_end:

;55: n = n + 1
mov  al, byte [$n]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$n],  al
jmp .L5
.L5_end:
xor rcx, rcx
push rbp
call exit
