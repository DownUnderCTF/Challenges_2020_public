#include <stdio.h>
#include <stdlib.h>

char *flag = "DUCTF{haha its not that easy}";

int g = 'g';
int a = 'a';

int brac0 = '{';

int brac1 = '}';

int crap = 0x6f;
int this = 0x29;
int is = 0xaa;
int too = 0x29;
int easy = 0x90;
int what = 0xac;
int the = 0xbc;
int heck = 0x36;


int D = 'D';



char *fmt = "%s%02x%02x%02x%02x%02x%02x%02x%02x}";

int main () {

	int f = 'f';
	int l = 'l';

	char realflag[100];
	realflag[24] = 0;

	realflag[0] = 'D';
	realflag[1] = 'U';
	realflag[2] = 'C';
	realflag[3] = 'T';
	realflag[4] = 'F';

	realflag[5] = brac0;
	realflag[23] = brac1;

	size_t ret = sprintf(realflag + 6, fmt, "d1d_You_Just_ltrace_", this, crap, is, too ,easy ,what, the, heck);
	realflag[ret + 6] = brac1;

	puts(flag + 6);

}





