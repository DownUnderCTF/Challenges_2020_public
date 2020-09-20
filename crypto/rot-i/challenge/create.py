from string import ascii_lowercase, ascii_uppercase

flag = open('flag.txt', 'r').read().strip()
msg = "You've solved the beginner crypto challenge! The flag is {}. Now get out some pen and paper for the rest of them, they won't all be this easy :).".format(flag)

def eNCryPt(msg):
    out = ''
    for i, c in enumerate(msg):
        if c in ascii_lowercase:
            alph = ascii_lowercase
        elif c in ascii_uppercase:
            alph = ascii_uppercase
        else:
            out += c
            continue
        out += alph[(alph.index(c) + i) % len(alph)]
    return out

print(eNCryPt(msg))
