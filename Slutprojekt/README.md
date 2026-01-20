# XOR Shellcode Obfuscation Tool and CLI

This is a Python CLI tool that XOR-obfuscates raw shellcode.
The tool reads a file containing shellcode and applies XOR-obfuscation by using a user-defined key.
The output can be written in raw format, C-array or Python array. 
The intended usage is to obfuscate shellcode prior to its usage in a payload chain.

# Requirements

Python 3.x  
No external dependencies needed.

# User Syntax

python slutprojekt.py -i <input_file> -o <output_file> -k <key> -f <format>

# Available arguments

-i, --infile : input file containing raw shellcode (required)

-o, --outfile : output file for obfuscated shellcode

-k, --key : XOR key (string or hexadecimal, e.g. 0x42)

-f, --format : output format: raw, Python, or C (default: raw)

## Examples

# 1. Obfuscate shellcode and output raw bytes:
```bash
-> python slutprojekt.py -i shellcode.bin -o output.bin -k key
```
# 2. Obfuscate shellcode and output a Python array
```bash
-> python slutprojekt.py -i shellcode.bin -o output.py -k key -f python
```
Output can look like this: shellcode = [0x90, 0xeb, 0xfe]

# 3. Obfuscate shellcode using a hexadecimal key and output a C array:
```bash
-> python slutprojekt.py -i shellcode.bin -o output.c -k 0xAA -f c
```
Output can look like this: unsigned char buf[] = {0x90, 0xeb, 0xfe};

# 4. Print obfuscated shellcode directly to the terminal:
```bash
-> python slutprojekt.py -i shellcode.bin -k key -f python
```

## Notes
The tool is using XOR obfuscation and is not intended for cryptographic security.
It is designed for laboratory use, such as simple payload obfuscation.
Chosen output format determines if the result is written in raw bytes or formatted source code.

It reads raw shellcode from a chosen file, applies XOR obfuscation using a user-supplied key and the output 
results in raw, C array and Python array format through a command line interface.