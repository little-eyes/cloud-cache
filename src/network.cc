/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong3@utk.edu)
 *     * Lipeng Wan (??)
 *
 * The basic network interface which wraps both
 * server and client. TCP server/client is adopted
 * here instead of HTTP which makes the communication
 * simple and easy.
 *
 * Note: measure everything!
 *
 * Dependency: C++11 and C++ Boost Library.
 */

#include <string>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h> /* close */
#include <string.h>
#include "stdlib.h"
#include "pthread.h"
#include "signal.h"
#include "network.h"
#define SUCCESS 0
#define ERROR   1
#define MAX_MSG 256

int server_dup;
void cleanup()
{
    close(server_dup);
    pthread_exit(NULL);
    return;
} /* cleanup() */

namespace std {
NetworkHelper::NetworkHelper() {
};
NetworkHelper::~NetworkHelper() {
};



/** 
 * readnf() - reading from a file descriptor but a bit smarter 
**/
int NetworkHelper::readnf(int fd, char *line)
{
    if (readline(fd, line, MAX_MSG) < 0)
        return ERROR; 
    return SUCCESS;
}

/**
 * readline() - read an entire line from a file descriptor until a newline.
 * functions returns the number of characters read but not including the
 * null character.
**/
int NetworkHelper::readline(int fd, char *str, int maxlen) 
{
  int n;           /* no. of chars */  
  int readcount;   /* no. characters read */
  char c;

  for (n = 1; n < maxlen; n++) {
    readcount = read(fd, &c, 1); /* store result in readcount */
    if (readcount == 1) /* 1 char read? */
    {
      *str = c;      /* copy character to buffer */
      str++;         /* increment buffer index */         
      if (c == '\n') /* is it a newline character? */
         break;      /* then exit for loop */
    } 
    else if (readcount == 0) /* no character read? */
    {
      if (n == 1)   /* no character read? */
        return (0); /* then return 0 */
      else
        break;      /* else simply exit loop */
    } 
    else 
      return (-1); /* error in read() */
  }
  *str=0;       /* null-terminate the buffer */
  return (n);   /* return number of characters read */
} /* readline() */


bool NetworkHelper::sendMessage(const string &host_str, const int &port, const string message) {
	
	char* dest = host_str.c_str();	
	int SERVER_PORT = port;
	char c_message[MAX_MSG];
    strcpy(c_message,(message+"\n").c_str());
	
	int client;  /* client socket */
    int rc;   
    struct sockaddr_in local_addr, serv_addr;
    struct hostent* host;
    char date[25];

    /* get host address from specified server name */
    host = gethostbyname(dest);

    if (host == NULL) 
    {
        printf("%s: unknown host 'sendMessage'\n",dest);
        return false;
    }
    /* now fill in sockaddr_in for remote address */
    serv_addr.sin_family = host->h_addrtype;
    /* get first address in host, copy to serv_addr */
    memcpy((char *) &serv_addr.sin_addr.s_addr, host->h_addr_list[0], host->h_length);
    serv_addr.sin_port = htons(SERVER_PORT);
    memset(serv_addr.sin_zero, 0, 8);

    /* create local stream socket */
    client = socket(PF_INET, SOCK_STREAM, 0);
    if (client < 0) {
        perror("cannot open socket ");
        return -1;
    }
    /* bind local socket to any port number */
    local_addr.sin_family = AF_INET;
    local_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    local_addr.sin_port = htons(0);
    memset(local_addr.sin_zero, 0, 8);

    rc = bind(client, (struct sockaddr *) &local_addr, sizeof(local_addr));

    if (rc < 0) 
    {
        printf("sendMessage: cannot bind port TCP %u\n",local_addr.sin_port);
        perror("error ");
        return(1);
    }
    /* connect to server */
    rc = connect(client, (struct sockaddr *) &serv_addr, sizeof(serv_addr));
    if (rc < 0) 
    {
        perror("cannot connect ");
        return(1);
    }

    /* now send /TIME */
    rc = send(client, c_message, strlen(c_message)+1 , 0);
 
    if (rc < 0) 
    {
        perror("cannot send data "); 
        close(client);
        return(false);
    }
 
 	printf("Sending complete\n");
    /* we're expecting 25 chars from server, */
    read(client,date,25);

    printf("%s",date);
    
    close(client);	
 	return true;
};

bool NetworkHelper::startServer(const string &host, const int &listen_port) {
	int client;         /* client socket descriptor */
    int addr_len;       /* used to store length (size) of sockaddr_in */
    pthread_t thread;   /* thread variable */
    int SERVER_PORT = listen_port;
    struct sockaddr_in cliAddr;   /* socket address for client */
    struct sockaddr_in servAddr;  /* socket address for server */

    /* now create the server socket 
       make it an IPV4 socket (PF_INET) and stream socket (TCP)
       and 0 to select default protocol type */          
    server = socket(PF_INET, SOCK_STREAM, 0);
	server_dup = server;
    if (server < 0) {
        perror("cannot open socket ");
        return ERROR;
    }
  
    /* now fill in values of the server sockaddr_in struct 
       s_addr and sin_port are in Network Byte Order (Big Endian)
       Since Intel CPUs use Host Byte Order (Little Endian), conversion 
       is necessary (e.g. htons(), and htonl() */    
    servAddr.sin_family = AF_INET;  /* again ipv4 */  
    servAddr.sin_addr.s_addr = htonl(INADDR_ANY); /* local address */
    servAddr.sin_port = htons(SERVER_PORT); 
    memset(servAddr.sin_zero, 0, 8);
        
    /* now bind server port 
       associate socket (server) with IP address:port (servAddr) */ 
    if (bind(server, (struct sockaddr *) &servAddr, sizeof(struct sockaddr)) < 0) {
        perror("cannot bind port ");
        return ERROR;
    }

    /* wait for connection from client with a pending queue of size 5 */
    listen(server, 5);
      
    while(1) /* infinite loop */
    {
        printf("**%s: waiting for data on port TCP %u\n", host.c_str(), SERVER_PORT);
        addr_len = sizeof(cliAddr);
        
        /* new socket for client connection
           accept() will block until a connection is present 
           accept will return a NEW socket for the incoming connection    
           server socket will continue listening 
           store client address in cliAddr */
        client = accept(server, (struct sockaddr *) &cliAddr, &addr_len);
        if (client < 0) {
            perror("cannot accept connection\n ");
            break;
        }


	//Processing message!
	struct sockaddr_in cliAddr;
    char line[MAX_MSG];
    //char reply[MAX_MSG];
    //int i;
    //int client_local;   /* keep a local copy of the client's socket descriptor */
    int addr_len;       /* used to store length (size) of sockaddr_in */
    //time_t currtime;        
    //char time_msg1[6] = {'/', 'T', 'I', 'M', 'E', '\n'};
    //char time_msg2[6] = {'/', 'T', 'I', 'M', 'E', 13};
    char quit_msg1[6] = {'/', 'Q', 'U', 'I', 'T', '\n'};
    char quit_msg2[6] = {'/', 'Q', 'U', 'I', 'T', 13};
    char cmd[6];
     
    int client_local = client;/* store client socket descriptor */
    addr_len = sizeof(cliAddr); /* store value of size of sockaddr_in */
    
    /* get clients name and store in cliAddr */
    getpeername(client_local, (struct sockaddr*)&cliAddr, &addr_len);	
    /* reset line */
    memset(line, 0, MAX_MSG);
    
    /* now read lines from the client socket */
    while(readnf(client_local, line)!=ERROR)  /* loop - read from socket */
    {
        if (!strcmp(line,""))   /* string must not be null string */
            break;
        
        //for (i = 0; i<6; i++)   /* get first 6 chars of string, capitalize */
        //    cmd[i] = toupper(line[i]);
        
		//do something with the message received
		//simply print out the message on the screen for here
		if(strlen(line)>2)
		{
			//echoing the mssageo
			printf("Message received from %s:%d: %s", inet_ntoa(cliAddr.sin_addr), ntohs(cliAddr.sin_port), line);
			send(client_local, "MSG received\n\0", 14, 0);
		}
		/* Did client ask for time? */
        /* Does client want to quit? */
        if (strncmp(line, quit_msg1, 6) == 0 || strncmp(cmd, quit_msg2, 6) == 0)
        {
            printf("Received /QUIT from %s:%d\n", inet_ntoa(cliAddr.sin_addr), ntohs(cliAddr.sin_port));
            break;
        }
        /* reset line */
        memset(line,0,MAX_MSG);
    } /* while(readnf) */
    printf("Closing socket\n");
    close(client_local);       
    } /* while (1) */

    close(server);
    return 0;
};

}
