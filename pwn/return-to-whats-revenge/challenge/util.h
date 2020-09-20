#include <stdint.h>

void handler();
void error(const char *);
__attribute__((constructor)) void setup();
