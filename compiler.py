# String States
CHAR, ESCAPE, HEX_ESCAPE, *_ = range(8)

from sys import argv

if __name__ != '__main__': debug = True
elif '-d' in argv: debug = True; argv.remove('-d')
else: debug = False

if len(argv) <2:
	if debug: argv.append('Tests\\refactor tester.ice')
	else: print('Input file not specified'); quit(1)
name = argv[1].rpartition('.')[0]
if len(argv)<3: argv.append(name+'.asm')

infile = open(argv[1])
out = open(argv[2], 'w')
def output(*args, file = out, **kwargs): print(*args, **kwargs, file = file)

sfile = open('builtins.ice-snippet')

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

if debug:
	class Debug:
		@staticmethod
		def get_snippets(): return snippets
		@staticmethod
		def get_variables(): return variables
		@staticmethod
		def get_infile(): return infile
		@staticmethod
		def get_outfile(): return output.__kwdefaults__["file"]
		@staticmethod
		def get_sfile(): return sfile

		@staticmethod
		def set_snippets(new_snippets): global snippets; snippets = new_snippets
		@staticmethod
		def set_variables(new_variables): global variables; variables = new_variables
		@staticmethod
		def set_infile(new_infile): global infile; infile = new_infile
		@staticmethod
		def set_sfile(new_sfile): global sfile; sfile = new_sfile
		@staticmethod
		def set_output_file(new_outfile):
			global output
			def output(*args, file = new_outfile, **kwargs):
				print(*args, **kwargs, file = file)

import re
class Patterns:
	wsep  = re.compile(r'\b')
	hex   = re.compile(r'[\da-fA-F]')
	equal = re.compile(r'(?<!=)=(?!=)')
	empty = re.compile(r'\[\][3-6]')

	shape = r'(?:(?:\[\d+\])*|\[\]|\**)'
	unit  = r'(?:[3-6]|[A-Za-z_]\w*)' # add tuple support
	label = rf'{shape}{unit}'
	decl  = re.compile(rf'(@({label})\s+|{shape}[3-6])([A-Za-z_]\w*)')
	dest  = re.compile(rf'(@{label}\s+|{shape}[3-6])?(\**)([A-Za-z_]\w*)'
			r'(?:\[([A-Za-z_]\w*|\d+)\])?')
	token = re.compile(rf'@(?P<label>{label})|(?P<subject>\d+|[a-zA-Z_]\w*)'
		r'(?:\s*(?:\.\s*(?P<method>[a-zA-Z_]\w*)\s*)?\((?P<args>.*?)\)|'
		r'\[(?P<item>.*?)\]' ')?|'
		r'(?P<symbol>\S)')

	stmt  = re.compile(r'(([\'"])(\\?.)*?\2|[^#])*')
	snip  = re.compile(r'%(\d+|e)([RELSCNU]|(?P<reg>[sd]i|[ibs]p|[a-d]))?\b')

	default = re.compile(r'(?P<param>(?P<int>[3-6])|(?:(?P<arr>\[\d+\])|\*))'
			# (?#|[3-6])))
			rf'(?P<element>{shape}(?:_?\w)*?)_(?P<method>[dm]\w*)')

class Variable:
	def __init__(self, label, name):
		self.name = name
		self.init = None
		self.size = label_size(label)
		if self.size in {1, 2, 4, 8}: self.size_n = self.size.bit_length()+2
		else: self.size_n = 0
		self.enc_name = self.encode()
		self.labels = [label]

	def __repr__(self):
		return f'{type(self).__name__}(@{self.get_label()} {self.name}, '\
			f'size = {self.size}, size_n = {self.size_n})'

	def encode(self):
		# enc_name = self.name.replace('_', '__')
		return '$'+self.name

	def get_label(self):
		return self.labels[-1]

	def get_clause(self, unit = False):
		return f'{size_list[self.size_n]} [{self.enc_name}]'

class Register(Variable):
	def encode(self):
		return get_reg(self.name, self.size_n)
	def get_clause(self, unit = False): return self.encode()

class Literal(Variable):
	def encode(self): return self.name
	def get_clause(self, unit = False): return self.name

def err(msg):
	print(f'File "{argv[1]}", line {line_no}')
	print('   ', line.strip())
	if debug: raise RuntimeError(repr(msg))

	print(msg)
	quit(1)

def get_length(label):
	# if label[0] == '*': return 1
	length = 1
	# TODO: add support for dynamic arrays
	for i in label[1:-2].split(']['):
		if not i: continue
		length *= int(i)
	return length

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

labels = {}
def label_size(label): # number of bytes
	fac = 1
	num = ''
	for i, d in enumerate(label):
		if d.isidentifier(): num = labels[label[i:]].size; break
		if d == '*': num = 6; break
		# add support for varrs (6, *d)
		if d == ']': fac *= int(num); num = ''
		elif d.isdigit(): num += d
	if num: return (fac<<(max(0, int(num)-3)))
	# control comes here only if the label format isn't right
	err('SyntaxError: Invalid label syntax.')

def element_size(label):
	if '*' in label: num = 8
	elif label[-1].isdigit(): num = 1<<max(0, int(label[-1])-3)
	else: num = 8

	# TODO: support named labels

	return num

def fun_encode(label, op):
	# check if label has that method?
	enc_op = op.replace('_', '__')
	if not label: return enc_op

	if len(op.lstrip('_'))+2 <= len(op) >= len(op.rstrip('_'))+2:
		enc_op = '_d'+enc_op[4:-4]
	else: enc_op = '_m'+enc_op

	label  = label.replace('_', '__')
	enc_op = label+enc_op
	return enc_op

def declare(label, name, init = None):
	if Patterns.empty.fullmatch(label):
		if init is None:
			err('SyntaxError: Implicit length requires initialisation.')
		init_length = len(init)//element_size(label)
		label = label[0]+str(init_length)+label[1:]

	if name in variables: # check prev
		var = variables[name]
		size = label_size(label)
		# TODO: plural
		if var.size != size: err(f'TypeError: {var.name!r}'
			f' uses {var.size} bytes, but {label!r} needs {size} bytes.')
		if init:
			if var.init and var.init != init:
				err(f'ValueError: Initialisation mismatch for {var.name!r}.'
					f'\n  Expected {[*var.init]}'
					f'\n  Got      {[*init]}')
			var.init = init
		return

	var = Variable(label, name)

	variables[name] = var

	if not init: output(var.enc_name+': resb', var.size)
	else: # check if init matches label
		if '[' not in label:
			err('ValueError: Cannot initialize non-sequence as sequence.')
		if '*' in label: err('ValueError: Sequence initialisation '
			'not yet supported for pointers.')
		size = label_size(label)
		# TODO: plural
		if len(init) != size:
			err(f'TypeError: {var.name!r} needs {size} bytes. '
				f'Got {len(init)} instead.')
		var.init = init

def get_snippet_label(enc_name, p, e): # use this if you know it's a snippet
	seek, ret_label, arg_labels = snippets[enc_name]
	if e is None: return ret_label
	return ret_label.replace('$e', e).replace('$s', p+e)

def get_call_label(enc_op): # this works for any enc_op
	if debug: print(f'Requested label of enc_op {enc_op!r}')

	enc_op, p, e = snippet_encode(enc_op)
	if enc_op in snippets: return get_snippet_label(enc_op, p, e)

	# Is it possible for snippet encode to run if enc_op in functions?
	if enc_op not in functions:
		err(f'NameError: function {enc_op!r} not defined.')
	return functions[enc_op][0] # (ret_label, *arg_labels)

def get_arg_labels(enc_op):
	enc_op, p, e = snippet_encode(enc_op)
	if enc_op in snippets:
		seek, ret_label, arg_labels = snippets[enc_op]
		return decode_snippet_args(arg_labels, p, e)

	# Is it possible for snippet encode to run if enc_op in functions?
	if enc_op not in functions:
		err(f'NameError: function {enc_op!r} not defined.')
	return functions[enc_op][1:] # (ret_label, *arg_labels)

def get_var(name, label = None):
	if name.isdigit(): return Literal(label or '6', name)
	if name not in variables: err(f'NameError: {name!r} not defined.')
	return variables[name]


# TODO?: `Snippet` class

def snippet_encode(name):
	match = Patterns.default.match(name)
	if not match: return name, None, None

	method = match['method']
	if   match['int']: enc_name = '_u'+method
	elif match['arr']: enc_name = '_a'+method
	else: enc_name = '_p'+method

	return enc_name, match['param'], match['element']

def decode_snippet_args(arg_labels, p, e) -> list[str]:
	arg_labels = arg_labels.copy()

	# TODO: add support for dynamic arrays

	if p == '*': p = '6'
	elif e: p = int(p[1:-1]); e = str(label_size(e))
	for i, size_n in enumerate(arg_labels):
		if   size_n == 's': arg_labels[i] = p
		elif size_n == 'e': arg_labels[i] = e
		else: arg_labels[i] = size_n

	return arg_labels

def insert_snippet(enc_name, args = (), p = None, e = None, match_args = True):
	seek, ret_label, arg_labels = snippets[enc_name]
	# if p:
	# ret_label = ret_label.replace('$e', e).replace('$s', p+e)
	# arg_labels, seek = snippet_setup(enc_name, args, p, e)
	if p: arg_labels = decode_snippet_args(arg_labels, p, e)

	# What if an argument is in c and another in a?
	# And I want to move a into c, then use the first argument.

	sfile.seek(seek)
	for line in sfile:
		if line in (';', ';\n'): break
		dline = line.strip()

		offset = 0
		for match in Patterns.snip.finditer(line):
			start, end = match.span()
			start += offset
			end   += offset
			if match[1] == 'e': label = e; arg = Literal(label, '0')
			else:
				n = int(match[1])

				arg = args[n]

				label = arg.get_label()
			tail = match[2]

			if not tail:
				print(f'File "{sfile.name}", in {enc_name}')
				err(f'Error: tail required in {dline!r}')
			elif tail == 'R':  sub = arg.name
			elif tail == 'E':  sub = arg.enc_name
			elif tail == 'L':  sub = str(get_length(label))

			elif tail == 'S':  sub = size_list[arg.size_n]
			elif tail == 'C':  sub = arg.get_clause()
			elif tail == 'N':  sub = str(label_size(label))
			elif tail == 'U':  sub = str(element_size(label))
			elif match['reg']: sub = get_reg(tail, arg.size_n)
			else: continue

			offset += len(sub)-len(match[0])
			line = line[:start]+sub+line[end:]
		output(line.strip())

def uni_fill(uni_chain, label):
	for i, uni in enumerate(reversed(uni_chain), 1):
		if uni.isidentifier(): break
		uni_chain[-i] = fun_encode(label, unary[uni])
		label = get_call_label(uni_chain[-i])

# def call_function(subject, op, args = (), label = None):
	# if label is not None: enc_op = fun_encode(label, op); args = (subject,)+args
	# elif subject in variables:
	# 	label = variables[subject].get_label()
	# 	enc_op = fun_encode(label, op)
	# elif op == '__call__': enc_op = subject.replace('_', '__')
	# else: err(f'NameError: Variable {subject!r} not declared.')

# Would take subject to check if it is a call to a function
# and not to a variable with a __call__ method.
# Should that check be here?
def call_function(enc_op, args : tuple[Variable] = ()):
	enc_op, p, e = snippet_encode(enc_op)

	if enc_op in snippets:
		insert_snippet(enc_op, args, p, e)
		return

	if enc_op not in functions:
		err(f'NameError: Function {enc_op!r} not defined.')

	arg_labels = functions[enc_op][1:]

	# TODO: plural
	if len(args) != len(arg_labels):
		err(f'TypeError: {enc_op!r} takes exactly {len(arg_labels)} arguments '
			f'({len(args)} given)')

	offset = -3
	for arg in args:
		if not arg.size_n:
			err(f'TypeError: {arg.name!r} cannot be passed as an argument.')

		if offset >= 0: output('push', arg_clause)
		else:
			output(f'mov {get_reg(arg_reg[offset], arg.size_n)}, {arg.name}')
		offset += 1

	if not offset&1: offset += 1; output('sub rsp, 8')
	# if vector_fun: output(f'mov rax, {vectors}')
	output('push rbp')
	output('call', enc_op)
	output('pop rbp')
	if offset: output('add rsp,', offset*8)

def assign(dest, imm: Variable = None):
	# TODO: get size of LHS (assuming 64-bit rn)
	match = Patterns.dest.match(dest)
	deref, dest, index = match[2], match[3], match[4]
	# print(dest, (var, index), sep = ' -> ')

	if dest.isdigit(): err("SyntaxError: Can't assign to literal.")

	if dest not in variables: err(f'NameError: {dest!r} not declared.')
	dest = variables[dest]

	if index:
		if deref: err("SyntaxError: Can't assign to multiple operations yet.")
		fun = fun_encode(dest.get_label(), '__setitem__')
		arg_labels = get_arg_labels(fun)
		print(f'{fun = }, {arg_labels = }, {index = }')
		
		if index.isdigit(): index = Literal(arg_labels[1], index)
		elif index not in variables: err(f'NameError: {index!r} not declared.')
		else: index = variables[index]

		call_function(fun, (dest, index, imm or Register(arg_labels[2], 'a')))
		return

	# Use __setat__ when * in dest
	if len(deref) > 2:
		err("SyntaxError: Can't assign to multiple dereferences yet.")
	if deref:
		fun = fun_encode(dest.get_label(), '__setat__')
		label = get_arg_labels(fun)[1]
		call_function(fun, (dest, imm or Register(label, 'a')))
		return

	output(f"mov {dest.get_clause()}, {imm or get_reg('a', dest.size_n)}")

variables = {}
functions = {}

snippets = {}
tell = 0
for line_no, line in enumerate(sfile, 1):
	tell += len(line)+CR_offset
	if not line.startswith('; '): continue
	enc_name, ret_label, *arg_labels = line[2:].split()
	snippets[enc_name] = (tell, ret_label, arg_labels)
# starts at a line starting with '; ' (mind the space)
# ends at a line with just ';' (refer `insert_snippet()`)

if debug: print('BUILTINS: ', *snippets)


if __name__ == '__main__':
	insert_snippet('_header')

	# Writing to bss segment

	output('\nsegment .bss')
	for line_no, line in enumerate(infile, 1):
		stmt = Patterns.stmt.match(line)[0].strip()
		lhs, *rhs = Patterns.equal.split(stmt, maxsplit = 1)
		lhs = lhs.strip()
		decls = lhs.split()
		decl = Patterns.decl.match(lhs)

		if not decl: continue

		if not rhs:
			if decl[2]:
				label = lhs.split()[0][1:]
				for decl in decls[1:]:
					decl = decl.strip()
					declare(label, decl)
			else:
				for decl in decls:
					decl = decl.strip()
					match = Patterns.decl.match(decl)
					if not match:
						err(f'SyntaxError: Expected a declaration token.')
					label, name = match[1].strip(), match[3]
					declare(label, name)
			continue

		if not lhs: err('SyntaxError: Assignment without destination.')
		if len(decls) != 1 and not (decl[2] and len(decls) == 2):
			err('SyntaxError: Assignment with multiple declarations')
		var = decl[0]
		size = element_size(decl[1])

		rhs = rhs[0].strip()
		end = False
		# Clean this up. Must expect comma after each value.
		if rhs[0] == '[': # TODO: robust syntax
			init = bytearray()
			for token in Patterns.wsep.split(rhs[1:]):
				token = token.strip()
				if not token: continue
				if end:
					err('SyntaxError: Token found after array initialisation.')
				if token.isdigit():
					init.extend(int(token).to_bytes(size, 'big'))
				elif token == ']': end = True
				elif token != ',': err('SyntaxError: Invalid token'
					f' {token!r} in array initialisation.')
			if not end:
				err('SyntaxError: Multi-line arrays are not yet supported.')

		elif rhs[0] in '"\'': # single char single quotes not yet char literal
			# TODO: test robust syntax
			init = bytearray()
			s = rhs[0]
			str_state = CHAR
			for c in rhs[1:]:
				if end:
					err('SyntaxError: Token found after string initialisation.')
				elif str_state == ESCAPE:
					str_state = CHAR
					if c == 'x': str_state = HEX_ESCAPE; init.append(0)
					elif c not in escape_sequences:
						err(f'SyntaxError: Invalid escape character {c!r}.')
					else: init.append(ord(escape_sequences[c]))
				elif str_state == HEX_ESCAPE:
					if not Patterns.hex.match(c):
						err('SyntaxError: Expected hexadecimal character.')

					if not init[-1]: init[-1] |= int(c, 16)<<4 | 15
					else:
						init[-1] = ~15&init[-1] | int(c, 16)
						str_state = CHAR

				elif c == '\\': str_state = ESCAPE
				elif c == s: end = True
				else: init.append(ord(c))
			else:
				if not end: err('SyntaxError: EOL while parsing string.')
		else: init = None

		var = var.strip()
		match = Patterns.decl.match(var)
		if not match: err(f'SyntaxError: Expected a declaration token.')
		name = match[3]
		label = match[2] or match[1]
		declare(label, name, init = init)

	# Writing to the data segment

	if debug: print('VARIABLES:', *variables.values())

	output()
	insert_snippet('_data')
	if debug: print('\nINITS:'); inits = False
	for var in variables.values():
		if not var.init: continue
		if debug: print(var.name, '=', var.init); inits = True

		output(var.enc_name, end = ': db ')
		out = repr(var.init)[12:-2].replace('`', '\\`')
		if '\\x' not in out: output(f'`{out}`')
		else: output(*var.init, sep = ', ')
	if debug and not inits: print(None)
	if debug: print()

	# Writing to the text segment

	infile.seek(0)
	output('\nsegment .text')
	output('main:')
	for line_no, line in enumerate(infile, 1):
		line = Patterns.stmt.match(line)[0]
		dest, _, exp = line.rpartition('=')
		dest = dest.strip()
		exp  = exp.strip()

		if not dest and Patterns.decl.match(exp): continue
		# if debug: print(f'{line_no}:', line.strip())
		isdecl = bool(Patterns.decl.match(dest))
		# decl = True
		uni_chain = []
		args = []
		label = None
		b_label = None
		bin_op  = None  # remembered for use after unary operations

		# output(f'\n;{line_no}:', line.strip())

		# expression lexing (mostly cleaned up)
		for token in Patterns.token.finditer(exp):
			if bin_op is True: # expecting a binary operator
				if token[0] not in binary:
					err('SyntaxError: Expected binary operator.')
				bin_op = fun_encode(b_label, binary[token[0]])
				continue

			if token['symbol']: # Expecting unary. Got some symbol.
				if token['symbol'] in '["\'':
					if bin_op or uni_chain: err('SyntaxError: '
						'Operations not yet supported on sequence literals.')
					if not isdecl: err('SyntaxError: Sequence literals '
						'not yet supported outside declaration.')
					dest = None; break # sequence literals initialise right now
				if token['symbol'] not in unary:
					err('SyntaxError: Invalid unary operator.')
				uni_chain.append(token['symbol'])
				label = None
				continue

			if token['label']:
				label = token['label']; uni_fill(uni_chain, label); continue


			if uni_chain:
				assert label or not uni_chain[-1].isidentifier()
				assert not label or uni_chain[-1].isidentifier()

			# Decode token
			args = []
			enc_op = None
			if token['args'] is not None:  # required for empty arg lists
				if not token['method']:
					enc_op = fun_encode('', token['subject'])
				else:
					var = get_var(token['subject'])
					args.append(var)
					enc_op = fun_encode(var.get_label(), token['method'])
				label = get_call_label(enc_op)
				arg_labels = get_arg_labels(enc_op)[len(args):]
				for arg, arg_label in zip(token['args'].split(','), arg_labels):
					args.append(get_var(arg.strip(), arg_label))
			elif token['item']:
				var = get_var(token['subject'])
				enc_op = fun_encode(var.get_label(), '__getitem__')
				label = get_call_label(enc_op)
				index_label = get_arg_labels(enc_op)[1]
				index = get_var(token['item'], index_label)
				args.extend([var, index])
			else:
				var = get_var(token['subject'], label)
				label = var.get_label()

			uni_fill(uni_chain, label)

			# Call suffixes and uni_chain.
			if enc_op is not None: call_function(enc_op, args)
			elif uni_chain: call_function(uni_chain.pop(), (var,))
			else: output(f'mov {get_reg("a", var.size_n)}, {var.get_clause()}')
			for enc_op in reversed(uni_chain):
				call_function(enc_op, (Register(label, 'a'),))
				label = get_call_label(enc_op)

			if bin_op is not None:
				arg_labels = get_arg_labels(bin_op)
				if len(arg_labels) != 2: err('TypeError: '
					f'{bin_op!r} does not take 2 arguments')
				# if label_size(arg_labels[1]) < label_size(label):
				# 	err(f'TypeError: Incompatible size for {bin_op!r}')
				call_function(bin_op,
					(Register(b_label, 'a'), Register(label, 'c')))
				b_label = get_call_label(bin_op)
			elif uni_chain: b_label = get_call_label(uni_chain[0])
			else: b_label = label

			label = None
			bin_op = True
			uni_chain = []

		# for no op (and for assignment also maybe?) check `label is None`
		if not dest: continue
		elif not exp: err('SyntaxError: Expected an expression.')
		else: assign(dest) # TODO: optimize redundant `mov rax` assign(dest, var)
		output()

	insert_snippet('_exit')

	print(f'Generated "{output.__kwdefaults__["file"].name}" successfully.')
