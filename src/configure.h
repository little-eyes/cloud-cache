/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
 *     * Lipeng Wan (??)
 *
 * The global configure file.
 *
 * Note: measure everything!
 *
 * Dependency: C++11, C++ Boost Library, Redis C Client.
 */
#include <string>
#include <vector>

using namespace std;

static const string MASTER_HOST = 
	"hydra1.eecs.utk.edu"; /* the master host name */

static const vector <string> SLAVE_HOST = {
	"hydra2.eecs.utk.edu",
	"hydra3.eecs.utk.edu",
	"hydra4.eecs.utk.edu"}; /* the slave hosts name */

static const vector <string> DATA_HOST = {
	"hydra2.eecs.utk.edu",
	"hydra2.eecs.utk.edu",
	"hydra2.eecs.utk.edu"}; /* the data hosts name */
