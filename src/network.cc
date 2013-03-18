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
#include "network.h"


namespace std {

NetworkHelper::NetworkHelper() {

};

NetworkHelper::~NetworkHelper() {

};

bool NetworkHelper::sendMessage(const string &host, const int &port, const string &message) {

	return true;
};

void NetworkHelper::startServer(const string &host, const int &listend_port) {

};

}
