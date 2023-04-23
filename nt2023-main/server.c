#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 50000
#define MAXBUF 1024


// === QUEUE for User input ====
struct QNode {
    char data[1024];
    struct QNode* next;
};
struct Queue {
    struct QNode *front, *rear;
};

void push(struct Queue* q, char* buf) {
    struct QNode* temp = (struct QNode*)malloc(sizeof(struct QNode));
    temp->next = NULL;
    strcpy(temp->data, buf);

    if (q->rear == NULL) {
        q->front = q->rear = temp;
        return;
    }
    q->rear->next = temp;
    q->rear = temp;
}

void freeQueue(struct Queue* q) {
    while(q->front!=NULL){  // write input queue
        struct QNode* curr = q->front;
        q->front = q->front->next;
        if (q->front == NULL) q->rear = NULL;
        free(curr);
    }
    free(q);
}
// ==================================

void error_handling(char *msg, int sockfd, struct Queue* q) {
    if(sockfd) close(sockfd);
    if(q) freeQueue(q);
    fputs(msg, stderr);
    exit(EXIT_FAILURE);
}

int main(int argc, char const* argv[])
{
    int server_sockfd, client_socket;
    struct sockaddr_in server_addr, client_addr;
    char buf[MAXBUF];
    socklen_t client_addr_length = sizeof(client_addr);

    memset(buf, 0x00, MAXBUF);

    // Create Socket
    if((server_sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // INADDR_ANY receives any data form any ip address
    server_addr.sin_port = htons(PORT);

    // Bind socket to the port
    if(bind(server_sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
        perror("Bind failed");
        close(server_sockfd);
        exit(EXIT_FAILURE);
    }

    // Receive from client
    if (listen(server_sockfd, 5) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    // Create Queue
    struct Queue* q = (struct Queue*)malloc(sizeof(struct Queue));
    q->front = q->rear = NULL;
    memset(buf, 0x00, MAXBUF);

    while(1) {
        if((client_socket = accept(server_sockfd, (struct sockaddr*)&client_addr, (socklen_t*)&client_addr_length)) < 0) {
            perror("Accept failed");
            close(server_sockfd);
            exit(EXIT_FAILURE);
        } else {
            printf("server> Client connected\n");
        }
        // 1. Communicate while Echo_CLOSE is received
        while(1) { 
            if(read(client_socket, buf, MAXBUF) < 0 ){
                perror("Read failed");
                close(server_sockfd);
                exit(EXIT_FAILURE);
            }
            if(strcmp(buf,"Echo_CLOSE")==0) {
                memset(buf, 0x00, MAXBUF);
                break;
            }
            
            // Receive from client
            if(strcmp(buf,"SEND")==0) {
                while(1) {
                    if (read(client_socket, buf, MAXBUF) < 0){
                        perror("Read failed");
                        close(server_sockfd);
                        exit(EXIT_FAILURE);
                    }
                    if (strcmp(buf, "RECV") ==0) {
                        memset(buf, 0x00, MAXBUF);
                        break;
                    }
                    // enqueue
                    push(q, buf);
                    strcpy(q->rear->data, buf);
                    // printf("server> Received: %s",q->rear->data);

                    memset(buf, 0x00, MAXBUF);
                }
            }
            
            // Send to client
            while(1) {
                struct QNode* curr = q->front;
                if(curr == NULL) {
                    // send ending flag
                    if(write(client_socket, "END_OF_SERVER_MSG", MAXBUF) < 0) {
                        perror("Send failed");
                        close(server_sockfd);
                        exit(EXIT_FAILURE);
                    }
                    break;
                }
                if (write(client_socket, curr->data, MAXBUF) < 0) {
                    perror("Send failed");
                    close(server_sockfd);
                    exit(EXIT_FAILURE);
                } 
                // printf("server> Sending: %s", curr->data);
    
                // deQueue
                q->front = curr->next;
                if (q->front == NULL) q->rear = NULL;
                free(curr);
            }
        }

        // 2. Close connection if Echo_CLOSED is received
        if(write(client_socket, "Echo_CLOSED", MAXBUF) < 0) {
            perror("Send failed");
            close(server_sockfd);
            exit(EXIT_FAILURE);
        }
        printf("server> Connection closed\n");
        close(client_socket);
    }

    freeQueue(q);
    close(server_sockfd);
    shutdown(server_sockfd, SHUT_RDWR);
    return 0;
}