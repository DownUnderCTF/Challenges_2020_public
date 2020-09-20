# Is this pwn or web?

**Author:** Faith

**Category:** pwn

**Difficulty:** Insane

Why do some people think browser exploitation == web?

Once you get code execution, you can execute `/home/ctf/flagprinter` to get the flag. No need to get a shell.

* V8 commit: 47054c840e26394dea0e36df47884202a15dd16d
* V8 version: 8.7.9

`nc localhost 1337`

**Files to be provided:**

* challenge.tar.gz

**Setup instructions:**

The following files in the `challenge/` directory must be executable:

* `d8`
* `flagprinter`
* `server.py`
