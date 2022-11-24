labels = {'void': 0, 'str': 6}

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

def get_size(label):
	fac = 1
	num = ''
	for i, d in enumerate(label):
		if d.isidentifier(): num = labels[label[i:]]; break
		if d == '*': num = 6; break
		# add support for varrs (6, *d)
		if d == ']': fac *= int(num); num = ''
		elif d.isdigit(): num += d
	assert num != ''
	if num == 0: return 0
	return (fac<<(max(0, int(num)-3)))

def get_size_n(label):
	size = get_size(label)
	if size not in {1, 2, 4, 8}: return 0
	return size.bit_length()+2
	# fac = 1
	# num = ''
	# for i, d in enumerate(label):
	# 	if d.isidentifier(): num = labels[label[i:]].size_n; break
	# 	if d == '*': num = 6; break
	# 	# add support for varrs (6, *d)
	# 	if d == ']':
	# 		if num not in '1248': return 0  # no size_n
	# 		fac *= int(num); num = ''
	# 	elif d.isdigit(): num += d
	# assert num
	# size_n = int(num)
	# size = (fac<<(max(0, size_n-3)))
	# if size > 8: return 0
	# size_n += fac.bit_length()
	# return size_n

def element_size(label):
	if '*' in label: num = 8
	elif label[-1].isdigit(): num = 1<<max(0, int(label[-1])-3)
	else: num = 8

	# TODO: support named labels

	return num
