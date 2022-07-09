*4pointer 4val
pointer = &val
val = 9200

@[]3 debug = 'val = '
print(debug)
printnum(val)


4p_val = pointer.__deref__()
@[]3 p_debug = 'p_val = '
print(p_debug)
printnum(p_val)

p_val = p_val.__add__(5)
@[]3 p_debug = 'p_val = '
print(p_debug)
printnum(p_val)
