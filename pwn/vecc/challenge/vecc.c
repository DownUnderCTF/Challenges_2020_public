#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

typedef struct {
	uint8_t * buffer;
	uint32_t len;
	uint32_t capacity;
} vecc;

vecc * table[10] = { NULL };

__attribute__((noinline))
uint64_t next_pow2(uint64_t x) {
	if (x <= 1) {
		return x;
	}
	return 1 << (64 - __builtin_clz(x - 1));
}

void vecc_append(vecc * v, uint8_t * buffer, uint32_t len) {
	if (v->len + len > v->capacity) {
		uint32_t next = next_pow2(v->len + len);
		v->buffer = realloc(v->buffer, next);
		v->capacity = next;
	}
	memcpy(&v->buffer[v->len], buffer, len);
	v->len += len;
}

void vecc_clear(vecc * v) {
	v->len = 0;
}

void vecc_destroy(vecc * v) {
	if (v->buffer != NULL) {
		free(v->buffer);
	}
	v->buffer = NULL;
	v->len = 0;
	v->capacity = 0;
}

int get_index() {
	printf("Index?\n");
	printf("> ");
	char buf[3];
	fgets(buf, 3, stdin);
	int index = buf[0] - '0';
	if (index < 0 || index >= 10) {
		return -1;
	}
	return index;
}

void create_vecc() {
	int index = get_index();
	if (index == -1) {
		printf("Invalid!\n");
		return;
	}
	table[index] = malloc(sizeof(vecc));
	printf("Done!\n");
}

void destroy_vecc() {
	int index = get_index();
	if (index == -1) {
		printf("Invalid!\n");
		return;
	}
	if (table[index] == NULL) {
		printf("No vecc there!\n");
		return;
	}
	vecc_destroy(table[index]);
	free(table[index]);
	table[index] = NULL;
	printf("Done!\n");
}

void append_vecc() {
	int index = get_index();
	if (index == -1) {
		printf("Invalid!\n");
		return;
	}
	if(table[index] == NULL) {
		printf("No vecc there!\n");
		return;
	}
	printf("Length?\n");
	printf("> ");
	char buf[5];
	fgets(buf, 5, stdin);
	int length = atoi(buf);
	if (length < 0) {
		printf("Invalid!\n");
		return;
	}
	uint8_t * temp = malloc(length);
	fread(temp, 1, length, stdin);
	vecc_append(table[index], temp, length);
	free(temp);
	printf("Done!\n");
}

void clear_vecc() {
	int index = get_index();
	if (index == -1) {
		printf("Invalid!\n");
		return;
	}
	if(table[index] == NULL) {
		printf("No vecc there!\n");
		return;
	}
	vecc_clear(table[index]);
	printf("Done!\n");
}

void show_vecc() {
	int index = get_index();
	if (index == -1) {
		printf("Invalid!\n");
		return;
	}
	if(table[index] == NULL) {
		printf("No vecc there!\n");
		return;
	}
	if(table[index]->buffer == NULL) {
		printf("Vecc is empty!\n");
		return;
	}
	vecc * v = table[index];
	fwrite(v->buffer, 1, v->len, stdout);
	printf("\n");
}

int shell() {
	printf("0: exit\n");
	printf("1: create vecc\n");
	printf("2: destroy vecc\n");
	printf("3: append vecc\n");
	printf("4: clear vecc\n");
	printf("5: show vecc\n");
	printf("> ");
	char buf[3];
	fgets(buf, 3, stdin);
	switch (buf[0]) {
		case '0':
			return 1;
		case '1':
			create_vecc();
			break;
		case '2':
			destroy_vecc();
			break;
		case '3':
			append_vecc();
			break;
		case '4':
			clear_vecc();
			break;
		case '5':
			show_vecc();
			break;
		default:
			printf("Invalid selection, try again\n");
			break;
	}
	return 0;
}

int main() {
	setbuf(stdout, NULL);

	printf("=== WELCOME TO THE VECC SHELL ===\n");
	int exit = 0;
	while (exit == 0) {
		exit = shell();
	}
	return 0;
}
