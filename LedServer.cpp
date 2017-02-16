#include "LedServer.h"
#include <bitset>

LedServer::LedServer(int portno) : running_(true) {
    // Setup server
    struct sockaddr_in serv_addr;
    // S U C C _ S T R E A M
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
        error("ERROR opening socket");
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    if (bind(sockfd, (struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0)
        error("ERROR on binding");
    std::cout << "setup server!" << '\n';
}

void LedServer::Run() {
    char name[128];
    gethostname(name, sizeof name);
    std::cout << "Running on: " << name << '\n';
    while (running_) {
        socklen_t clilen;
        char buffer[BUFF_SIZE];
        listen(sockfd, 5);
        clilen = sizeof(cli_addr);
        newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd < 0)
            error("ERROR on accept");
        bzero(buffer, BUFF_SIZE);
        int n = read(newsockfd, buffer, 255);
        if (n < 0)
            error("ERROR reading from socket");
        bitset<32> bits(buffer);
        std::cout << "Received bits: " << bits << '\n';
        // printf("Here is the message: %u\n", (unsigned)buffer);
        n = write(newsockfd,"I got your message",18);
        if (n < 0)
            error("ERROR writing to socket");
    }
}

LedServer::~LedServer() {
    running_ = false;
    close(newsockfd);
    close(sockfd);
}

void LedServer::error(const char *msg)
{
    perror(msg);
    exit(1);
}
