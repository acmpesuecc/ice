# TODO: Remove varinfo(). Make methods under the Variable class.

# Flags for varinfo()
[USE_UNITSIZE, GET_CLAUSE, GET_LENGTH, GET_SIZE, GET_NBYTES, GET_REG,
	*_] = (1<<i for i in range(8))

# String States
CHAR, ESCAPE, HEX_ESCAPE, *_ = range(8)

from sys import argv
debug = False
if '-d' in argv: debug = True; argv.remove('-d')
if len(argv) <2:
	if debug: argv.append('Examples\\hello.ice')
	else: print('Input file not specified'); quit(1)
name = argv[1].rpartition('.')[0]
if len(argv)<3: argv.append(name+'.asm')

infile = open(argv[1])
out = open(argv[2], 'w')
def output(*args, file = out, **kwargs): print(*args, **kwargs, file = file)

import re
class Patterns:
	wsep  = re.compile(r'\b')
	hex   = re.compile(r'[\da-fA-F]')
	equal = re.compile(r'(?<!=)=(?!=)')
	space = re.compile(r'\s+')
	empty = re.compile(r'\[\][3-6]')

	shape = r'(?:(?:\[\d+\])*|\[\]|\*)'
	unit  = r'[3-6]|[A-Za-z_]\w*' # add tuple support
	label = rf'{shape}{unit}'
	token = re.compile(rf'@({label})|\d+|[a-zA-Z_]\w*|(\S)')
	decl  = re.compile(rf'@({label}\s+|{shape}[3-6])([A-Za-z_]\w*)')
	dest  = re.compile(rf'(@{label}\s+|{shape}[3-6])?([A-Za-z_]\w*)'
			r'(?:\[([A-Za-z_]\w*)\])?')

	stmt  = re.compile(r'(([\'"])(\\?.)*?\2|[^#])*')
	sub   = re.compile(r'(?i)%(\d+)([a-z])?\b')

class Variable:
	def __init__(self, label, name):
		self.name = name
		self.init = None
		self.enc_name = self.var_encode()
		self.size = label_size(label)
		self.labels = [label]

	def __repr__(self):
		return f'{type(self).__name__}(@{self.get_label()} {self.name}, '\
			f'size = {self.size})'

	def var_encode(self):
		enc_name = self.name.replace('_', '__')
		return '$'+enc_name

	def get_label(self):
		return self.labels[-1]

class Register(Variable):
	def var_encode(self):
		# assuming label[0] for register gives unit
		unit = self.get_label()[0]
		if unit == '*': unit = '6' # 64-bit
		a, b = reg_list[int(unit)]
		return a+self.name+b

class Literal(Variable):
	def var_encode(self): return self.name

def err(msg):
	print(f'File "{argv[1]}", line {line_no}')
	print('   ', line.strip())
	if debug: raise RuntimeError(repr(msg)) # temporary, for debugging

	print(msg)
	quit(1)

def new_var(token, init = None):
	match = Patterns.decl.match(token)
	label, name = match[1].strip(), match[2]

	if Patterns.empty.fullmatch(label):
		if init is None:
			err('ValueError: Implicit length requires initialisation.')
		init_length = len(init)
		label = label[0]+str(init_length)+label[1:]

	if name in variables: # check prev
		var = variables[name]
		size = label_size(label)
		if var.size != size: err(f'TypeError: {var.name!r}'
			f'uses {var.size} bytes, but {label!r} needs {size} bytes.')
		if init:
			if var.init and var.init != init:
				err(f'ValueError: Initialisation mismatch for {var.name!r}.'
					f'\n  Expected {var.init}'
					f'\n  Got      {init}')
			var.init = init
		return

	var = Variable(label, name)

	variables[name] = var
	shape_len = get_length(shape)
	if init:
		init_length = len(init)
		if init_length != shape_len:
			err(f'ValueError: Shape expects {shape_len} elements. '
				f'Got {init_length} instead.')
		var.init = init
	else:
		size = varinfo(name, GET_SIZE)[0]
		output(var.enc_name+': res'+size, shape_len)

def varinfo(var, flags = GET_CLAUSE, reg = 'a'):
	if var not in variables: err(f'ValueError: {var!r} is not declared.')
	var = variables[var]
	# size, int and reg for pointers will already be known, so it isn't needed
	# clause of a pointer has to be with a dword, so no need extra flag
	# no, but it doesn't work with the builtins so yes extra flag
	label = var.labels[-1]
	# add support for size from label names
	size = int(label[-1]) if '*' not in label or flags&USE_UNITSIZE else 5
	out = ()
	if flags&GET_CLAUSE: out += (f'{size_list[size]} [{var.enc_name}]',)
	# if flags&GET_LENGTH: out += (get_length(var.shape),)
	if flags&GET_SIZE: out += (f'{size_list[size]}',)
	if flags&GET_NBYTES: out += (var.size,)
	if flags&GET_REG: a, b = reg_list[size]; out += (a+reg+b,)

	if len(out) == 1: return out[0]
	return out

def insert_snippet(fun, args = (), encode = True):
	sfile.seek(snippets[fun][0])
	for line in sfile:
		if line in (';', ';\n'): break

		offset = 0
		for match in Patterns.sub.finditer(line):
			start, end = match.span()
			start += offset
			end   += offset
			arg = args[int(match[1])]
			tail = match[2]

			if not encode: sub = arg
			elif not tail: sub = varinfo(arg)
			elif tail == 'r': sub = variables[arg].enc_name
			elif tail == 's': sub = varinfo(arg, flags = GET_SIZE)
			elif tail == 'n': sub = str(varinfo(arg, flags = GET_NBYTES))
			elif tail == 'l': sub = str(varinfo(arg, flags = GET_LENGTH))
			elif tail in 'abcd': sub = varinfo(arg, flags = GET_REG, reg = tail)
			else: continue

			offset += len(sub)-len(match[0])
			line = line[:start]+sub+line[end:]
		output(line.strip())

def fun_encode(subject, op):
	op = op.replace('_', ' ')

	if subject not in variables:
		if op == '  call  ': return subject.replace('_', '__')
		return op.replace(' ', '__')

	if op.startswith('  ') and op.endswith('  ') and len(op) >= 4:
		op = '_d'+op[2:-2]
	else: op = '_m'+op
	op = op.replace(' ', '__')

	label = variables[subject].labels[-1]
	if label[0] == '_' and label[1] != '_': label = label.replace('_', ' ', 1)
	label = label.replace('_', '__')
	label = label.replace(' ', '_')

	return label+op

def get_call_label(enc_op):
	if enc_op in snippets: return snippets[enc_op][1]
	return functions[enc_op][0] # (ret_label, *arg_sizes)

def assign(dest, imm = None):
	match = Patterns.dest.match(dest)
	var, index = match[2], match[3]
	# print(dest, (var, index), sep = ' -> ')

	if index:
		if imm: output('mov eax,', imm)
		call_function('__setitem__', var, [index])
		return

	if variables[var].shape[0] == '*':
		if not imm: output('mov ebx, eax'); src = 'ebx'
		else: src = imm
		insert_snippet('_ptralloc', (var, src), encode = False)
		return

	if imm: output(f'mov {varinfo(var)}, {imm}')
	else:
		clause, reg = varinfo(var, flags = GET_CLAUSE|GET_REG)
		output(f'mov {clause}, {reg}')

def call_function(op, subject, args = ()):
	enc_op = fun_encode(subject, op)

	if enc_op in snippets:
		insert_snippet(enc_op, args = [subject]+args)
		return

	offset = 0
	for arg in args:
		arg_clause, size = varinfo(arg, flags = GET_CLAUSE|GET_NBYTES)
		output('push', arg_clause)
		offset += size

	if op != '__call__':
		subject_clause, size = varinfo(subject, flags = GET_CLAUSE|GET_NBYTES)
		output('push', subject_clause)
		offset += size
		output('call', enc_op)
	else: output('call', subject)
	output('add esp,', offset)

def get_length(label, expected = None):
	# if label[0] == '*': return 1
	length = 1
	# add support for ^ symbol in label
	# add support for varr
	for i in label[1:-2].split(']['):
		if not i: continue
		length *= int(i)
	return length

def label_size(label):
	fac = 1
	num = ''
	for i, d in enumerate(label):
		# add support for varrs
		if d == ']': fac *= int(num); num = ''
		elif d.digit(): num += d
		elif d == '*': return 4*fac
		elif d.isalpha(): return labels[label[i:]].size*fac
	if num: return (1<<(max(0, int(num)-3)))
	# control comes here only if the label format isn't right
	err('SyntaxError: Invalid label syntax.')

variables = {}

escape_sequences = {
	'a':'\a','n':'\n','f':'\f','t':'\t','v':'\v','r':'\r',
	"'":'\'','"':'"','\\':'\\'}

# a few dunder methods
symbols = {
	'|' : '__or__',
	'&' : '__and__',
	'^' : '__xor__',
	'+' : '__add__',
	'-' : '__sub__',
	'*' : '__mul__',
	'/' : '__truediv__',
	'//': '__floordiv__',
	'**': '__pow__',
	'<<': '__lshift__',
	'>>': '__rshift__',
}

# byte if size <= 8, word if 16 ...
size_list = ['byte', 'byte', 'byte', 'byte', 'word', 'dword', 'qword']
reg_list  = [' l', ' l', ' l', ' l', ' x', 'ex', 'rx']

sfile = open('builtins.ice-snippet')

snippets = {}
tell = 0
for line_no, line in enumerate(sfile, 1):
	tell += len(line)
	if not line.startswith('; '): continue
	name, ret, *args = line[2:].split()
	snippets[name] = (name, ret, args)
# starts at a line starting with '; ' (mind the space)
# ends at a line with just ';' (refer `insert_snippet()`)

if debug: print('BUILTINS: ', *snippets)

insert_snippet('_header')

# Writing to bss segment

output('\nsegment .bss')
for line_no, line in enumerate(infile, 1):
	stmt = Patterns.stmt.match(line)[0].strip()
	lhs, *rhs = Patterns.equal.split(stmt, maxsplit = 1)
	lhs = lhs.strip()
	decls = lhs.split()

	if not Patterns.decl.match(lhs): continue

	if not rhs:
		for decl in decls:
			decl = decl.strip()
			if Patterns.decl.match(decl): new_var(decl)
			else: err(f'SyntaxError: Expected a declaration token.')
		continue

	if not lhs: err('SyntaxError: Assignment without destination.')
	if len(decls) > 1:
		err('SyntaxError: Assignment with multiple declarations')
	var = decls[0]
	init = []

	rhs = rhs[0].strip()
	end = False
	if rhs[0] == '[':
		for token in Patterns.wsep.split(rhs[1:]):
			token = token.strip()
			if not token: continue
			if end:
				err('SyntaxError: Token found after array initialisation.')
			if token.isdigit(): init.append(int(token))
			elif token == ']': end = True
			elif token != ',': err('SyntaxError: Invalid token'
				f' {token!r} in array initialisation.')
		if not end: err('SyntaxError: Multi-line arrays are not yet supported.')

	elif rhs[0] in '"\'':
		s = rhs[0]
		str_state = CHAR
		for c in rhs[1:]:
			if str_state == ESCAPE:
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
					str_state = 0

			elif c == '\\': str_state = ESCAPE
			elif c == s: break
			else: init.append(ord(c))
			# print(c, f'{init_type:06b}', init)
		else: err('SyntaxError: EOL while parsing string.')

	new_var(var, init = init)

# Writing to the data segment

if debug: print('VARIABLES:', *variables.values())

output()
insert_snippet('_data')
if debug: print('\nINITS:')
inits = False
for var in variables.values():
	if not var.init: continue
	inits = True
	size = size_list[int(var.shape[-1])][0]

	if debug: print(var.name, '=', var.init)
	output(var.enc_name+': d'+size, end = ' ')
	output(*var.init, sep = ', ')
if debug and not inits: print(None)

# Writing to the text segment

infile.seek(0)
output('\nsegment .text')
output('_main:')
for line_no, line in enumerate(infile, 1):
	decl = True
	subject = ''
	op = ''
	args = []
	line = Patterns.stmt.match(line)[0]
	dest, _, exp = line.rpartition('=')
	dest = dest.strip()
	exp  = exp.strip()

	if not dest and Patterns.decl.match(exp): continue
	# if debug: print(f'{line_no}:', line.strip())
	isdecl = bool(Patterns.decl.match(dest))

	# expression lexing (still might need cleaning up)
	tokens = Patterns.wsep.split(exp)
	for token in tokens:
		token = token.strip()
		if not token: continue
		if Patterns.decl.match(token):
			err('SyntaxError: Cannot declare within expressions.')

		if not subject:
			if token[0] in '["\'':
				if isdecl: dest = False; break
				else: err('SyntaxError: Initialisation without declaration.')
			D = Patterns.ident.match(token)
			if not D:err(f'SyntaxError: Invalid token {token!r} in expression.')
			if D[1]: err('SyntaxError: Cannot declare within expressions')
			subject = token

		elif not op:
			if   token[0] == '(': op = '__call__'
			elif token[0] == '[': op = '__getitem__'
			elif token == '.': op = False
			elif op == False: op = token
			elif token in symbols: op = symbols[token]
			elif not token: err('SyntaxError: Expected an operation.')
		elif token.isalnum(): args.append(token)

	if op:
		output(f'\n;{line_no}:', line.strip())
		call_function(op, subject, args)
		if dest: assign(dest)
		continue

	# just assignment or no op
	if not dest:
		if subject: output(f';{line_no}: no op {subject}')
	elif not subject: err('SyntaxError: Expected an expression.')
	elif subject.isdigit():
		output(f'\n;{line_no}:', line.strip())
		assign(dest, imm = subject)
	else:
		sclause, sreg = varinfo(subject, flags = GET_CLAUSE|GET_REG)
		output(f'mov {sreg}, {sclause}')
		assign(dest)
