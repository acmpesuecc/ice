# Single Strings
println('String')  # (DELETE) strings not supported as args
hello('String')    # (DELETE) strings not supported as args
hello('Str = ing') # (DELETE) '=' in the string shouldn't cause assignment
[]3hello = 'String'# (RETAIN) correct string init
[]3hello= 'String' # (RETAIN) whitespace shouldn't mess it up
[]3hello ='String' # (RETAIN) whitespace shouldn't mess it up
[]3hello='String'  # (RETAIN) whitespace shouldn't mess it up
[]3hello = 'Hello' # (DELETE) init string doesn't match
'String' = hello   # (DELETE) assignment to string shouldn't work

# Double Strings
println("String")  # (DELETE) strings not supported as args
hello("String")    # (DELETE) strings not supported as args
hello("Str = ing") # (DELETE) '=' in the string shouldn't cause assignment
[]3hello = "String"# (RETAIN) correct string init
[]3hello= "String" # (RETAIN) whitespace shouldn't mess it up
[]3hello ="String" # (RETAIN) whitespace shouldn't mess it up
[]3hello="String"  # (RETAIN) whitespace shouldn't mess it up
[]3hello = "Hello" # (DELETE) init string doesn't match
"String" = hello   # (DELETE) assignment to string shouldn't work

# Declarations
3uint              # (RETAIN) uint decl
[24]3var           # (RETAIN) array declaration
[4][6]3var         # (RETAIN) 2D array declaration
[]3var             # (DELETE) implicit length without init
[5]3hello = 'Hello'# (RETAIN) correct string initialisation
[]3hello = 'Hello' # (RETAIN) implicit length string initialisation
[6]3hello = 'Hello'# (DELETE) incorrect length string initialisation

# Arrays?
[]3var = []        # (DELETE) empty array
[0]3var            # (DELETE) empty array
