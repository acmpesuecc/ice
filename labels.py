labels = {}

def set_labels(new_labels):
	global labels
	labels = new_labels

def get_length(label):
	# if label[0] == '*': return 1
	length = 1
	# TODO: add support for dynamic arrays
	for i in label[1:-2].split(']['):
		if not i: continue
		length *= int(i)
	return length

def get_size(label): # number of bytes
	fac = 1
	num = ''
	for i, d in enumerate(label):
		if d.isidentifier(): num = labels[label[i:]].size_n; break
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
