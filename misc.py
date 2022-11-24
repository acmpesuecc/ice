import labels
import Patterns
from sys import argv

# String States
CHAR, ESCAPE, HEX_ESCAPE, *_ = range(8)
WHILE_BRANCH = type('WHILE_BRANCH', (), {'__repr__': lambda s: '<WHILE_BRANCH>'})()

import os
crlf = int(os.name == 'nt')

# byte if size <= 8, word if 16 ...
size_list = ['byte', 'byte', 'byte', 'byte', 'word', 'dword', 'qword']
reg_list  = [' l', ' l', ' l', ' l', ' x', 'ex', 'rx']

arg_regs = ['di', 'si', 'c', 'd', 'r8', 'r9']
if os.name == 'nt': arg_regs = arg_regs[2:]

elses = {'elif', 'else'}
keywords = {'while', 'if', *elses}

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
	'<':  '__lt__',
	'>':  '__gt__',
	# '//': '__floordiv__',
	# '**': '__pow__',
	# '<<': '__lshift__',
	# '>>': '__rshift__',
	# '<=': '__le__',
	# '>=': '__ge__',
}

def err(msg):
	import compiler
	try: print(f'File "{compiler.infile.name}", line {Shared.line_no}')
	except AttributeError: print(f'Debug input, line {Shared.line_no}')
	print('   ', Shared.line.strip())
	if Shared.debug: raise RuntimeError(repr(msg))

	print(msg)
	quit(1)

def get_reg(reg: r'[abcd]|[ds]i|[sbi]p|r(8|9|1[1-5])', size_n, var = None):
	if not size_n:
		if var is None: err("TypeError: Can't fit in a register.")
		err(f"TypeError: Can't fit {var} in a register.")
	if reg in 'abcd':
		l, r = reg_list[size_n]
		return l+reg+r

	if reg.startswith('r'):
		if size_n == 6: return reg
		return reg+'bwd'[size_n-3]

	if size_n == 3: return reg+'l'
	if size_n == 4: return reg
	return 'er'[size_n-5]+reg

class Shared:
	line = '[DEBUG] ** Empty line **'
	line_no = 0
	debug = False

class Variable:
	def __init__(self, label, name, setlabel = True):
		self.name = name
		self.init = None
		self.size = labels.get_size(label)
		self.size_n = labels.get_size_n(self.size)
		self.enc_name = self.encode()
		self.labels = [label if setlabel else None]

	def __repr__(self):
		return f'{type(self).__name__}(@{self.get_label()} {self.name}, '\
			f'size = {self.size})'

	def encode(self):
		# enc_name = self.name.replace('_', '__')
		return '$'+self.name

	def get_label(self):
		# TODO: add logic for scope level
		return self.labels[-1]

	def set_label(self, label):  # might make this a @property
		if Patterns.empty.fullmatch(label):
			# assume non-inits have been ruled out
			arr_len = len(self.init) // labels.element_size(label)
			label = '%s%d%s' % (label[0], arr_len, label[1:])

		if labels.get_size(label) != self.size:
			# TODO: plural
			err(f'TypeError: Cannot set label {label!r} for {self.name!r} '
				f'(Requires {self.size} bytes, got {labels.get_size(label)})')
		if Shared.debug: print(f'Set the label of {self.name!r} to {label}')
		self.labels[-1] = label
		return label  # returns because it changes if empty label

	def get_clause(self, unit = False):
		return f'{size_list[self.size_n]} [{self.enc_name}]'

class Register(Variable):
	def encode(self):
		return get_reg(self.name, self.size_n)
	def get_clause(self, unit = False): return self.encode()

class Literal(Variable):
	def encode(self): return self.name
	def get_clause(self, unit = False): return self.name
