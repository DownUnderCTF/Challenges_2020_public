#include <stdio.h>
#include <unistd.h>

#include "util.h"

void vuln() {
    char name[40];

    printf("Where would you like to return to?\n");
    gets(name);
}

int main(void) {
    printf("Today, we'll have a lesson in returns.\n");
    vuln();
}
