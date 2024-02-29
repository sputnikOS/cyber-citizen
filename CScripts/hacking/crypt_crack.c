#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>

void vomit(char *message, char *extra) {
	printf(message, extra);
	exit(1);
}