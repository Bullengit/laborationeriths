"""
CLI-verktyg som XOR-krypterar rå källkod.
Genom att läsa källkod från en fil,
XOR-kryptera och spara datan i råformat,
python-array eller c-array.
Tilltänkt användning är för obfuskering av shellcode innan du använder den i en payload-kedja.
"""
import argparse
import sys


# Funktioner som presenterar obfuskerad källkod i önskat språk.
def py_array(data):
    """
    Konverterar bytes till en python-lista med hexadecimaler,
    används för att visa obfuskerad data i python-kod.
    
    """
    hexlist = [f"0x{a:02x}" for a in data]
    return f"shellcode = [{','.join(hexlist)}]"

def c_array(data):
    """
    Konverterar bytes till en C-lista med hexadecimaler,
    används för att visa obfuskerad data i C-kod.
    
    """
    hexlist = [f"0x{a:02x}" for a in data]
    return f"unsigned char buf[] = {{{','.join(hexlist)}}};"

# Funktionen som obfuskerar shellcode
def xor(data, key):
    """
    Xor används för enkel payload-obfuskering.
    Data är filens innehåll i bytes, key är nyckeln för själva obfuskeringen,
    funktionen returnerar den obfuskerade datan.

    """
    outputs = bytearray()
    for i in range(len(data)):
        outputs.append(data [i] ^ key[i % len(key)])
    return bytes(outputs)

#Huvudprogram med argparse
def main ():
    """
    Programmets huvudfunktion,
    läser input från kommandoraden med argparse,
    öppnar en fil med rå shellcode,
    obfuskerar shellcode med XOR och vald nyckel,
    sparar eller skriver ut den krypterade datan i valt format.
    """
    #Skapar ett argparse-objekt för att handskas med CLI-argument
    parser = argparse.ArgumentParser(description="XOR encryption for raw shellcode.")
    
    #Här definerar vi argumenten, om det ska vara input eller output, nyckel och format. 
    parser.add_argument("-i", "--infile", dest="input_file", required=True,help="Input file containing raw shellcode")
    parser.add_argument("-o", "--outfile", dest="output_file", help="Output file for encrypted shellcode")
    parser.add_argument("-k", "--key", required=True, help="XOR key")
    parser.add_argument("-f", "--format", choices=["raw", "python", "c"], default="raw", help="Output-format")

    #Här läser den in argumenten som användaren skrivit in i terminalen.
    args = parser.parse_args()
   
    try: #öppnar och läser filen i binärt läge.
        with open(args.input_file, "rb") as f:
            shellcode = f.read()
    except FileNotFoundError: #Finns/hittas filen inte så körs felhanteringen.
        print("Error, file could not load.")
        sys.exit(1)

    if args.key.startswith("0x"): #konverterar nyckel till heltal om den är i hex.
        key = [int(args.key,16)]
    else:
        key = [ord(c) for c in args.key] #Annars konvertera alla tecken i strängen till ASCII-värde

    crypt_data = xor(shellcode, key)

    if args.format ==  "python": #formaterar output i valt format.
        result = py_array(crypt_data)
    elif args.format == "c":
        result = c_array(crypt_data)
    else:
        result = crypt_data #om inget format har valt så skrivs det ut i raw-bytes.

    if args.output_file:
        if args.format == "raw":
            mode = "wb"
        else:
            mode = "w"
        with open(args.output_file, mode) as f:
            f.write(result)
        print(f"Saved to {args.output_file}")
    else:
        print(result) #anges ingen outputfil, skrivs det i terminalen.

if __name__ == "__main__":
    main()