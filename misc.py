# String States
CHAR, ESCAPE, HEX_ESCAPE, *_ = range(8)

import os
CR_offset = int(os.name == 'nt')

# byte if size <= 8, word if 16 ...
size_list = ['byte', 'byte', 'byte', 'byte', 'word', 'dword', 'qword']
reg_list  = [' l', ' l', ' l', ' l', ' x', 'ex', 'rx']

arg_regs = ['di', 'si', 'c', 'd', 'r8', 'r9']
if os.name == 'nt': arg_regs = arg_regs[2:]

escape_sequences = {
	'a':'\a','n':'\n','f':'\f','t':'\t','v':'\v','r':'\r',
	"'":'\'','"':'"','\\':'\\'}

# a few dunder methods
unary = {
	'+': '__pos__',
	'-': '__neg__',
	'~': '__invert__',
	'*': '__deref__',
	'&': '__ref__',
}

binary = {
	'|' : '__or__',
	'&' : '__and__',
	'^' : '__xor__',
	'+' : '__add__',
	'-' : '__sub__',
	'*' : '__mul__',
	'%' : '__mod__',
	'/' : '__truediv__',
	# '//': '__floordiv__',
	# '**': '__pow__',
	# '<<': '__lshift__',
	# '>>': '__rshift__',
}

def err(msg):
	print(f'File "{argv[1]}", line {line_no}')
	print('   ', line.strip())
	if debug: raise RuntimeError(repr(msg))

	print(msg)
	quit(1)

def get_reg(reg: r'[abcd]|[ds]i|[sbi]p', size_n):
	if not size_n: err("TypeError: Can't fit in a register.")
	if reg in 'abcd':
		l, r = reg_list[size_n]
		return l+reg+r

	if reg.startswith('r'):
		if size_n == 6: return reg
		return reg+'bwd'[size_n-3]

	if size_n == 3: return reg+'l'
	if size_n == 4: return reg
	return 'er'[size_n-5]+reg

