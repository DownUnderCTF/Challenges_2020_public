nsjail-ctf
==========

A base image for making pwn challenges.

To build a challenge, copy your binary and other associated files to `/home/ctf/chal`.
The default nsjail-pwn.sh script can be configured via docker `ENV`, or an
alternative script can be provided using ENV.

At the end of your Dockerfile, expose the appropriate port using `EXPOSE port_number/TCP`.

## options

Default options are listed below.

```sh
PORT=1337               # Listening port
MAX_CONNS_PER_IP=16     # Maximum number of connections per IP address.
MAX_MEMORY=67108864     # Maximum memory that processes can use.
MAX_PIDS=16             # Maximum number of processes.
TIME_LIMIT=60           # Timeout before connection is closed.
RLIMIT_CPU=10           # Maximum amount of CPU time permitted.
```
