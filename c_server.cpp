/*
 * A simple server in the internet domain using TCP
 * The port number is passed as an argument
 *
 * For reference: http://www.linuxhowtos.org/C_C++/socket.htm
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "led-matrix.h"
#include "thread.h"

#define BUFF_SIZE 256

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

// Base-class for a Thread that does something with a matrix.
class RGBMatrixManipulator : public Thread {
public:
RGBMatrixManipulator(RGBMatrix *m) : running_(true), matrix_(m)
{
}
virtual ~RGBMatrixManipulator()
{
    running_ = false;
}

// Run() implementation needs to check running_ regularly.

protected:
volatile bool running_;    // TODO: use mutex, but this is good enough for now.
RGBMatrix *const matrix_;
};

// Pump pixels to screen. Needs to be high priority real-time because jitter
// here will make the PWM uneven.
class DisplayUpdater : public RGBMatrixManipulator {
public:
DisplayUpdater(RGBMatrix *m) : RGBMatrixManipulator(m)
{
}

void Run()
{
    while (running_)
        matrix_->UpdateScreen();
}
};

int main(int argc, char *argv[])
{
    // Init led matrix
    GPIO io;

    if (!io.Init())
        return 1;
    RGBMatrix m(&io);
    RGBMatrixManipulator *updater = new DisplayUpdater(&m);
    updater->Start(10);      // high priority
    m.SetPixel(0, 0, 1, 1, 1);
    // Things are set up. Just wait for <RETURN> to be pressed.
    printf("Press <RETURN> to exit and reset LEDs\n");
    getchar();
    // Stopping display updater thread.
    delete updater;

    // Final thing before exit: clear screen and update once, so that
    // we don't have random pixels burn
    m.ClearScreen();
    m.UpdateScreen();

    return 0;
    /*
     * int sockfd, newsockfd, portno;
     * socklen_t clilen;
     * char buffer[BUFF_SIZE];
     * struct sockaddr_in serv_addr, cli_addr;
     * int n;
     * if (argc < 2) {
     *        fprintf(stderr,"ERROR, no port provided\n");
     *        exit(1);
     * }
     * sockfd = socket(AF_INET, SOCK_STREAM, 0);
     * if (sockfd < 0)
     *        error("ERROR opening socket");
     * bzero((char *) &serv_addr, sizeof(serv_addr));
     * portno = atoi(argv[1]);
     * serv_addr.sin_family = AF_INET;
     * serv_addr.sin_addr.s_addr = INADDR_ANY;
     * serv_addr.sin_port = htons(portno);
     * if (bind(sockfd, (struct sockaddr *) &serv_addr,
     *         sizeof(serv_addr)) < 0)
     *        error("ERROR on binding");
     * listen(sockfd,5);
     * clilen = sizeof(cli_addr);
     * newsockfd = accept(sockfd,
     *                   (struct sockaddr *) &cli_addr,
     *                   &clilen);
     * if (newsockfd < 0)
     *        error("ERROR on accept");
     * bzero(buffer, BUFF_SIZE);
     * n = read(newsockfd,buffer,255);
     * if (n < 0) error("ERROR reading from socket");
     * printf("Here is the message: %s\n",buffer);
     * n = write(newsockfd,"I got your message",18);
     * if (n < 0) error("ERROR writing to socket");
     * close(newsockfd);
     * close(sockfd);
     * return 0;*/
}
