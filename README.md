# Ice

Compiled languages are usually statically typed because the compiler needs to know the size of the variable beforehand. Ice takes this literally, and the only part of a variable's type that is static is its size. Ice allows us to change the type of the variable.\
These are called _labels_ in ice.

```Perl
@str msg = 'Hello, World!' # @str is a label of size 64 bits since it's a 64-bit pointer.
print(msg) # -> Hello, World!

@bytes msg # We change the type of the variable here. Now it acts as a pointer to an array.
print(msg) # -> [72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33]
```

Ice is a compiled language and tries to be everything like python, unless types/labels are involved.

More details are in the [wiki](../../wiki)

## Installation
Haven't cleaned this part yet, so you'll have to download the repo files. You'll also need [nasm](https://www.nasm.us/pub/nasm/snapshots/latest/) and [gcc](https://www.mingw-w64.org/downloads/).


### Getting nasm and gcc on Arch Linux
_Yeah, I use arch btw._
```bash
$ sudo pacman -S nasm
$ sudo pacman -S gcc # if it isn't updated
```

## Usage
It isn't quite easy yet. There are a couple of the steps.

**Build on Windows**
First add the nasm and gcc bin folders to your path.
```batch
> python3 <path_to_compiler>/compiler.py <ice_file_name>.ice <assembly_file_name>.asm
> nasm -fwin64 <assembly_file_name>.asm -o <object_file_name>.o
> gcc -no-pie <object_file_name>.o -o <executable_file_name>.exe
```

**Build on Linux (and perhaps macOS)**
```bash
$ python3 <path_to_compiler>/compiler.py <ice_file_name>.ice <assembly_file_name>.asm
$ nasm -felf64 <assembly_file_name>.asm -o <object_file_name>.o
$ gcc -no-pie <object_file_name>.o -o <binary_file_name>
```

