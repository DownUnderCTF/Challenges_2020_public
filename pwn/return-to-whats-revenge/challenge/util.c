#include <stdint.h>
#include <signal.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "util.h"
#include "sandbox.h"

void handler() {
	puts("Time's up");
	exit(0);
}

void error(const char *s) {
	puts(s);
	exit(1);
}

__attribute__((constructor))
void setup() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    signal(SIGALRM, handler);
    alarm(30);

    sandbox();
}
