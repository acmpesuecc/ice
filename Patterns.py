from re import compile as _compile
wsep  = _compile(r'\b')
hex   = _compile(r'[\da-fA-F]')
equal = _compile(r'(?<!=)=(?!=)')
empty = _compile(r'\[\][3-6]')

_shape = r'(?:(?:\[\d+\])*|\[\]|\**)'
_unit  = r'(?:[3-6]|[A-Za-z_]\w*)' # add tuple support
_label = rf'{_shape}{_unit}'
decl  = _compile(rf'(@({_label})\s+|{_shape}[3-6])([A-Za-z_]\w*)')
dest  = _compile(rf'(@{_label}\s+|{_shape}[3-6])?(\**)([A-Za-z_]\w*)'
		r'(?:\[([A-Za-z_]\w*|\d+)\])?')
token = _compile(rf'@(?P<label>{_label})|(?P<subject>\d+|[a-zA-Z_]\w*)'
	r'(?:\s*(?:\.\s*(?P<method>[a-zA-Z_]\w*)\s*)?\((?P<args>.*?)\)|'
	r'\[(?P<item>.*?)\]' ')?|'
	r'(?P<symbol>\S)')

stmt  = _compile(r'(([\'"])(\\?.)*?\2|[^#])*')
snip  = _compile(r'%(\d+|e)([RELSCNU]|(?P<reg>[sd]i|[ibs]p|[a-d]))?\b')

default = _compile(r'(?P<param>(?P<int>[3-6])|(?:(?P<arr>\[\d+\])|\*))'
		# (?#|[3-6])))
		rf'(?P<element>{_shape}(?:_?\w)*?)_(?P<method>[dm]\w*)')
