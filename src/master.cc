/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
 *     * Lipeng Wan (??)
 *
 * Implementing the master machine.
 * 
 * The master machine read problem set, and dispatch
 * each problem to slave/worker machines. Also the
 * master machine needs a bitmap to maintain the
 * solving progress, which is just a static memory
 * field maintaining by Redis or MySQL database.
 * 
 * One optimization is called twin-dispatch: for each
 * task, the master machine issue two copies to two
 * different machines, they try to solve the problem
 * indenpently and simutaneously. Then we accept the
 * first results from the first outcome.
 *
 * To imporve the belief, we can issue more than three
 * task copies and let them vote.
 *
 * Note: measure everything!
 *
 * Dependency: C++11 and C++ Boost Library.
 */

#include <iostream>
#include "master.h"


int main() {

	return 0;
}
