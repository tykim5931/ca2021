#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAXBUF 1024

int main (void) {
    int socket_sd;
    struct sockaddr_in server_addr, client_addr;
    char server_message[MAXBUF], client_message[MAXBUF];
    int client_struct_length = sizeof(client_addr);

    memset(server_message, 0x00, MAXBUF);
    memset(client_message, 0x00, MAXBUF);

    socket_sd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if(socket_sd < 0) {
        printf("Error while creating socket\n");
        return -1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(2000);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if(bind(socket_sd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        printf("Couldn't bind to the port\n");
        return -1;
    }

    printf("Listening for incoming messages...\n\n");

    if(recvfrom(socket_sd, client_message, sizeof(client_message), 0,
        (struct sockaddr*)&client_addr, &client_struct_length) < 0) {
            printf("Couldn't receive\n");
            close(socket_sd);
            return -1;
    }

    printf("Received message from IP: %s and port: %i\n",
        inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
    printf("Msg from client: %s\n", client_message);

    if (sendto(socket_sd, client_message, strlen(client_message), 0,
        (struct sockaddr*)&client_addr, client_struct_length) < 0)
    {}
}