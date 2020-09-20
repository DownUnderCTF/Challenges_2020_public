#include <stdio.h>
#include <unistd.h>

__attribute__((constructor))
void setup() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

void vuln() {
    char name[40];

    printf("Where would you like to return to?\n");
    gets(name);
}

int main(void) {
    printf("Today, we'll have a lesson in returns.\n");
    vuln();
}
