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
void cleanup();

namespace std {

class NetworkHelper {

public:
	NetworkHelper();
	~NetworkHelper();
	bool sendMessage(const string &host, const int &port, const string &message);
	bool startServer(const string &host, const int &listen_port);/*Do we need a server host?*/
	

private:
	/* auxillary functions to read newline-terminated strings from a file/socket */	
	int readnf (int, char *);
	int readline(int, char *, int);

	int server;         /* listening socket descriptor */
	void handler(void * paramsd); /*Thread handler for incoming connections*/



};

}
