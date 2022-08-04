# Modules
import Patterns
from misc import *
import labels
import functions
import snippets
sfile = open('builtins.ice-snippet')
snippets.read_snippets(sfile, crlf)

from sys import argv

if __name__ != '__main__': Shared.debug = True
elif '-d' in argv: Shared.debug = True; argv.remove('-d')
else: Shared.debug = False

if len(argv) <2:
	if Shared.debug: argv.append('Tests\\refactor tester.ice')
	else: print('Input file not specified'); quit(1)
name = argv[1].rpartition('.')[0]
if len(argv)<3: argv.append(name+'.asm')

infile = open(argv[1])
out = open(argv[2], 'w')
def output(*args, file = out, **kwargs): print(*args, **kwargs, file = file)
functions.set_output(output)
snippets.set_output(output)

variables = {}
keywords = {'while', 'endwhile'}

if Shared.debug:
	Shared.line_no = 0
	Shared.line = '[DEBUG] *Empty line*'
	print('BUILTINS: ', *snippets.snippets)

	class Debug:
		@staticmethod
		def set_snippets(new_snippets): global snippets; snippets = new_snippets
		@staticmethod
		def set_variables(new_variables): global variables; variables = new_variables
		@staticmethod
		def set_functions(new_functions): functions.set_functions(new_functions)
		@staticmethod
		def set_labels(new_labels): labels.set_labels(new_labels)
		@staticmethod
		def set_infile(new_infile): global infile; infile = new_infile
		@staticmethod
		def set_snippets(new_sfile, new_crlf = None):
			global sfile, snippets
			sfile = new_sfile
			if new_crlf is None: new_crlf = crlf
			snippets.read_snippets(sfile, new_crlf)
		@staticmethod
		def set_output_file(new_outfile):
			global output
			def output(*args, file = new_outfile, **kwargs):
				print(*args, **kwargs, file = file)
			snippets.set_output(output)
			functions.set_output(output)

def declare(label, name, init = None):
	if Patterns.empty.fullmatch(label):
		if init is None:
			err('SyntaxError: Implicit length requires initialisation.')
		init_length = len(init)//labels.element_size(label)
		label = label[0]+str(init_length)+label[1:]

	if name in variables: # check prev
		var = variables[name]
		size = labels.get_size(label)
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
		size = labels.get_size(label)
		# TODO: plural
		if len(init) != size:
			err(f'TypeError: {var.name!r} needs {size} bytes. '
				f'Got {len(init)} instead.')
		var.init = init

def get_var(name, label = None):
	if name.isdigit(): return Literal(label or '6', name)
	if name not in variables: err(f'NameError: {name!r} not defined.')
	return variables[name]

def uni_fill(uni_chain, label):
	for i, uni in enumerate(reversed(uni_chain), 1):
		if uni.isidentifier(): break
		uni_chain[-i] = functions.encode(label, unary[uni])
		label = functions.get_label(uni_chain[-i])

def parse(exp) -> 'size_n':
	uni_chain = []
	args = []
	label = None
	b_label = None
	bin_op  = None  # remembered for use after unary operations
	size_n  = 0

	if Shared.debug: output(f'\n;{Shared.line_no}:', Shared.line.strip())
	for token in Patterns.token.finditer(exp):
		if bin_op is True: # expecting a binary operator
			if token[0] not in binary:
				err('SyntaxError: Expected binary operator.')
			bin_op = functions.encode(b_label, binary[token[0]])
			continue

		if token['symbol']: # Expecting unary. Got some symbol.
			if token['symbol'] in '["\'':
				if bin_op or uni_chain: err('SyntaxError: '
					'Operations not yet supported on sequence literals.')
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
		if token['subject'] in keywords:
			err(f'Keyword {token["subject"]!r} not allowed in expression.')

		args = []
		enc_op = None
		if token['args'] is not None:  # required for empty arg lists
			if not token['method']:
				enc_op = functions.encode('', token['subject'])
			else:
				var = get_var(token['subject'])
				args.append(var)
				enc_op = functions.encode(var.get_label(), token['method'])
			label = functions.get_label(enc_op)
			arg_labels = functions.get_arg_labels(enc_op)[len(args):]
			for arg, arg_label in zip(token['args'].split(','), arg_labels):
				args.append(get_var(arg.strip(), arg_label))
		elif token['item']:
			var = get_var(token['subject'])
			enc_op = functions.encode(var.get_label(), '__getitem__')
			label = functions.get_label(enc_op)
			index_label = functions.get_arg_labels(enc_op)[1]
			index = get_var(token['item'], index_label)
			args.extend([var, index])
		else:
			var = get_var(token['subject'], label)
			label = var.get_label()

		uni_fill(uni_chain, label)

		# Call suffixes and uni_chain.
		if bin_op: output('mov rcx, rax')
		if enc_op is not None: functions.call(enc_op, args)
		elif uni_chain: functions.call(uni_chain.pop(), (var,))
		else: output(f'mov {get_reg("a", var.size_n)}, {var.get_clause()}')
		for enc_op in reversed(uni_chain):
			functions.call(enc_op, (Register(label, 'a'),))
			label = functions.get_label(enc_op)

		if bin_op is not None:
			arg_labels = functions.get_arg_labels(bin_op)
			if len(arg_labels) != 2: err('TypeError: '
				f'{bin_op!r} does not take 2 arguments')
			# if labels.get_size(arg_labels[1]) < labels.get_size(label):
			# 	err(f'TypeError: Incompatible size for {bin_op!r}')
			functions.call(bin_op,
				(Register(b_label, 'c'), Register(label, 'a')))
			b_label = functions.get_label(bin_op)
		elif uni_chain: b_label = functions.get_label(uni_chain[0])
		else: b_label = label

		label = None
		bin_op = True
		uni_chain = []

	return labels.get_size_n(b_label)

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
		fun = functions.encode(dest.get_label(), '__setitem__')
		arg_labels = functions.get_arg_labels(fun)
		if Shared.debug: print(f'{fun = }, {arg_labels = }, {index = }')
		
		if index.isdigit(): index = Literal(arg_labels[1], index)
		elif index not in variables: err(f'NameError: {index!r} not declared.')
		else: index = variables[index]

		functions.call(fun, (dest, index, imm or Register(arg_labels[2], 'a')))
		return

	# Use __setat__ when * in dest
	if len(deref) > 2:
		err("SyntaxError: Can't assign to multiple dereferences yet.")
	if deref:
		fun = functions.encode(dest.get_label(), '__setat__')
		label = functions.get_arg_labels(fun)[1]
		functions.call(fun, (dest, imm or Register(label, 'a')))
		return

	output(f"mov {dest.get_clause()}, {imm or get_reg('a', dest.size_n)}")

if __name__ == '__main__':
	snippets.insert('_header')

	# Writing to bss segment

	output('\nsegment .bss')
	for Shared.line_no, Shared.line in enumerate(infile, 1):
		stmt = Patterns.stmt.match(Shared.line)[0].strip()
		if Patterns.keywords.match(stmt): continue

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
		size = labels.element_size(decl[1])

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

	if Shared.debug: print('VARIABLES:', *variables.values())

	output()
	snippets.insert('_data')
	if Shared.debug: print('\nINITS:'); inits = False
	for var in variables.values():
		if not var.init: continue
		if Shared.debug: print(var.name, '=', var.init); inits = True

		output(var.enc_name, end = ': db ')
		out = repr(var.init)[12:-2].replace('`', '\\`')
		if '\\x' not in out: output(f'`{out}`')
		else: output(*var.init, sep = ', ')
	if Shared.debug and not inits: print(None)
	if Shared.debug: print()

	# Writing to the text segment

	ctrl_no = 0
	ctrl_stack = []

	infile.seek(0)
	output('\nsegment .text')
	output('main:')
	for Shared.line_no, Shared.line in enumerate(infile, 1):
		Shared.line = Patterns.stmt.match(Shared.line)[0]

		kw = Patterns.keywords.match(Shared.line)
		if kw:
			if kw[1] == 'endwhile':
				if kw[2]: err('SyntaxError: endwhile takes no expression')
				snippets.insert('_while_end', (ctrl_stack.pop(),))
			elif kw[1] == 'while':
				ctrl_literal = Literal('3', str(ctrl_no))
				snippets.insert('_while_precond', (ctrl_literal,))
				size_n = parse(kw[2])
				snippets.insert('_while_postcond', (ctrl_literal, Register(str(size_n), 'a')))
				ctrl_stack.append(ctrl_literal)
				ctrl_no += 1
			continue

		dest, _, exp = Shared.line.rpartition('=')
		dest = dest.strip()
		exp  = exp.strip()

		if not dest and Patterns.decl.match(exp): continue
		if not Shared.line.strip(): continue
		# if Shared.debug: print(f'{Shared.line_no}:', Shared.line.strip())
		isdecl = bool(Patterns.decl.match(dest))
		# decl = True
		if not exp or exp[0] not in '["\'': parse(exp)
		elif isdecl: dest = '' # sequence literals only initialise right now
		else: err('SyntaxError: Sequence literals '
			'not yet supported outside declaration.')

		# for no op (and for assignment also maybe?) check `label is None`
		if dest == '': continue
		elif not exp: err('SyntaxError: Expected an expression.')
		else: assign(dest) # TODO: optimize redundant `mov rax` assign(dest, var)
		output()

	snippets.insert('_exit')

	# print(f'Generated "{output.__kwdefaults__["file"].name}" successfully.')
