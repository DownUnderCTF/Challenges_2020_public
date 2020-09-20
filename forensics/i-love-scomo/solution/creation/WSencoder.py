import binascii, sys

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def main(original, hidden, message):
    ofile = open(original, 'r') #original file
    hfile = open(hidden, 'w')   #hidden message file
    lines = ofile.readlines()
    h_bits = text_to_bits(message)
    if len(h_bits) < len(lines):
        i = 0
        for line in lines:
            if i < len(h_bits):
                hfile.write(line[:-1] + ' ' * int(h_bits[i]) + '\n')
            else:
                hfile.write(line)
            i += 1

        print("encoding hidden message complete!")
    else:
        print("The message is too long to be hidden in the original file")
    ofile.close()
    hfile.close()
    return 0


if __name__ == "__main__":
    try:
        original = sys.argv[1]
        hidden = sys.argv[2]
        message = sys.argv[3]
    except:
        print("You goofed something...")
        sys.exit(1)
    main(original, hidden, message)
