# In a pickle
We are provided with a data file which contains a string `I know that the intelligence agency's are onto me so now I'm using ways to evade them: I am just glad that you know how to use pickle. Anyway the flag is` which is seen in cleartext along with `DUCTF{}` however the rest of the contents are unreadable and taking a hint from the name of the challenge we figure out that the challenge has something to do with the python pickle library:

```python
import pickle
pickle_in = open("data", "rb")
data = pickle.load(pickle_in)
print(data)
```

Using the above script gives us the following output:

```
{1: 'D', 2: 'UCTF', 3: '{', 4: 112, 5: 49, 6: 99, 7: 107, 8: 108, 9: 51, 10: 95, 11: 121, 12: 48, 13: 117, 14: 82, 15: 95, 16: 109, 17: 51, 18: 53, 19: 53, 20: 52, 21: 103, 22: 51, 23: '}', 24: "I know that the intelligence agency's are onto me so now i'm using ways to evade them: I am just glad that you know how to use pickle. Anyway the flag is "}
```

We see that loading the pickle file gives us a python dictionary as an output. However, the flag is still obfuscated.

Attempting to use `chr()` against the values give us some ascii letters which can be used in a script to completely decode the flag.

```python
import pickle
pickle_in = open("data", "rb")
data = pickle.load(pickle_in)
flag = "DUCTF{"
for i in range(4,23):
	flag += chr(data[i])
flag += "}"
print(flag)
```

## Flag:

```
DUCTF{p1ckl3_y0uR_m3554g3}
```
