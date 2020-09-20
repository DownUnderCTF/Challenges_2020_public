# added protection


This challenge is about reverse engineering encrypted shellcode.

It includes a snippet of hand written shellcode, encrypted with a very typical xor + add encoding algorithm, and finally injected into memory via `mmap` and `memcpy` to execute.

There are many ways to solve this - static analysis is one of them. One can analyze this very simple and small program, extract the shellcode, and attempt to write a decoding algorithm based on the logic in the binary.

Of course, a faster way would be to run it in GDB, set breakpoints after the shellcode is decrypted, and inspect the content.

Feel free to have a go yourself before continuing.

## analyzing the program

My preferred way is `gdb`. I like to first decompile programs when playing RE challenges, so I used retdec decompiler (you can also use ghidra) to decompile it. This is the snippet of `main` from retdec:

```c
// Address range: 0x1175 - 0x12a9
int main(int argc, char ** argv) {
    // 0x1175
    fprintf(g5, "size of code: %zu\n", 130);
    for (int64_t i = 0; i < 65; i++) {
        int16_t * v1 = (int16_t *)(2 * i + (int64_t)&g4); // 0x11cf
        uint16_t v2 = *v1 ^ -0x4111; // 0x11d2
        *v1 = (v2 < 42 ? -43 : -42) + v2;
    }
    int64_t * v3 = mmap(NULL, 130, 7, 34, -1, 0); // 0x1252
    if (v3 != (int64_t *)-1) {
        // 0x1278
        memcpy(v3, &g4, 130);
        return 0;
    }
    // 0x1262
    perror("mmap");
    exit(1);
    // UNREACHABLE
}
```

So funny enough, retdec didn't actually pick up the fact that the shellcode was *executed*. This was the snippet from ghidra, which is more accurate (but in my opinion, less readable than retdec):

```c
undefined8 main(void)

{
  ushort *puVar1;
  code *__dest;
  ulong local_10;
  
  fprintf(stderr,"size of code: %zu\n",0x82);
  local_10 = 0;
  while (local_10 < 0x41) {         // <--------------- decoding routine
    puVar1 = (ushort *)(code + local_10 * 2);
    *puVar1 = *puVar1 ^ 0xbeef;
    if (*puVar1 < 0x2a) {
      *puVar1 = *puVar1 - 0x2b;
    }
    else {
      *puVar1 = *puVar1 - 0x2a;
    }
    local_10 = local_10 + 1;
  }
  __dest = (code *)mmap((void *)0x0,0x82,7,0x22,-1,0);
  if (__dest == (code *)0xffffffffffffffff) {
    perror("mmap");
                    // WARNING: Subroutine does not return
    exit(1);
  }
  memcpy(__dest,code,0x82);         // <-------------- MEMCPY 
  (*__dest)();                      // <-------------- shell code executed
  return 0;
}
```

So you can see by the labeled sections above that memcpy was called on the code to the `__dest` location before it was executed. This is because anything encrypted has to be decrypted before it executes, which is the nature of all malware.

## debugging it in gdb 

Now we run it in gdb.

`gdb -q ./added_protection`

Starting off with disassembling the main function, to identify where to set our breakpoints:

```
(gdb) disass main

... snipped 
   0x000000000000128a <+277>:   callq  0x1050 <memcpy@plt> ; memcpy called here
   0x000000000000128f <+282>:   mov    -0x18(%rbp),%rax
   0x0000000000001293 <+286>:   mov    %rax,-0x20(%rbp)
   0x0000000000001297 <+290>:   mov    -0x20(%rbp),%rdx
   0x000000000000129b <+294>:   mov    $0x0,%eax
   0x00000000000012a0 <+299>:   callq  *%rdx               ; shellcode called here 
   0x00000000000012a2 <+301>:   mov    $0x0,%eax
   0x00000000000012a7 <+306>:   leaveq
   0x00000000000012a8 <+307>:   retq
```

So at main+299, the shellcode would've been fully decrypted and copied into memory. We set the breakpoint there.

```
(gdb) b *main+299
```

use `r` is to run the program:

```
(gdb) r
Starting program: ./added_protection
size of code: 130

Breakpoint 1, 0x00005555555552a0 in main ()
(gdb)
```

now we have hit our breakpiont, we can step through one by one.

at this point I like to use `layout asm` to have the assmebly code layout above my command window, to see what's being executed. Then we just `ni` (next instruction), jump into our shellcode and see.

```
(gdb) ni
```

And at this point, "Can u find the flag?" is printed and gdb exits. Interesting.

Doing that again, but this time without `ni`, and just looking at what gets executed:

We inspect 20 instructions (`x/20i` at the register `rdx`, because that's where the call goes in main (`callq  *%rdx`)

```
(gdb) x/20i $rdx
   0x7ffff7ffb000:  sub    $0x64,%rsp
   0x7ffff7ffb004:  mov    %rsp,%rcx
   0x7ffff7ffb007:  movabs $0x64617b4654435544,%r8
   0x7ffff7ffb011:  movabs $0x6e456465636e3476,%r9
   0x7ffff7ffb01b:  movabs $0x5364337470797263,%r10
   0x7ffff7ffb025:  movabs $0x65646f436c6c6568,%r11
   0x7ffff7ffb02f:  movabs $0x662075206e61437d,%r12
   0x7ffff7ffb039:  movabs $0x2065687420646e69,%r13
   0x7ffff7ffb043:  movabs $0x2020203f67616c66,%r14
   0x7ffff7ffb04d:  mov    $0xa,%r15d
   0x7ffff7ffb053:  push   %r15
   0x7ffff7ffb055:  push   %r14
   0x7ffff7ffb057:  push   %r13
   0x7ffff7ffb059:  push   %r12
   0x7ffff7ffb05b:  push   %r11
   0x7ffff7ffb05d:  push   %r10
```


Here we see a bunch of stuff being pushed into memory. Cool.

Extracting the data out of it:

```
64617b4654435544
6e456465636e3476
5364337470797263
65646f436c6c6568
662075206e61437d
2065687420646e69
2020203f67616c66
```

That looks very ASCII. Putting that into a file, lets say /tmp/data, then using xxd to decode ascii:

```
xxd -r -p /tmp/data
da{FTCUDnEdecn4vSd3tpyrcedoCllehf u naC} eht dni   ?galf

```

looks like we have our flag, but in little endian, so it's reversed. We just switch that around.

```
xxd -r -p /tmp/data | rev
flag?   ind the }Can u fhellCodecrypt3dSv4ncedEnDUCTF{ad
```

Now it's still little endian because it was pushed onto the stack "upside down". We can manually reverse this, 8 chars at a time:

DUCTF{adv4ncedEncrypt3dShellCode}Can u find the flag?

There we go! The flag is `DUCTF{adv4ncedEncrypt3dShellCode}`





