import binascii

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def main():
    hidden = input("What is the hidden file name  : ")
    hfile = open(hidden, 'r')
    lines = hfile.readlines()
    bits = ''
    zcount = 0
    for line in lines:
        line = line[:-1]
        if len(line) == 0:
            bits += '0'
            zcount += 1
        elif line[-1] == " ":
            bits += '1'
            zcount = 0
        else:
            bits += '0'
            zcount += 1
        if zcount >= 8:
            diff = len(bits) % 8
            if diff == 0:
                diff = 8
            bits = bits[:-diff]
            break
    if len(bits) > 0:
        text = text_from_bits(bits)
        print("your secret message is: " + text)
    else:
        print("no secret message in this file")

    hfile.close()
    return 0


if __name__ == "__main__":
    main()