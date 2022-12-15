extern printf
extern sprintf
extern strcpy
extern malloc
extern exit
global main

segment .bss
$hello_ptr: resb 8
$x: resb 8
$y: resb 8

segment .data
_p: db `%u\n`, 0
_q: db `%llu\n`, 0
_c: db 0, 0
_ln: db 0, 10, 0
_fmt_udstr: db `%llu`, 0
_str: dq 0, 0, 0
_p_str: db `%s`, 0
_p_strln: db `%s\n`, 0
$hello_arr: db 72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33, 0

segment .text
main:

; 1: 'if 0:\n'
mov rax, 0
test rax, -1
setnz al
test al, al
jz .L0_0_else


; 2: '@6 hello_ptr\n'

; 3: "@[]3 hello_arr = 'Hello, World!\\x00'\n"

; 4: 'hello_ptr = str(hello_arr)\n'
.L0_0_else:
.L0_end:
mov rax, $hello_arr
mov qword [$hello_ptr], rax

; 5: 'println(hello_ptr)\n'
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, qword [$hello_ptr]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

; 7: '6x = 8  '
mov rax, 8
mov qword [$x], 8

; 8: '6x = str(x)\n'
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, qword [$x]
push rbp
call sprintf
pop rbp
mov rax, _str
mov qword [$x], rax

; 10: '*4y = 55\n'
mov rax, 55
mov qword [$y], 55

; 11: '6y = str(y)\n'
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, qword [$y]
push rbp
call sprintf
pop rbp
mov rax, _str
mov qword [$y], rax

; 13: 'println(x)\n'
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, qword [$x]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

; 14: '@str x\n'

; 15: 'println(x)\n'
mov rax, qword [$x]
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

; 16: 'println(hello_ptr)\n'
mov rcx, _str
mov rdx, _fmt_udstr
xor r8, r8
mov r8, qword [$hello_ptr]
push rbp
call sprintf
pop rbp
mov rax, _str
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp

; 17: '@str hello_ptr\n'

; 18: 'println(hello_ptr)\n'
mov rax, qword [$hello_ptr]
mov rdx, rax
mov rcx, _p_strln
push rbp
call printf
pop rbp
xor rcx, rcx
push rbp
call exit
