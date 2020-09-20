#include <stdio.h>

#define INPUT_SIZE  64
#define INPUT_TIMES  3

__attribute__((constructor))
void setup() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

int main() {
    char buffer[INPUT_SIZE];
    int i;

    for (i = 0; i < INPUT_TIMES; i++) {
        fgets(buffer, INPUT_SIZE, stdin);
        printf(buffer);
    }

    return 0;
}
