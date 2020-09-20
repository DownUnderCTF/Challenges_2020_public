from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from os import urandom

flag = open('flag.txt', 'rb').read().strip()
flag = flag.lstrip(b'DUCTF{').rstrip(b'}')
assert len(flag) == 32

KEY = urandom(16)

def encrypt(msg, key, p0, c0):
    msg = pad(msg, 16)
    blocks = [msg[i:i+16] for i in range(0, len(msg), 16)]

    out = b''

    for p in blocks:
        c = strxor(p, c0)
        c = AES.new(key, AES.MODE_ECB).encrypt(c)

        out += strxor(p0, c)

        c0 = c
        p0 = p

    return out

msg = 'If Bruce Schneier multiplies two primes, the product is prime. On a completely unrelated note, the key used to encrypt this message is ' + KEY.hex()
ciphertext = encrypt(msg.encode(), KEY, flag[16:], flag[:16])

print('key = ' + KEY.hex())
print('ciphertext = ' + ciphertext.hex())
