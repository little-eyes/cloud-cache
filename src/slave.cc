/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
 *     * Lipeng Wan (??)
 *
 * Implementing the slave machine.
 *
 * The slave machine is used to run the solve() function
 * which implemented in solver.c. The developer needs to
 * implement his own solve() function in order to run in
 * the cloud cache framework.
 *
 * The slave is actually a TCP server waiting for the
 * request. Then for each request it inserts into the
 * task queue. Each task in the queue will be run in a 
 * different thread to off-load the main thread's burden.
 *
 * Note: measure everything!
 *
 * Dependency: C++11 and C++ Boost Library.
 */

#include <iostream>
#include "slave.h"
#include "sharding.h"
#include "hiredis/hiredis.h"
#include <cstring>
#include <cstdio>
using namespace std;

int main() {
	cout << MASTER_HOST << endl;
	NetworkHelper networkLayer;
	networkLayer.startServer("localhost",20202);
	return 0;
}

