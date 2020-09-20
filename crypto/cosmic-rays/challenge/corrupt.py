# reads 2 lines from stdin, outputs the same content with some characters corrupted
"""
key = <32 hex>
ciphertext = <352 hex>
"""

def corrupt_one(txt, idx):
    return txt[:idx] + '▒' + txt[idx+1:]

def corrupt(txt, idxs):
    for i in idxs:
        txt = corrupt_one(txt, i)
    return txt

key_line = input().strip()
assert len(key_line) == 38

ciphertext_line = input().strip()
assert len(ciphertext_line) == 365

key_corrupt_idxs = [2, 7, 19, 36]
key_line_corrupted = corrupt(key_line, key_corrupt_idxs)

ciphertext_corrupt_idxs = [2, 6] + list(set(range(46, 333)) - {47, 50, 57, 63, 69, 77, 78, 84, 89, 94, 104, 106, 108, 131, 145, 167, 170, 174, 180, 183, 189, 200, 203, 205, 206, 209, 222, 225, 239, 240, 243, 245, 251, 254, 257, 260, 263, 268, 274, 280, 289, 293, 299, 301, 304, 309, 311, 314, 316, 319, 321, 322, 324, 325, 326, 327, 328, 330, 331} | {337, 351})
ciphertext_line_corrupted = corrupt(ciphertext_line, ciphertext_corrupt_idxs)

print(key_line_corrupted)
print(ciphertext_line_corrupted)
