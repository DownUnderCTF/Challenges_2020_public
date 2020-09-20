default: encoder shellcode added_protection

# this makefile is for GNU linux; although might work on osx too

encoder: encoder.c Makefile
	echo "compiling encoder..."
	gcc -std=gnu99 encoder.c -o encoder


# https://gist.githubusercontent.com/superkojiman/11164279/raw/2b0319fb7a7a0e348ed47a17b6d69595c217bb8f/bin2sc.py
shellcode: sc_flag.asm Makefile
	echo "generating shellcode..."
	nasm sc_flag.asm
	./encoder sc_flag > sc_flag_encoded
	xxd -i sc_flag_encoded  | sed "s/sc_flag_encoded/code/" | tee shellcode.h

added_protection: added_protection.c shellcode.h Makefile
	set -x 
	echo "compiling final file.."
	gcc added_protection.c -o added_protection

