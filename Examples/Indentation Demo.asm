extern printf
extern sprintf
extern strcpy
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
_q: db `%llu\n`, 0
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

; 3: '5i = 0\n'
mov rax, 0
mov dword [$i], 0

; 4: "[]3vbig = 'a very big \\x00'\n"

; 5: "[]3big = 'a big \\x00'\n"

; 6: "[]3space = ' \\x00'\n"

; 8: 'while i < 20:\n'
.L0:
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


; 9: 'if i < 5:\n'
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


; 10: 'println(i)\n'
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

; 11: 'elif i < 15:\n'
jmp .L1_end
.L1_0_else:
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


; 12: 'print(big)\n'
mov rax, $big
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

; 13: 'println(i)\n'
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

; 14: 'if i&1:\n'
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


; 15: 'println(22)\n'
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

; 16: 'else:\n'
jmp .L2_end
.L2_0_else:


; 17: '3k = 0\n'
mov rax, 0
mov byte [$k], 0

; 18: 'while k < 4:\n'
.L3:
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


; 19: 'print(k)\n'
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

; 20: 'print(space)\n'
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

; 21: 'k = k + 1\n'
mov  al, byte [$k]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$k],  al

; 22: 'println(11)\n'
jmp .L3
.L3_end:
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

; 23: 'else:\n'
.L2_1_else:
.L2_end:
jmp .L1_end
.L1_1_else:


; 24: 'print(vbig)\n'
mov rax, $vbig
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

; 25: 'println(i)\n'
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

; 26: 'i = i + 1\n'
.L1_2_else:
.L1_end:
mov eax, dword [$i]
mov rcx, rax
mov rax, 1
mov ebx, ecx
add rbx, rax
mov rax, rbx
mov dword [$i], eax

; 28: '@6 a b c\n'
jmp .L0
.L0_end:

; 30: 'println(space)\n'
mov rax, $space
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

; 32: 'a = 1\n'
mov rax, 1
mov qword [$a], 1

; 33: 'b = 1\n'
mov rax, 1
mov qword [$b], 1

; 35: '3j = 0\n'
mov rax, 0
mov byte [$j], 0

; 36: 'while j < 93:\n'
.L4:
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


; 37: 'print(j)\n'
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

; 38: 'print(space)\n'
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

; 39: 'println(a)\n'
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

; 40: 'c = a\n'
mov rax, qword [$a]
mov qword [$c], rax

; 41: 'a = b\n'
mov rax, qword [$b]
mov qword [$a], rax

; 42: 'b = b + c\n'
mov rax, qword [$b]
mov rcx, rax
mov rax, qword [$c]
mov rbx, rcx
add rbx, rax
mov rax, rbx
mov qword [$b], rax

; 43: 'j = j + 1\n'
mov  al, byte [$j]
mov rcx, rax
mov rax, 1
mov  bl,  cl
add rbx, rax
mov rax, rbx
mov byte [$j],  al

; 45: 'println(space)\n'
jmp .L4
.L4_end:
mov rax, $space
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

; 47: '3n = 0\n'
mov rax, 0
mov byte [$n], 0

; 48: 'while n < 16:\n'
.L5:
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


; 49: 'print(n)\n'
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

; 50: 'print(space)\n'
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

; 51: 'if n&1:\n'
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


; 52: 'println(2)\n'
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

; 53: 'else:\n'
jmp .L6_end
.L6_0_else:


; 54: 'println(1)\n'
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

; 55: 'n = n + 1\n'
.L6_1_else:
.L6_end:
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
