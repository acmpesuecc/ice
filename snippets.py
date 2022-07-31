import Patterns
from misc import get_reg, err

def set_output(new_output):
	global output
	output = new_output

def read_snippets(new_sfile, CR_offset):
	global sfile, snippets
	sfile = new_sfile
	snippets = {}
	tell = 0
	for line_no, line in enumerate(sfile, 1):
		tell += len(line)+CR_offset
		if not line.startswith('; '): continue
		enc_name, ret_label, *arg_labels = line[2:].split()
		snippets[enc_name] = (tell, ret_label, arg_labels)
	# starts at a line starting with '; ' (mind the space)
	# ends at a line with just ';' (refer `snippets.insert()`)

def encode(name):
	match = Patterns.default.match(name)
	if not match: return name, None, None

	method = match['method']
	if   match['int']: enc_name = '_u'+method
	elif match['arr']: enc_name = '_a'+method
	else: enc_name = '_p'+method

	return enc_name, match['param'], match['element']

def decode_args(arg_labels, p, e) -> list[str]:
	arg_labels = arg_labels.copy()

	# TODO: add support for dynamic arrays

	if p == '*': p = '6'
	elif e: p = int(p[1:-1]); e = str(label_size(e))
	for i, size_n in enumerate(arg_labels):
		if   size_n == 's': arg_labels[i] = p
		elif size_n == 'e': arg_labels[i] = e
		else: arg_labels[i] = size_n

	return arg_labels

def get_label(enc_name, p, e): # use this if you know it's a snippet
	seek, ret_label, arg_labels = snippets[enc_name]
	if e is None: return ret_label
	return ret_label.replace('$e', e).replace('$s', p+e)

def insert(enc_name, args = (), p = None, e = None, match_args = True):
	seek, ret_label, arg_labels = snippets[enc_name]
	# if p:
	# ret_label = ret_label.replace('$e', e).replace('$s', p+e)
	# arg_labels, seek = snippet_setup(enc_name, args, p, e)
	if p: arg_labels = decode_args(arg_labels, p, e)

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
