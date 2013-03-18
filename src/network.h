/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
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


namespace std {

class NetworkHelper {

public:
	NetworkHelper();
	~NetworkHelper();
	bool sendMessage(const string &host, const int &port, const string &message);
	void startServer(const string &host, const int &listen_port);

};

}
