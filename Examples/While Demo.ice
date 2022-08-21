# Owing to while loops, Ice is now Turing Complete!
# The syntax still needs prettying up,
# so we use an 'endwhile' keyword instead of indentation


# Demo 1: print numbers from 1 to 100
3x = 0
while x < 100
	x = x + 1
	println(x)
endwhile

# String literals are only supported for initialization
# That's why we declare a variable to use the string
@[]3 space = " \x00"   # strings don't null terminate by default yet
println(space)  # print() and println() call printf under the hood
# and printf only works on null ending strings

# All these quirks will be fixed in the future, don't worry :)


# Demo 2: print the first 25 fibonacci numbers
3i = 0
6b = 1
@6 a c # everything is zero initialized by default
while i < 94
	c = a+b
	print(i)
	print(space)
	println(a)
	a = b
	b = c
	i = i + 1
endwhile
