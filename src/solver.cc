/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
 *     * Lipeng Wan (??)
 *
 * The file implements the generic solver and all its
 * inherited solver. If the developer would like to
 * solve some hard problem via the cloud cache, he
 * can easily inherit the generic solver to create
 * his own solver.
 *
 * the solver will utilize the cloud cache to speed
 * up the solving process. cloud cache interface is
 * defined in ccache.h.
 *
 * Note: measure everything!
 *
 * Dependency: C++11 and C++ Boost Library.
 */

#include "solver.h"


namespace std {

GenericSolver::GenericSolver() {
 
};

GenericSolver::~GenericSolver() {

};

bool GenericSolver::solve() {

	return true;
};

}
