PROG = return-to-whats-revenge
CFLAGS = -g -no-pie -fno-stack-protector -Wl,-z,relro,-z,now

all:
	gcc $(CFLAGS) return-to-whats-revenge.c util.c bpf-helper.c -o $(PROG)

clean:
	rm -f $(PROG)

