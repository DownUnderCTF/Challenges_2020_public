from random import shuffle
from secret import secret_msg

ALPHABET = '0123456789abcdef'

class Cipher:
    def __init__(self, key):
        self.key = key
        self.n = len(self.key)
        self.s = 7

    def add(self, num1, num2):
        res = 0
        for i in range(4):
            res += (((num1 & 1) + (num2 & 1)) % 2) << i
            num1 >>= 1
            num2 >>= 1
        return res

    def encrypt(self, msg):
        key = self.key
        s = self.s
        ciphertext = ''
        for m_i in msg:
            c_i = key[self.add(key.index(m_i), s)]
            ciphertext += c_i
            s = key.index(m_i)
        return ciphertext

plaintext = b'The secret message is:'.hex() + secret_msg.hex()

key = list(ALPHABET)
shuffle(key)

cipher = Cipher(key)
ciphertext = cipher.encrypt(plaintext)
print(ciphertext)

# output:
# 85677bc8302bb20f3be728f99be0002ee88bc8fdc045b80e1dd22bc8fcc0034dd809e8f77023fbc83cd02ec8fbb11cc02cdbb62837677bc8f2277eeaaaabb1188bc998087bef3bcf40683cd02eef48f44aaee805b8045453a546815639e6592c173e4994e044a9084ea4000049e1e7e9873fc90ab9e1d4437fc9836aa80423cc2198882a
