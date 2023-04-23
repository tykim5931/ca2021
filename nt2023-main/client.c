#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

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

static volatile int keepRunning=1;
void intHandler(int dummy) {
    keepRunning=0;
}

int main(int argc, char const* argv[])
{
    signal(SIGINT, intHandler);

    // int status, valread, client_fd;
    int client_sockfd;  // define socket descriptor
    struct sockaddr_in server_addr; // define server address
    socklen_t server_addr_len;
    char buf[MAXBUF];

    // Open socket (using tcp, thus use sock_stream)
    if((client_sockfd = socket(AF_INET, SOCK_STREAM,0)) < 0) {
        error_handling("Socket Opening Error\n", 0, 0);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_addr.sin_port = htons(PORT);
    server_addr_len = sizeof(server_addr);

    // Create Input Queue!
    struct Queue* q = (struct Queue*)malloc(sizeof(struct Queue));
    q->front = q->rear = NULL;
    memset(buf, 0x00, MAXBUF);

    if (connect(client_sockfd, (struct sockaddr *) &server_addr, server_addr_len) < 0) {
        error_handling("Connect Error\n", client_sockfd, q);
    }

    printf("client> Connected to server!\n");

    while(1) {
        // Get User Inputs
        printf("client> Give user input:\n");
        while(strcmp(fgets(buf, MAXBUF, stdin), "Q\n") != 0) {
            if(strcmp(buf, "bye\n")==0) {
                memset(buf, 0x00, MAXBUF);
                goto byebye;
            } 
            push(q, buf);
            memset(buf, 0x00, MAXBUF);
        }
        memset(buf, 0x00, MAXBUF);  // flush Q

        // Send to server
        if (write(client_sockfd, "SEND", MAXBUF) <=0) {  // Write SEND
            error_handling("Write Error\n", client_sockfd, q);
        }
        while(q->front!=NULL){  // write input queue
            struct QNode* curr = q->front;

            // printf("client> Sending: %s", curr->data);

            if (write(client_sockfd, curr->data, MAXBUF) <=0) {
                error_handling("Write Error\n", client_sockfd, q);
            }

            // deQueue
            q->front = q->front->next;
            if (q->front == NULL) q->rear = NULL;
            free(curr);
        }
        if (write(client_sockfd, "RECV", MAXBUF) <=0) {  // write RECV
            error_handling("client> Write Error\n", client_sockfd, q);
        }

        // Read from server
        printf("client> Message from server:\n%s", buf);
        while(1) {
            if(read(client_sockfd, buf, MAXBUF) < 0) {
                error_handling("client> Reaad Error\n", client_sockfd, q);
            }
            if(strcmp(buf, "END_OF_SERVER_MSG") == 0) {
                memset(buf, 0x00, MAXBUF);
                break;
            }
            printf("%s", buf);
            memset(buf, 0x00, MAXBUF);
        }
    }

    // Close in Bye Condition
byebye:
    if (write(client_sockfd, "Echo_CLOSE", MAXBUF) <= 0) {
        error_handling("Write Error",client_sockfd, q);
    }
    if (read(client_sockfd, buf, MAXBUF) <= 0) {
        error_handling("Read Error", client_sockfd, q);
    }

    close(client_sockfd);
    freeQueue(q);

    printf("client> Connection closed. Good bye!\n");
    return 0;
}

