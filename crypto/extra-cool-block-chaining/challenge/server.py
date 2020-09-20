#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
from os import urandom

flag = open('./flag.txt', 'rb').read().strip()
KEY = urandom(16)
IV = urandom(16)

def encrypt(msg, key, iv):
    msg = pad(msg, 16)
    blocks = [msg[i:i+16] for i in range(0, len(msg), 16)]
    out = b''
    for i, block in enumerate(blocks):
        cipher = AES.new(key, AES.MODE_ECB)
        enc = cipher.encrypt(block)
        if i > 0:
            enc = strxor(enc, out[-16:])
        out += enc
    return strxor(out, iv*(i+1))

def decrypt(ct, key, iv):
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    out = b''
    for i, block in enumerate(blocks):
        dec = strxor(block, iv)
        if i > 0:
            dec = strxor(dec, ct[(i-1)*16:i*16])
        cipher = AES.new(key, AES.MODE_ECB)
        dec = cipher.decrypt(dec)
        out += dec
    return out

flag_enc = encrypt(flag, KEY, IV).hex()

print('Welcome! You get 1 block of encryption and 1 block of decryption.')
print('Here is the ciphertext for some message you might like to read:', flag_enc)

try:
    pt = bytes.fromhex(input('Enter plaintext to encrypt (hex): '))
    pt = pt[:16] # only allow one block of encryption
    enc = encrypt(pt, KEY, IV)
    print(enc.hex())
except:
    print('Invalid plaintext! :(')
    exit()

try:
    ct = bytes.fromhex(input('Enter ciphertext to decrypt (hex): '))
    ct = ct[:16] # only allow one block of decryption
    dec = decrypt(ct, KEY, IV)
    print(dec.hex())
except:
    print('Invalid ciphertext! :(')
    exit()

print('Goodbye! :)')
