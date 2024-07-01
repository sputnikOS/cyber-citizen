#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "../hacking.h"

int main(void) {
    int i, recv_length, sockfd;
    u_char buffer[9000];

    if ((sockfd = socket(PF_iNET_SOCK)))
}