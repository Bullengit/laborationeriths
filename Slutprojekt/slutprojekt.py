"""
Use this CLI tool to XOR-encrypt raw shellcode.
It reads shellcode from a file, applies XOR-encryption 
and saves the data in raw format, as Python array or C array.
The intended use is to obfuscate shellcode prior to its use in a payload chain.

Example:
    python slutprojekt.py -i example.bin -o output.enc -k key -f python.

This will create a file containing obfuscated shellcode in Python format.
"""
import argparse
import sys


# Functions that represent obfuscated shellcode in the chosen programming language.
def py_array(data):
    """
    Convert bytes into a Python array presentation.
    Output is formatted as a list with hexadecimal values, made
    for usage in Python source code.

    :param data: Obfuscated shellcode data in bytes.
    :type data: bytes
    :return: Python formatted shellcode array as a string.
    :rtype: str
    """
    hexlist = [f"0x{a:02x}" for a in data]
    return f"shellcode = [{','.join(hexlist)}]"

def c_array(data):
    """
    Convert bytes into a C-array presentation.
    Output is formatted as a list with hexadecimal values, made
    for usage in C source code.

    :param data: Obfuscated shellcode data in bytes.
    :type data: bytes
    :return: C formatted shellcode array as a string.
    :rtype: str
    
    """
    hexlist = [f"0x{a:02x}" for a in data]
    return f"unsigned char buf[] = {{{','.join(hexlist)}}};"

# The function that obfuscates the shellcode
def xor(data, key):
    """
    Applies XOR-obfuscation to a payload.
    The function reads binary data and XORs it with the provided key
    to produce an obfuscated payload suitable for shellcode usage.

    :param data: Payload data in bytes.
    :param key: XOR-key used for obfuscation.
    :return: XOR-obfuscated payload.
    """
    outputs = bytearray()
    for i in range(len(data)):
        outputs.append(data [i] ^ key[i % len(key)])
    return bytes(outputs)

#Main function with argparse arguments
def main ():
    """
    Program main function and entry point,
    Parses command-line arguments using argparse, reads raw shellcode
    from chosen input file, applies XOR-obfuscation by using specified key,
    and outputs the result in raw, Python array or C array format.
    """
    #Create an argparse-object to handle CLI arguments
    parser = argparse.ArgumentParser(description="XOR encryption for raw shellcode.")
    
    #Define input/output arguments, key and output format.
    parser.add_argument("-i", "--infile", dest="input_file", required=True,help="Input file containing raw shellcode")
    parser.add_argument("-o", "--outfile", dest="output_file", help="Output file for encrypted shellcode")
    parser.add_argument("-k", "--key", required=True, help="XOR key")
    parser.add_argument("-f", "--format", choices=["raw", "python", "c"], default="raw", help="Output-format")

    #Parse arguments provided by the user
    args = parser.parse_args()
   
    try: #Open and reads the input file as binaries.
        with open(args.input_file, "rb") as f:
            shellcode = f.read()
    except FileNotFoundError: #Error handling if the file does not exist.
        print("Error, file could not load.")
        sys.exit(1)

    if args.key.startswith("0x"): #Converts the key to integer if its entered in hexadecimal format.
        key = [int(args.key,16)]
    else:
        key = [ord(c) for c in args.key] #Else, convert each character to its ASCII-value

    crypt_data = xor(shellcode, key)

    if args.format ==  "python": #Output format according to selected format.
        result = py_array(crypt_data)
    elif args.format == "c":
        result = c_array(crypt_data)
    else:
        result = crypt_data #Default output is raw bytes if nothing else is chosen.

    if args.output_file:
        if args.format == "raw":
            mode = "wb"
        else:
            mode = "w"
        with open(args.output_file, mode) as f:
            f.write(result)
        print(f"Saved to {args.output_file}")
    else:
        print(result) #If no output file is specifed, print to terminal.

if __name__ == "__main__":
    main()