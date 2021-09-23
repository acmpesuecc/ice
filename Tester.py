from os import spawnl, P_WAIT
from os.path import expanduser
file = open('Test Cases.ice')
out  = open('Tests/Test01.ice', 'w')
test_no = 1
final = ''
L = len('(RETAIN) ')
pyw = expanduser(r'~\AppData\Local\Programs\Python\Python39\pythonw.exe')

def run_test():
	out.close()
	code = spawnl(P_WAIT, pyw, ' compiler.py', out.name)
	return code

def result(expect, suffix = ''):
	print(f'Line {line_no:02}: Wanted code {expect}. Got', code, suffix)

for line_no, line in enumerate(file, 1):
	if line.startswith('# '): print(f'\nTest {test_no}:', line[2:-1]); continue
	elif line == '\n':
		test_no += 1
		final = ''
		out = open(f'Tests/Test{test_no:02}.ice', 'w')
	else:
		endstr = line.partition('# ')[2]
		out.write(line)
		code = run_test()
		if endstr.startswith('(RETAIN)'):
			if not code: final += line
			result(0, code*'[FAILED] '+endstr.strip()[L*code:])
		else:
			result(1, (1-code)*'[FAILED] '+endstr.strip())
			out = open(out.name, 'w')
			out.write(final)
			out.close()
		out = open(out.name, 'a')

out.close()