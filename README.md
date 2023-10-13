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
I don't provide a binary yet, so you'll have to [download the repo files](https://github.com/cubed-guy/ice/archive/refs/heads/master.zip), and get [nasm](https://www.nasm.us/pub/nasm/snapshots/latest/) and [gcc](https://www.mingw-w64.org/downloads/).

**Note:** _For Windows, use [this direct link](https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-posix/seh/x86_64-8.1.0-release-posix-seh-rt_v6-rev0.7z) to download the gcc version that works for ice._


### Getting nasm and gcc on Arch Linux
_Yeah, I use arch btw._
```bash
$ sudo pacman -S nasm
$ sudo pacman -S gcc # if it isn't updated
```

## Usage
It isn't quite easy yet. There are a couple of the steps.

**Build on Windows**
```batch
> python3 <path_to_compiler>/compiler.py <ice_file_name>.ice <assembly_file_name>.asm
> <path to nasm> -fwin64 <assembly_file_name>.asm -o <object_file_name>.o
> <path to gcc> <object_file_name>.o -o <executable_file_name>.exe
```
`nasm` and `gcc` are found in their corresponding `bin` folders. Alternatively, you can add the `bin` folders to your path variables to avoid typing the path every time.

**Build on Linux (and perhaps macOS)**
```bash
$ python3 <path_to_compiler>/compiler.py <ice_file_name>.ice <assembly_file_name>.asm
$ nasm -felf64 <assembly_file_name>.asm -o <object_file_name>.o
$ gcc -no-pie <object_file_name>.o -o <binary_file_name>
```

#### Contributor
Sanket Padhi @cubed-guy
