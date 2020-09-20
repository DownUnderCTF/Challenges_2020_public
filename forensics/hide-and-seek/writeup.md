1. Find the 'malware' in `/opt`
2. Experiment with ps -aux to realise that child.py doesn't show up; even though it is clearly running. Run strings on libprocesshider.so and find the string 'python3'; suggesting that it is hiding python3 executables from tools like ps, pstree and top.
3. Extract the volatility profile from the virtual machine. This can be done with the use of a host-only adapter, and a WebDAV server; or with the use of services such as https://gofile.io.
4. Load this profile into volatility. In my case it was to copy it into `/usr/lib/python2.7/site-packages/volatility/plugins/overlays/linux`
4. Make a memory dump of the machine. 

```bash
vboxmanage debugvm "hide-and-seek" dumpvmcore --filename test.elf # Dump Core

objdump -h test.elf|egrep -w "(Idx|load1)" # Get offsets

size=0x80000000;off=0x00002598;head -c $(($size+$off)) test.elf|tail -c +$(($off+1)) > test.raw # Extract RAM
```

5. Use Volatility to search for python3 processes.

```bash
volatility --profile=LinuxUbuntu_5_4_0-45-generic_profilex64 -f test.raw linux_psaux | grep python3
```

6. Get the PID of the process `python3 /opt/malware/mother.cpython-38.pyc`
7. Go back to the running VM snapshot, execute the command `pyrasite-shell [PID]`
8. This will get you an interactive python shell within the mother process
9. Run `dir()`, see there is a flag variable.
10. `print(flag)`
11. ???
12. Profit!!!