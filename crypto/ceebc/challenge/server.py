#!/usr/bin/env python3
from os import urandom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.backends import default_backend

backend = default_backend()

key = urandom(32)

solution_message = b'flagflagflagflag'


def CBC_MAC(key, message, iv):
    if len(message) != 16 or len(iv) != 16:
        raise ValueError('Only messages/IVs of size 16 are allowed!')
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    enc = cipher.encryptor()
    return enc.update(message) + enc.finalize()


def sign(message, iv):
    return CBC_MAC(key, message, iv) + iv


def verify(message, signature):
    iv = signature[16:]
    computed_sig = sign(message, iv)
    return constant_time.bytes_eq(signature, computed_sig)


sample = b'cashcashcashcash'
print('Hey there, have a message {} and its signature {}!'.format(
      sample.decode('utf-8'), sign(sample, urandom(16)).hex()
      ))

received_message = input('Now give me your message: ').encode('utf-8')
try:
    received_signature = bytes.fromhex(input('Now the signature (in hex): '))
except ValueError:
    print('Signature was not in hex!')
    exit()

try:
    valid = verify(received_message, received_signature)
except ValueError as e:
    print(e)
    exit()

if valid:
    print('Signature valid!')

    if received_message == solution_message:
        print(open('flag.txt').read())
    else:
        print('Phew! Good thing the message isn\'t {}!'
              .format(solution_message.decode('utf-8')))
else:
    print('Invalid signature!')
