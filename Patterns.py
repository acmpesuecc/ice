from re import compile as _compile
wsep  = _compile(r'\b')
hex   = _compile(r'[\da-fA-F]')
equal = _compile(r'(?<!=)=(?!=)')
# equal = _compile(r'((?<!=)|[-+*/&^|%]|<<|>>|//)=(?!=)')
empty = _compile(r'\[\][3-6]')

_shape = r'(?:(?:\[\d+\])*|\[\]|\**)'
_unit  = r'(?:[3-6]|[A-Za-z_]\w*)' # add tuple support
_label = rf'{_shape}{_unit}'
decl  = _compile(rf'(@({_label})\s+|{_shape}[3-6])([A-Za-z_]\w*)')
dest  = _compile(rf'(?:(@{_label}\s+|{_shape}[3-6])|((?:\*\s*)*))?([A-Za-z_]\w*)'
		r'(?:\[([A-Za-z_]\w*|\d+)\])?')
token = _compile(rf'@(?P<cast>{_label})|(?P<subject>\d+|[a-zA-Z_]\w*)'
	r'(?:\s*(?:\.\s*(?P<method>[a-zA-Z_]\w*)\s*)?\((?P<args>.*?)\)|'
	r'\[(?P<item>.*?)\]' ')?|'
	r'(?P<symbol>[!<=>]=|<<|>>|//|\S)')  # __pow__? ^^? but it isn't default...
keywords = _compile(r'\s*\b(if|elif|while|else)\b(.*?)(:\s*)?$')
function = _compile(rf'(@({_label})\s+|{_shape}[3-6])?(?P<name>[A-Za-z_]\w*)\s*'
					r'\((?P<args>.*?)\)\s*:')  # the colon decides if it's a fun

stmt  = _compile(r'(\s*)((?:\'(?:\\?.)*?\'|"(?:\\?.)*?"|[^#])*)')

_reg = r'[abcd]|[ds]i|[sbi]p|r(?:8|9|1[1-5])'
snip  = _compile(rf'%(\d+|e)([RELSCNU]|(?P<reg>{_reg}))?')
default = _compile(r'(?P<param>(?P<int>[3-6])|(?:(?P<arr>\[\d+\])|\*))'
		# (?#|[3-6])))
		rf'(?P<element>{_shape}(?:_?\w)*?)_(?P<method>[dm]\w*)')
call  = _compile(rf'%(\d)(?P<reg>{_reg})?\.(\w+)'
	r'\(((?:\s*%?\w+)?(?:\s*,\s*%?\w+)*\s*)\)')
