# Alternative Write-Up for Hide-And-Seek

1.  `vboximg-mount -i hide-and-seek/hide-and-seek\ Clone.vdi /tmp/mnt`

2. 

```bash
ls -lh /tmp/mnt
-rw-r--r--  1 4294967295  nogroup    10G Sep 15 22:50 vhdd
-rw-rw-rw-  1 root        wheel     512M Jan  1  1970 vol0
-rw-rw-rw-  1 root        wheel     9.5G Jan  1  1970 vol1
```

3. `testdisk ./vhdd`

4. Proceed > Advanced > Linux > List

5. Navigate to /opt/malware

6. Retrieve `mother.cpython-38.pyc`

7. Decompile this python byte code with `uncompyle6`

8. Find the exec statement that makes the flag, run it a print it yourself.

9. ???

10. Profit!!!

## Credit 
h4sh#5081 from UQ Cyber

## The moral of the story

Not even `rm` can hide your mistakes.
