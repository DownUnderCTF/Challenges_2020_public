#!/usr/bin/env python3.8

import ecdsa
import random
import hashlib

Curve = ecdsa.NIST384p
G = Curve.generator
n = Curve.order

flag = open('flag.txt', 'r').read().strip()
auth_msg = b'I know alll of your secrets!'

def inv(z, n=n):
    return pow(z, -1, n)

def gen_keypair():
    d = random.randint(1, n-1)
    Q = d*G
    return d, Q

def sign(msg, d):
    x = int(hashlib.sha1(int.to_bytes(d, 48, byteorder='big')).hexdigest(), 16) % 2**25
    while True:
        k1 = (random.getrandbits(340) << 25) + x
        k2 = (random.getrandbits(340) << 25) + x
        r1 = (k1*G).x()
        r2 = (k2*G).y()
        if r1 != 0 or r2 != 0:
            break
    h = int(hashlib.sha384(msg).hexdigest(), 16)
    s = inv(k1)*(h*r1 - r2*d) % n
    return (r1, r2, s)

def verify(msg, Q, sig):
    if any(x < 1 or x >= n for x in sig):
        return False
    r1, r2, s = sig
    h = int(hashlib.sha384(msg).hexdigest(), 16)
    v1 = h*r1*inv(s)
    v2 = r2*inv(s)
    x1 = (v1*G + (-v2 % n)*Q).x()
    return (x1 - r1) % n == 0

def menu():
    m = '''Here are your options:
    [S]ign a message
    [V]erify a signature
    [P]ublic Key
    [Q]uit'''
    print(m)
    choice = input()[0].lower()
    if choice == 's':
        print('Enter your message (hex):')
        msg = bytes.fromhex(input())
        if len(msg) >= 8:            
            print('Message too long!')
            exit()
        sig = sign(msg, d)
        print(' '.join(map(str, sig)))
    elif choice == 'v':
        print('Enter your message (hex):')
        msg = bytes.fromhex(input())
        print('Enter your signature:')
        sig = [int(x) for x in input().split()]
        if verify(msg, Q, sig):
            if msg == auth_msg:
                print('Hello there authenticated user! Here is your flag:', flag)
                exit()
            else:
                print('Verified!')
        else:
            print('Invalid Signature!')
    elif choice == 'p':
        print(Q.x(), Q.y())
    else:
        print('Oh ok then... Bye!')
        exit()

d, Q = gen_keypair()

print('Welcome to my impECCable signing service.')
for _ in range(11):
    menu()
