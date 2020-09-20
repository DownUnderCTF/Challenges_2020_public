from Crypto.Util.number import bytes_to_long, getPrime

flag = open('flag.txt', 'rb').read().strip()

p, q = getPrime(1024), getPrime(1024)
n = p*q
e = 0x10001

s = pow(557*p - 127*q, n - p - q, n)

c = pow(bytes_to_long(flag), e, n)

print(f'n = {n}')
print(f's = {s}')
print(f'c = {c}')
