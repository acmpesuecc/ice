# Here's just a comment. It should be ignored.

3newVar
[2]3newArr # inline comment

# multiple assignments in a line
*33newVarr *223guavarrPointer

@*33thisLabel:
	3firstFunc(self, 3arg):
	  3localVar = 2
	  localVar += arg
	  return localVar

	[2]3secondFunc(self):
		3firstReturn
		3secondReturn
		firstReturn = 3
		secondReturn = 4

		[2]3out

		out[0] = firstReturn
		out[1] = secondReturn
		return out

@thisLabel newVarr

@*223guavarrLabel(thisLabel):
	2orange(self): return 2

	procedure(self, 2w, 2h, 3val):
		[w][h]self
		for 2x in range(w): # not sure yet how for should work
			# now, an inline control block
			for 2y in range(h): 3oval = val; self[x][y] = oval
	# The first indentation level under a label head must contain
	# only function heads. Need to implement that as well.

3loneFunction(2x, 2y):
	return guavarrPointer[x][y]

@guavarrLabel guavarrPointer

guavarrPointer.procedure(3, 6, 12)

newVar = loneFunction(2, 0)

print(newVarr.firstFunc(newVar))
# Some sort of *args syntax can be implemented.
# Not the same syntax of course, because `*` is used for pointers.
