#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#define MAXBUF 1024
void error_handling (char *msg);

int main (int argc, char **argv) {
    struct sockaddr_in server_addr;
    int sockfd;
    socklen_t server_addr_len;
    char buf[MAXBUF];

    // Open socket
    if ((sockfd = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
        error_handling("socket error\n");
    }

    server_addr.sin_family = AF_INET;   // map serverside
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_addr.sin_port = htons(50000);
    server_addr_len = sizeof(server_addr);

    if (connect(sockfd, (struct sockaddr *) &server_addr, server_addr_len) < 0) {
        close(sockfd);
        error_handling("connect error\n");
    }

    memset(buf, 0x00, MAXBUF);
    fgets(buf, MAXBUF, stdin);

    if(write(sockfd, buf, MAXBUF) <= 0) {
        close(sockfd);
        error_handling("write error\n");
    }
    if(read(sockfd, buf, MAXBUF) <= 0) {
        close(sockfd);
        error_handling("read error\n");
    }

    close(sockfd);
    return 0;
}

void error_handling(char *msg) {
    fputs(msg, stderr);
    exit(EXIT_FAILURE);
}