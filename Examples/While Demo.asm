extern printf
extern sprintf
extern malloc
extern exit
global main

segment .bss
$x: resb 1
$i: resb 1
$j: resb 1
$b: resb 4
$a: resb 4
$c: resb 4

segment .data
_p: db `%u\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
_fmt_udstr: db `%llu`, 0
_str: times 3 dq 0
_p_str: db `%s`, 0
_p_strln: db `%s\n`, 0
$space: db ` 0`

segment .text
main:

;7: 3x = 0
mov rax, 0
mov byte [$x],  al

.L0:

;8: while x < 100
mov  al, byte [$x]
mov rcx, rax
mov rax, 100
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

;16: space[1] = 0
mov rax, 0
xor rbx, rbx
mov rbx, 1
mov  al,   al
mov byte [rbx * 1 + $space],  al


;17: println(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

;24: 3i = 0
mov rax, 0
mov byte [$i],  al


;26: 5b = 1
mov rax, 1
mov dword [$b], eax

.L1:

;28: while i < 10
mov  al, byte [$i]
mov rcx, rax
mov rax, 10
mov  bl,  cl
cmp rbx, rax
setl al
test  al, -1
setnz al
test al, al
jz .L1_end

;29: c = a+b
mov eax, dword [$a]
mov rcx, rax
mov eax, dword [$b]
mov ebx, ecx
add ebx, eax
mov rax, rbx
mov dword [$c], eax


;30: print(i)
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

;31: print(space)
mov rax, $space
mov rdx, rax
mov rcx, _p_str
push rbp
call printf
pop rbp

;32: println(a)
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8d, dword [$a]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

;33: a = b
mov eax, dword [$b]
mov dword [$a], eax


;34: b = c
mov eax, dword [$c]
mov dword [$b], eax


;35: i = i + 1
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
