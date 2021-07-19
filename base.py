# Parses basic expressions and assignments
# And now can also parse declarations

# Flags for varinfo()
GET_CLAUSE = 0b100
GET_INT = 0b010
GET_REG = 0b001

from sys import argv
# if len(argv) <2: print('Input file not specified'); quit(1)
if len(argv)<2: argv.append('Examples/base tester.ice')
name = argv[1].rpartition('.')[0]
if len(argv)<3: argv.append(name+'.asm')

infile = open(argv[1])
out = open(argv[2], 'w')
def output(*args, file = out, **kwargs): print(*args, **kwargs, file = file)

import re
class Patterns:
	wsep  = re.compile(r'\b')
	decl  = re.compile(r'((?:\[\d+\])*[0-6])([A-Za-z_]\w*)')
	ident = re.compile(r'((\[\d+\])*[0-6])?([A-Za-z_]\w*)|\b\d+\b')

	stmt  = re.compile(r'(([\'"])(\\?.)*?\2|[^#])*')
	sub   = re.compile(r'(?i)%(\d+)([a-z])?\b')

def err(msg):
	print(f'File "{argv[1]}", line {line_no}')
	print('   ', line.strip())
	raise RuntimeError(repr(msg)) # temporary, for debugging

	print(msg)
	quit(1)

def split_shape(token):
	match = Patterns.decl.match(token)
	return match[1], match[2]

def new_var(token):
	shape, name = split_shape(token)
	var = Variable(shape, name)
	if name in variables:
		old_shape = variables[name].shape
		if old_shape == shape: return
		err(f'ValueError: {var.name!r} is already defined '
			f'with shape {old_shape!r}')

	variables[name] = var
	size = indexed_sizes[int(var.shape[-1])]

	output(var.enc_name+': res'+size, '1')

def varinfo(var, flags = GET_CLAUSE, reg = 'a'):
	if var not in variables: err(f'ValueError: {var!r} is not declared.')
	var = variables[var]
	size = int(var.shape[-1])
	out = ()
	if flags&GET_CLAUSE: out += (f'{size_list[size]} [{var.enc_name}]',)
	if flags&GET_INT: out += (1<<max(0, size-3),)
	if flags&GET_REG:
		reg_temp = reg_list[size]
		reg = reg_temp[0]+reg+reg_temp[1]
		out += (reg,)

	if len(out) == 1: return out[0]
	return out

def insert_snippet(fun, args = []): # dw this won't break
	sfile.seek(0)
	for line in sfile.readlines()[snippets[fun]:]:
		if line in (';', ';\n'): break

		offset = 0
		for match in Patterns.sub.finditer(line):
			start, end = match.span()
			start += offset
			end   += offset
			arg = args[int(match[1])]
			tail = match[2]

			if tail in 'abcd': sub = varinfo(arg, flags = GET_REG, reg = tail)
			elif not tail: sub = varinfo(arg)
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
		op = '_d'+op.strip()
	else: op = '_m'+op
	op = op.replace(' ', '__')

	label = variables[subject].labels[-1]
	if label[0] == '_' and label[1] != '_': label = label.replace('_', ' ', 1)
	label = label.replace('_', '__')
	label = label.replace(' ', '_')

	return label+op

class Variable:
	def __init__(self, shape, name):
		self.shape = shape
		self.name = name
		self.enc_name = self.var_encode()
		if len(shape) == 1: self.labels = ['_u']
		else:               self.labels = ['_a']

	def __repr__(self):
		return f'Variable({self.shape+self.name})'

	def var_encode(self):
		enc_name = self.name.replace('_', '__')
		return 'v_'+enc_name

variables = {}	# formerly the `shapes` dict

# byte if size <= 8, word if 16 ...
indexed_sizes = 'bbbbwdq'
size_list = ['byte', 'byte', 'byte', 'byte', 'word', 'dword', 'qword']
reg_list  = [' l', ' l', ' l', ' l', ' x', 'ex', 'rx']

sfile = open('builtins.ice-snippet')
snippets = {line[2:-1]: line_no for line_no, line in enumerate(sfile, 1)
	if line.startswith('; ')}
# starts at a line starting with '; ' (mind the space)
# ends at a line with just ';' (refer builtin methods and functions part)

print('BUILTINS: ', *snippets)

insert_snippet('_header')

# Writing to bss segment

output('\nsegment .bss')
for line_no, line in enumerate(infile, 1):
	decls = 0
	tokens = Patterns.stmt.match(line)[0].split()

	for token in tokens:
		if not token or token.isspace(): continue

		if Patterns.decl.match(token):
			new_var(token)
			decls += 1
		elif token.strip() == '=':
			if decls > 1:
				err('SyntaxError: Assignment with multiple declarations.')
			break
		elif decls:
			err('SyntaxError: Non-declaration token in declaration line.')
		else: break	# not a declaration line

print('VARIABLES:', *variables.values())

# Generating Assembly Code for Every Line of Source Code

# (some of) python's dunder names
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
	if Patterns.decl.match(dest): dest = split_shape(dest)[1]

	tokens = Patterns.wsep.split(exp)
	for token in tokens:
		if not token or token.isspace(): continue

		if Patterns.decl.match(token):
			err('SyntaxError: Cannot declare within expressions.')

		# expression lexing (still might need cleaning up)
		if not subject:
			D = Patterns.ident.match(token)
			if not D: err('SyntaxError: Invalid expression.')
			if D[1]: err('SyntaxError: Cannot declare within expressions')
			subject = token
		elif not op:
			token = token.strip()
			if token[0] == '(': op = '__call__'
			elif token == '.': op = False
			elif op == False: op = token
			elif token in symbols: op = symbols[token]
			elif not token: err('SyntaxError: Expected an operation.')
		elif token.isalnum(): args.append(token)

	# just assignment or no op
	if not op:
		if not dest:
			if subject: output(f'; no op {subject}')
		elif not subject: err('SyntaxError: Expected an expression.')
		elif subject.isdigit():
			dclause = varinfo(dest)
			output(f'\n;{line_no}:', line.strip())
			output(f'mov {dclause}, {subject}')
		else:
			sclause, sreg = varinfo(subject, flags = GET_CLAUSE|GET_REG)
			dclause, dreg = varinfo(dest, flags = GET_CLAUSE|GET_REG)
			output(f'mov {sreg}, {sclause}')
			output(f'mov {dclause}, {dreg}')
		continue

	output(f'\n;{line_no}:', line.strip())

	enc_op = fun_encode(subject, op)

	# builtin functions and methods
	if enc_op in snippets:
		insert_snippet(enc_op, args = [subject]+args)

		if dest: output(f'mov {varinfo(dest)}, {varinfo(dest, flags=GET_REG)}')
		continue

	# normal function calls
	offset = 0
	for arg in args:
		arg_clause, size = varinfo(arg, flags = GET_CLAUSE|GET_INT)
		output('push', arg_clause)
		offset += size

	if op != '__call__':
		subject_clause, size = varinfo(subject, flags = GET_CLAUSE|GET_INT)
		output('push', subject_clause)
		offset += size
		output('call', enc_op)
	else: output('call', subject)
	output('add esp,', offset)

	if dest: output(f'mov {varinfo(dest)}, {varinfo(dest, flags=GET_REG)}')