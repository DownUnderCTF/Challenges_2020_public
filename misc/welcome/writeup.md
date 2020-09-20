SSHing into the server with credentials `ductf:ductf` bombards us with thousands of colourful texts saying "Welcome to DUCTF!". Presumably, the flag is hidden as one of the messages. We can pipe the output into grep to filter for the flag.

```
$ ssh ductf@0.0.0.0 -p 1337 | grep -P 'DUCTF{.*?}' -o
ductf@localhost's password:
DUCTF{w3lc0m3_t0_DUCTF_h4v3_fun!}
```
