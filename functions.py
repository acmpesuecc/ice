from misc import *
import snippets

functions = {}


def set_output(new_output):
	output = new_output
	return output

def set_functions(new_functions):
	functions = new_functions
	return functions
def encode(label, op):
	# check if label has that method?
	enc_op = op.replace('_', '__')
	if not label: return enc_op

	if len(op.lstrip('_'))+2 <= len(op) >= len(op.rstrip('_'))+2:
		enc_op = '_d'+enc_op[4:-4]
	else: enc_op = '_m'+enc_op

	label  = label.replace('_', '__')
	enc_op = label+enc_op
	return enc_op

def get_label(enc_op): # this works for any enc_op
        print(set_functions(new_functions))
	enc_op, p, e = snippets.encode(enc_op)
	if enc_op in snippets.snippets: return snippets.get_label(enc_op, p, e)

	# Is it possible for snippet encode to run if enc_op in functions?
	if enc_op not in functions:
		err(f'NameError: function {enc_op!r} not defined.')
	return functions[enc_op][0] # (ret_label, *arg_labels)

def get_arg_labels(enc_op):
        print(set_functions(new_functions))
	enc_op, p, e = snippets.encode(enc_op)
	if enc_op in snippets.snippets:
		seek, ret_label, arg_labels = snippets.snippets[enc_op]
		return snippets.decode_args(arg_labels, p, e)

	# Is it possible for snippet encode to run if enc_op in functions?
	if enc_op not in functions:
		err(f'NameError: function {enc_op!r} not defined.')
	return functions[enc_op][1:] # (ret_label, *arg_labels)

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
def call(enc_op, args : tuple[Variable] = ()):
        print(set_output(new_output))
        print(set_functions(new_functions))
	enc_op, p, e = snippets.encode(enc_op)

	if enc_op in snippets.snippets:
		snippets.insert(enc_op, args, p, e)
		if Shared.debug: print(f'  CALLED: {enc_op} (snippet) with {args}')
		return

	if enc_op not in functions:
		err(f'NameError: Function {enc_op!r} not defined.')

	arg_labels = functions[enc_op][1:]

	# TODO: plural
	if len(args) != len(arg_labels):
		err(f'TypeError: {enc_op!r} takes exactly {len(arg_labels)} arguments '
			f'({len(args)} given)')

	offset = -len(arg_regs)
	for arg in args:
		if not arg.size_n:
			err(f'TypeError: {arg.name!r} cannot be passed as an argument.')

		if offset >= 0: a('push', arg.get_clause())
		else:
			a(f'mov {get_reg(arg_regs[offset], arg.size_n)}, {arg.name}')
		offset += 1

	if offset > 0 and offset&1: offset += 1; output('sub rsp, 8')
	# if vector_fun: output(f'mov rax, {vectors}')
	output('push rbp')
	output('call', enc_op)
	output('pop rbp')
	if offset > 0: output('add rsp,', offset*8)

	if Shared.debug: print(f'  CALLED: {enc_op} (function) with {args}')
