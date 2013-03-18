/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
 *     * Lipeng Wan (??)
 *
 * This is the sharding classes definition. Sharding
 * is very important for the performance of the cloud
 * cache performance.
 * 
 * The task of the sharding is two-fold: 1) shard the
 * cache query; 2) shard the task requests.
 *
 * Note: measure everything!
 *
 * Dependency: C++11 and C++ Boost Library.
 */

#include <string>

namespace std {

class ShardingProvider {

public:
	ShardingProvider();
	~ShardingProvider();
	string getTaskSharding(const string &key);
	string getCacheSharding(const string &key);

private:
	string sha1(const string &key);
};

}
