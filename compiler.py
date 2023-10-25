# Modules
import Patterns
from misc import *
import labels
import functions
import snippets

from sys import argv

if __name__ != '__main__': Shared.debug = True
elif '-d' in argv: Shared.debug = True; argv.remove('-d')
else: Shared.debug = False

if '-lf'   in argv: crlf = False; argv.remove('-lf')
if '-crlf' in argv: crlf = True;  argv.remove('-crlf')

sfile = open('builtins.ice-snippet')
snippets.read_snippets(sfile, crlf)

if len(argv) <2:
	# if Shared.debug: argv.append('Tests\\refactor tester.ice')
	if Shared.debug: argv.append('Examples\\Demo.ice')
	else: print('Input file not specified'); quit(1)
name = argv[1].rpartition('.')[0]
if len(argv)<3: argv.append(name+'.asm')

variables = {}

def set_output_file(new_outfile):
	global output, out
	out = new_outfile
	def output(*args, file = new_outfile, **kwargs):
		print(*args, **kwargs, file = file)
	snippets.set_output(output)
	functions.set_output(output)

if Shared.debug:
	Shared.line_no = 0
	Shared.line = '[DEBUG] *Empty line*'
	# print('BUILTINS: ', *snippets.snippets)

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

	var = Variable(label, name, setlabel = False)

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

def get_var(name):
	if name.isdigit():
		size_n = (int(name).bit_length()-1).bit_length()
		if size_n > 6: err(f'ValueError: Literal too big to fit in 64 bits.')
		var = Literal('6', name)
		if Shared.debug: print(f'  GOT VAR: {var}')
		return var
	if not name.isidentifier():
		err(f'SyntaxError: {name!r} is not a valid identifier.')
	if name not in variables: err(f'NameError: {name!r} not declared.')
	var = variables[name]
	if Shared.debug: print(f'  GOT VAR: {var}')
	return var

def uni_fill(uni_chain, label):
	for i, uni in enumerate(reversed(uni_chain), 1):
		if uni not in unary: break
		uni_chain[-i] = functions.encode(label, unary[uni])
		label = functions.get_label(uni_chain[-i])

def parse(exp) -> ('size_n', 'imm'):
	uni_chain = []
	args = []
	cast = None
	term_label = None
	exp_label = None  # label of the expression so far
	bin_op  = None  # operation to perform after parsing current term
	imm = None

	if Shared.debug: print('PARSE BEGIN')
	for token in Patterns.token.finditer(exp):
		if Shared.debug:
			print(f'  STATE: {cast = }, {term_label = }, {exp_label = }, '
				f'{bin_op = }, {imm = }')
			print(f'TOKEN: {token[0]!r}')

		if bin_op is EXPECTED:
			if token[0] not in binary:
				err('SyntaxError: Expected binary operator.')
			bin_op = functions.encode(exp_label, binary[token[0]])
			exp_label = None
			term_label = None
			continue

		if token['symbol']: # Expecting unary. Got some symbol.
			if token['symbol'] in '["\'':
				if bin_op or uni_chain: err('SyntaxError: '
					'Operations not yet supported on sequence literals.')
			if token['symbol'] not in unary:
				err(f'SyntaxError: Invalid unary operator {token["symbol"]!r}.')
			uni_chain.append(token['symbol'])
			if Shared.debug: print('  UNI CHAIN:', uni_chain)
			continue

		if token['cast']:
			uni_fill(uni_chain, token['cast'])
			if Shared.debug: print('  UNI CHAIN:', uni_chain)
			if term_label is None:
				if uni_chain: term_label = functions.get_label(uni_chain[0])
				else: term_label = token['cast']
			continue


		# Decode token

		if token['subject'] in keywords:
			err(f'Keyword {token["subject"]!r} not allowed in expression.')

		# token may have a suffix()[]
		args = []
		inner_label = None
		imm = None
		suffix_op = None
		if token['args'] is not None:  # required for empty arg lists
			if not token['method']:
				suffix_op = functions.encode('', token['subject'])
			else:
				var = get_var(token['subject'])
				args.append(var)
				suffix_op = functions.encode(var.get_label(), token['method'])
			inner_label = functions.get_label(suffix_op)
			arg_labels = functions.get_arg_labels(suffix_op)[len(args):]
			for arg, arg_label in zip(token['args'].split(','), arg_labels):
				if Shared.debug:
					print(f'  ARG: {arg.strip()!r} as @{arg_label}')
				arg = get_var(arg.strip())
				args.append(arg)
				if arg.get_label() is None:
					err(f'NameError: {arg.name!r} is not yet declared.')
			# if Shared.debug: print('  ARGS:', args)
		elif token['item']:
			var = get_var(token['subject'])
			if var.get_label() is None:
				err(f'NameError: {var.name!r} is not yet declared.')
			suffix_op = functions.encode(var.get_label(), '__getitem__')
			inner_label = functions.get_label(suffix_op)
			index_label = functions.get_arg_labels(suffix_op)[1]
			index = get_var(token['item'], index_label)
			if index.get_label() is None:
				err(f'NameError: {index.name!r} is not yet declared.')
			args.extend([var, index])
		else:
			var = get_var(token['subject'])
			if var.get_label() is None:
				err(f'NameError: {var.name!r} is not yet declared.')
			if isinstance(var, Literal) and not (bin_op or term_label):
				imm = var
			inner_label = var.get_label()

		if Shared.debug: print('STATE: inner_label =', inner_label)
		uni_fill(uni_chain, inner_label)

		# Call suffixes and uni_chain.
		if bin_op: output('mov rcx, rax')
		if suffix_op is not None: functions.call(suffix_op, args)
		elif uni_chain:
			enc_op = uni_chain.pop()
			if Shared.debug:
				print('STATE: arg_labels =', functions.get_arg_labels(enc_op))
			arg_label = functions.get_arg_labels(enc_op)[0]
			if Shared.debug: print('STATE: %r, %r', (arg_label, inner_label))
			if labels.get_size(arg_label) > labels.get_size(inner_label): err(
				f'TypeError: label {arg_label!r} is too big for casting. '
				f'Expected at most {labels.get_size(inner_label)}, '
				f'got {labels.get_size(arg_label)} bytes')

			functions.call(enc_op, (var,))
			inner_label = functions.get_label(enc_op)
			imm = None
		else:
			if term_label:
				if labels.get_size(term_label) > labels.get_size(inner_label):
				  err(
				    f'TypeError: label {term_label!r} is too big for casting. '
				    f'Expected at most {labels.get_size(inner_label)}, '
				    f'got {labels.get_size(term_label)} bytes')
			output(f'mov {get_reg("a", var.size_n, var)}, {var.get_clause()}')

		for enc_op in reversed(uni_chain):
			arg_labels = functions.get_arg_labels(enc_op)
			if len(arg_labels) != 1: err('TypeError: '
				f'{enc_op!r} does not take one argument')
			arg_label = arg_labels[0]
			# assuming arg_label != inner_label only if cast

			# TODO: correct size checking for real function calls
			if labels.get_size(arg_label) > labels.get_size(inner_label): err(
				f'TypeError: label {arg_label!r} is too big for casting. '
				f'Expected at most {labels.get_size(inner_label)}, '
				f'got {labels.get_size(arg_label)} bytes')
			functions.call(enc_op, (Register(arg_label, 'a'),))
			inner_label = functions.get_label(enc_op)

		if term_label is None: term_label = inner_label
		elif labels.get_size(term_label) > labels.get_size(inner_label): err(
				f'TypeError: label {term_label!r} is too big for casting. '
				f'Expected at most {labels.get_size(term_label)}, '
				f'got {labels.get_size(inner_label)} bytes')

		if bin_op is not None:
			arg_labels = functions.get_arg_labels(bin_op)
			if len(arg_labels) != 2: err('TypeError: '
				f'{bin_op!r} does not take 2 arguments')
			# if labels.get_size(arg_labels[1]) > labels.get_size(term_label):
			# 	err(f'TypeError: Incompatible size for {bin_op!r}. '
			# 		f'Expected at most {labels.get_size(term_label)}, '
			# 		f'got {labels.get_size(arg_labels[1])} bytes')
			functions.call(bin_op,
				(Register(arg_labels[0], 'c'), Register(arg_labels[1], 'a')))
			exp_label = functions.get_label(bin_op)
			imm = None

		# first term
		else: exp_label = term_label

		bin_op = EXPECTED
		uni_chain = []

	if Shared.debug:
		print(f'  STATE: {cast = }, {term_label = }, {exp_label = }, '
			f'{bin_op = }, {imm = }')
		print('PARSE END %r' % exp)
	if bin_op is not EXPECTED: err('SyntaxError: Invalid expression.')
	return labels.get_size_n(labels.get_size(exp_label)), imm

def assign(dest, size_n, imm: Literal = None):
	# TODO: get LHS (assuming rax rn)
	match = Patterns.dest.match(dest)
	deref, dest, index = match[2], match[3], match[4]
	# print(dest, (var, index), sep = ' -> ')

	if Shared.debug: print(f'ASSIGN: {dest = }, {size_n = }, {imm = }')

	if dest.isdigit(): err("SyntaxError: Can't assign to literal.")

	if dest not in variables: err(f'NameError: {dest!r} not declared.')
	dest = variables[dest]
	if dest.get_label() is None:
		err(f'NameError: {dest.name!r} not yet declared.')

	if index:
		if deref: err("SyntaxError: Can't assign to multiple operations yet.")
		fun = functions.encode(dest.get_label(), '__setitem__')
		arg_labels = functions.get_arg_labels(fun)
		# if Shared.debug: print(f'{fun = }, {arg_labels = }, {index = }')
		
		index = get_var(index)

		val = imm or Register(arg_labels[2], 'a')

		functions.call(fun, (dest, index, val))
		return

	# Use __setat__ when * in dest
	if deref:
		if len(deref.strip()) >= 2:
			err("SyntaxError: Can't assign to multiple dereferences yet.")
		fun = functions.encode(dest.get_label(), '__setat__')
		label = functions.get_arg_labels(fun)[1]

		val = imm or Register(label, 'a')
		functions.call(fun, (dest, val))
		return

	# if not imm and dest.size_n != size_n:
	# 	err('TypeError: assignment sizes do not match')
	if dest.size_n == 0: err('TypeError: invalid destination size.')

	if imm is not None:
		# assert isinstance(imm, Literal)

		size_n = (int(imm.name).bit_length()-1).bit_length()
		if dest.size_n < size_n:
			err(f'ValueError: {imm.name} does not fit in '
				f'label {dest.get_label()!r}')

		output(f'mov {dest.get_clause()}, {imm.name}'); return

	elif dest.size_n < size_n:
		size_n = dest.size_n  # only look at the low bits (for little endian)

	src_a  = get_reg('a', size_n)
	src_b  = get_reg('b', size_n)
	dest_a = get_reg('a', dest.size_n)
	dest_b = get_reg('b', dest.size_n)

	if dest.size_n == size_n:
		output(f'mov {dest.get_clause()}, {dest_a}')
	elif size_n < 5: # @Optimization
		output(f'movzx {dest_a}, {src_a}')
		output(f'mov {dest.get_clause()}, {dest_a}')
	else:
		output(f'xor {dest_b}, {dest_b}')
		output(f'mov {src_b}, {src_a}')
		output(f'mov {dest.get_clause()}, {dest_b}')

def dedent(indent_stack, branch_stack, ladder_stack, end = True):
	indent_stack.pop()
	if not end: return
	branch_id = branch_stack.pop()
	if branch_id is WHILE_BRANCH:
		snippets.insert('_while_end', (ladder_stack.pop(),))
	else:
		snippets.insert('_if_end', (ladder_stack.pop(), branch_id))
	# if Shared.debug: print(f'DEDENT: {ladder_stack = }, {branch_stack = }')

class passes:
	@staticmethod
	def declaration():
		# Writing to bss segment

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
						match = Patterns.decl.match(decl)
						if not match:
							err(f'SyntaxError: Expected a declaration token.')
						if match[2]: err('SyntaxError: '
							f'{decl!r} @ declarations not allowed '
							'for inline multi-declaration.')
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

	@staticmethod
	def data():
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

	@staticmethod
	def codegen(*, is_function = False, start_line = 1, function_locals = {}):
		# Writing to the text segment

		next_ladder_id = 0
		ladder_stack = []
		branch_stack = []

		indent_stack = ['']
		prev_indent  = ''
		expect_indent = is_function
		skipping_function = False

		label_level = 0

		for Shared.line_no, Shared.line in enumerate(infile, start_line):
			match = Patterns.stmt.match(Shared.line)
			if not match: err('SyntaxError: EOL in string')  # only possibility?

			curr_indent, Shared.line = match[1], match[2]
			if not Shared.line.rstrip(): continue

			if skipping_function:
				# requires function definitions to be at outermost indentation
				# label definitions will also get skipped after I implement them
				if curr_indent == '': skipping_function = False
				else: continue

			if Shared.debug:
				print('\nLINE %d: %r' % (Shared.line_no, Shared.line))
				output('\n; %d: %r' % (Shared.line_no, Shared.line))

			kw = Patterns.keywords.match(Shared.line)

			if expect_indent:
				if (curr_indent == prev_indent
					or not curr_indent.startswith(prev_indent)):
					err('IndentationError: Expected indent block.')
				indent_stack.append(curr_indent)
				label_level += 1
				expect_indent = False
			elif curr_indent != prev_indent:
				for dedents, indent in enumerate(reversed(indent_stack), 0):
					if curr_indent == indent: break
				else: err('IndentationError: '
					'Current indentation does not match any outer indentation')

				# if Shared.debug: print('DEDENT - MULTIPLE:',
				# 	f'{len(branch_stack) = }',
				# 	f'{len(ladder_stack) = }',
				# 	f'{dedents = }',
				# )
				for i in range(dedents-1):
					dedent(indent_stack, branch_stack, ladder_stack)
				# if Shared.debug: print('DEDENT - LAST:',
				# 	f'{len(branch_stack) = }',
				# 	f'{len(ladder_stack) = }',
				# )
				dedent(indent_stack, branch_stack, ladder_stack,
					end = not (kw and kw[1] in elses))

				label_level -= dedents
				if Shared.debug: print('LABEL LEVEL = ', label_level)
				for var in variables:
					get_var(var).set_label_level(label_level)

				if is_function and label_level == 0: break  # stop reading file

			# if Shared.debug: print(f'INDENT: {indent_stack = } '
			# 	f' from {prev_indent!r} to {curr_indent!r}')
			prev_indent = curr_indent


			function = Patterns.function.match(Shared.line)
			if function is not None:
				if is_function:
					err('SyntaxError: local functions are not allowed.')
				if curr_indent != '':
					err('SyntaxError: functions are not allowed in constructs')

				skipping_function = True
				continue

			if kw is None:
				# handle shorthand assignments += -= *= /= %= &= |= ^= <<= >>= //=
				dest, _, exp = Shared.line.rpartition('=')
				dest = dest.strip()
				exp  = exp.strip()

				
				# no destination, only declaration
				decl = Patterns.decl.match(exp)
				if not dest and decl:
					if Shared.debug: print(f'DECL ONLY: {decl} '
						f'(dest: {Patterns.decl.match(dest)})')

					if decl[2]:
						label = decl[2]
						# accepts multi non-@ decl
						get_var(decl[3]).set_label(label, label_level)
						for var in exp.split()[2:]:
							get_var(var).set_label(label, label_level)
						continue

					label = decl[1]
					for decl in exp.split():
						match = Patterns.decl.match(decl)
						label, var = match[1], match[3]
						get_var(var).set_label(label, label_level)
					continue

				# (re)declaration with assignment
				decl = Patterns.decl.match(dest)
				if decl:
					if Shared.debug: print(f'DECL DEST: {decl} '
						f'(exp: {Patterns.decl.match(exp)})')
					label = decl[2] or decl[1]
					var = get_var(decl[3])
					var.set_label(label, label_level)

				if not exp or exp[0] not in '["\'': size_n, imm = parse(exp)
				elif decl: dest = '' # sequence literals only initialise right now
				else: err('SyntaxError: Sequence literals '
					'not yet supported outside declaration.')

				# for no op (and for assignment also maybe?) check `label is None`
				if dest == '': continue
				elif not exp: err('SyntaxError: Expected an expression.')
				else: assign(dest, size_n, imm) # TODO: optimize redundant `mov rax` assign(dest, var)
				continue

			# Keyword Statements

			if   kw[1] == 'while':
				if not kw[2]: err('SyntaxError: no condition given in while')
				ladder_id = Literal('3', str(next_ladder_id))
				snippets.insert('_while_precond', (ladder_id,))
				size_n, imm = parse(kw[2])
				snippets.insert('_while_postcond',
					(ladder_id, Register(str(size_n), 'a')))
				ladder_stack.append(ladder_id)
				branch_stack.append(WHILE_BRANCH)
				next_ladder_id += 1
				if Shared.debug:
					print(f'while: {ladder_stack = }, {branch_stack = }')
			elif kw[1] == 'if':
				if not kw[2]: err('SyntaxError: no condition given in if')
				ladder_id = Literal('3', str(next_ladder_id))
				branch_id = Literal('3', '0')
				size_n, imm = parse(kw[2])
				snippets.insert('_if',(
					ladder_id, branch_id, Register(str(size_n), 'a')))
				ladder_stack.append(ladder_id)
				branch_stack.append(branch_id)
				next_ladder_id += 1
				if Shared.debug:
					print(f'if:    {ladder_stack = }, {branch_stack = }')
			elif kw[1] == 'elif':
				ladder_id = ladder_stack[-1]
				branch_id = branch_stack[-1]
				if branch_id is WHILE_BRANCH:
					err('SyntaxError: elif not allowed after while')
				snippets.insert('_else', (ladder_id, branch_id))
				size_n, imm = parse(kw[2])
				branch_id.name = str(int(branch_id.name)+1)
				snippets.insert('_if', (
					ladder_id, branch_id, Register(str(size_n), 'a')))
				if Shared.debug:
					print(f'elif:  {ladder_stack = }, {branch_stack = }')
			elif kw[1] == 'else':
				if kw[2]: err('SyntaxError: else takes no expression')
				ladder_id = ladder_stack[-1]
				branch_id = branch_stack[-1]
				if branch_id is WHILE_BRANCH:
					err('SyntaxError: else not yet supported after while')
					snippets.insert('_while_else', (ladder_id,))
				# else: snippets.insert('_if_else', (ladder_id, branch_id))
				else: snippets.insert('_else', (ladder_id, branch_id))
				branch_id.name = str(int(branch_id.name)+1)
				if Shared.debug:
					print(f'else:  {ladder_stack = }, {branch_stack = }')
			else:
				# return, break, continue etc. those that don't end with ':'
				err(f'SyntaxError: {kw[1]} is not yet supported.')
				output()
				continue
			if not kw[3]: err(f'SyntaxError: Colon required at the end of {kw[1]}')
			expect_indent = True

			output()

		if expect_indent:
			err('IndentationError: Expected indentation, got EOF instead.')
		while len(indent_stack) > 1:
			dedent(indent_stack, branch_stack, ladder_stack)

def call_function(function_name, args):
    # Function Prologue
    output(f"push rbp")
    output(f"push rbx")

    # Load function arguments into registers
    for i, arg in enumerate(args):
        output(f"mov {get_reg('a', arg.size_n, arg)}, {arg.get_clause()}")

    # Function Call
    output(f"call {function_name}")

    # Function Epilogue
    output(f"pop rbx")
    output(f"pop rbp")

    # Handle return value (if any)
    output(f"mov rax, <return_value_register>")

# Example function call
args = [get_var("arg1"), get_var("arg2")]
call_function("my_function", args)


if __name__ == '__main__':
	infile = open(argv[1])
	out = open(argv[2], 'w')
	set_output_file(out)

	snippets.insert('_header')
	infile.seek(0)
	output('\nsegment .bss')
	passes.declaration()
	passes.data()
	output('\nsegment .text')
	output('main:')

	infile.seek(0)
	passes.codegen()
	snippets.insert('_exit')

	# print(f'Generated "{output.__kwdefaults__["file"].name}" successfully.')
