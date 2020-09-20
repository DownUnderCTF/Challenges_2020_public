# Zombie Writeup

This is a medium heap exploit which involves exploiting a soundness hole in the rust type system. Everything is already set up for you, so you don't have to think too hard about the actual soundness hole though.

The idea here is that you first create a dangling reference to a freed block of memory on the heap. This is done through the `infect` command, which calls the `zombie` function with a user provided parameter.

```rust
fn zombie(size: usize) -> &'static mut [u8] {
	let mut object = vec![b'A'; size];
	let r = virus(object.as_mut());
	r
}
```
This zombie function first creates a heap allocated array filled with 0x41 of a user defined size, then calls the `virus` function.

This is a modification of rustlang issue 25860 as hinted in the code comments.

https://github.com/rust-lang/rust/issues/25860

This is a long standing hole in rust's (normally memory safe) type system which allows one to convert a reference lifetime to the static lifetime and therefore bypass rust's borrow checker: convert `&'a T` to `&'static T` and a big no-no for memory safety.

I have modified this to work with a mutable pointer so now there is a dangling reference which can be used to both read from, and write to the freed block of memory.

Usually this could be done easily using rust's `unsafe` keyword, but I decided to make this challenge extra baffling in exchange for source code access.

## The Challenge

The idea behind this challenge is that we have a shell with various commands, one of which is the "get flag" command, however that command is hardcoded to be ignored and a new command read in.

```rust
match line.as_str().trim() {
	"get flag" => continue,
	"infect" => infected = Some(infect(&mut lines)),
	"eat brains" => eat_brains(&mut lines, &mut infected),
	"inspect brains" => inspect_brains(&mut lines, &mut infected),
	_ => (),
}
```

after the command is finished executing there is another check to see if the command was "get flag", and if it was the flag is printed out.

```rust
if line.as_str().trim() == "get flag" {
	let flag = read_to_string("flag.txt").unwrap();
	println!("Here's the flag: {}", &flag);
}
```

So we need to change the command while it is still inside the buffer during the execution of one of our commands.

We also have other commands, "eat brains" and "inspect brains" which allow us to read from and write to our dangling reference returned from the `infect` function.

The final piece of the puzzle is understanding how the `String` struct works in rust. It contains a pointer to the heap, and will reallocate to grow when all the heap space for its buffer is used up. In this case we are reading stdin line by line, so if a line is longer than any have previously been, it is possible to force the String struct in the line variable to reallocate to a buffer that we have previously freed.

## The Exploit

First our normal setup:

```python
from pwn import *

p = remote("localhost", 1337)
```

Now our first step is to create our dangling pointer:

```python
p.sendline("infect")
p.sendline("32")
```

This will create a pointer to a 32 byte piece of freed memory and then store that in the `infected` variable in main.

```python
p.sendline("eat brains                     ")
```

Since the `.trim()` is called on each line before it is compared against the instructions, the trailing whitespace in this command will be ignored and the command recognised as "eat brains".

The purpose of the trailing whitespace here is to force the line containing this command to allocate a 32 byte buffer to store the command. This will take the buffer we have previously freed and have a dangling reference to back out of the freed bins and use it as part of the string buffer.

Now we have also entered the "eat brains" function at the same time, so we are able to modify the buffer that now contains the "eat brains                     " string.

The final piece of this puzzle is understanding how strings work in rust. Unlike in C, rust strings are not null terminated, instead the length of the string is stored alongside the pointer to the string and therefore in this case we do not have control over the length of the string.

If we simply replaced the first few bytes of the command buffer with the command we wanted and a null terminator we would end up with:
"get flag\x00s                     "

When this is `.trim()`ed the result would be "get flag\x00s" which would not match the required string "get flag". Instead we overwrite a few more bytes of the command with the space character:

```python
def brains(string):
	counter = 0
	for c in string:
		p.sendline(str(counter))
		p.sendline(str(ord(c)))
		counter += 1
	p.sendline("done")

brains("get flag  ")
```

Note the additional spaces at the end of the command, this will overwrite the "ns" in "brains" and cause the `.trim()` method to trim the command down to "get flag", which then prints the flag.
