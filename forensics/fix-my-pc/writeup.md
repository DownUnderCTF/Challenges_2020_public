fix-my-pc
=========

We are presented with what looks like a disk image, and the other file which seems like a memory
dump. The image provided is a qcow2, which is a common disk format used in virtualization software
such as qemu. To mount it, qemu-nbd can be used.

```
qemu-nbd --connect=/dev/nbd0 system.img
```

On further inspection, it appears that 2 of the partitions are encrypted with LUKS whereas
the boot partition is unencrypted.


We can use cryptsetup to inspect the header.
```
Version:        1
Cipher name:    aes
Cipher mode:    xts-plain64
Hash spec:      sha256
Payload offset: 4096
MK bits:        512
```

By using the memory dump, we can retrieve the key that was used to encrypt the drive. I used a tool
called findaes to extract the AES key from the memory dump.

```
Found AES-256 key schedule at offset 0x1bffed68: 
ff 98 d7 67 61 14 70 24 eb b0 c8 d4 e1 14 18 14 21 4d 2a 83 d7 93 66 09 37 77 55 e5 18 0a 3c 57 
Found AES-256 key schedule at offset 0x1bffef58: 
09 4e 2a df 58 cf b1 7d 85 f0 f6 93 3f 7b 44 ef a0 0a 3c da 7b be 01 87 3e 09 ff 4e e7 a6 05 39
```

Once we extract the key, we can use cryptsetup to mount our partition by using the `--master-key-file`
option.
```sh
sudo cryptsetup --master-key-file master.key luksOpen /dev/nbd0p2 cryptfroot
```

On opening this image, we can check out `/etc/fstab` which shows that there is another partition
which is mounted to home. Further, we can check out `/etc/crypttab` which contains the path to the
key file which is used to unlock the second encrypted partition.

```sh
sudo cryptsetup --key-file etc/crypttab.d/home.key luksOpen /dev/nbd0p3 cryptfhome
```

Once we unlock and mount the second partition. We are greeted with a user account named bob. This
user's home contains a few directories with images and text files, but those are mostly irrelevant.
There is also a SSH key thrown in. From reading the `.ash_history`, we also see that there is a repo
that bob has tried to clone, so by putting two-and-two together, that SSH key can then be used to clone
the GitHub repo.

```
git clone git@github.com:cornochips/configs.git
```

By trawling through the GitHub repo's history, we can then find the flag!

