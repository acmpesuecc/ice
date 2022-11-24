if 0:
	@6 hello_ptr
	@[]3 hello_arr = 'Hello, World!\x00'
hello_ptr = str(hello_arr)
println(hello_ptr)

6x = 8  # should fail, not yet declared
6x = str(x)

*4y = 55
6y = str(y)

println(x)
@str x
println(x)
println(hello_ptr)
@str hello_ptr
println(hello_ptr)

