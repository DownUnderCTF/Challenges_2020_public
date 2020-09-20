NAME				:= vecc

### STANDARD OPTIONS ###

CC					:= gcc
CFLAGS				:= -std=c11 -m64 -Wall -Wextra -Wpedantic
INTEL_ASM			:= -masm=intel
# DEBUGGING			:= -g -ggdb
OPTIMISATION		:= -O2
# 32BIT				:= -m32

### HARDENING ###
# STATIC				:= -static
FULL_RELRO			:= -Wl,-z,relro,-z,now

### WEAKNESSES ###
# VULN_STACK			:= -fno-stack-protector --param ssp-buffer-size=4 -z execstack -D_FORTIFY_SOURCE=0
# NO_RELRO			:= -Wl,-z,norelro
NO_PIE				:= -no-pie
# RPATH				:= -Wl,-rpath=./rpath

EXTRA				:= -fno-stack-protector --param ssp-buffer-size=4 -D_FORTIFY_SOURCE=0

SELECTIONS			:= $(CFLAGS) $(INTEL_ASM) $(DEBUGGING) $(OPTIMISATION) $(32BIT) $(STATIC) $(FULL_RELRO) $(VULN_STACK) $(NO_RELRO) $(NO_PIE) $(RPATH) $(EXTRA)

all: clean build

build:
	$(CC) $(SELECTIONS) $(NAME).c -o $(NAME)

clean:
	rm -f $(NAME)

aslr:
	sudo sysctl -w kernel.randomize_va_space=1

strip:
	strip $(NAME)
