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
	string getTaskShardingByIp(const string &key);
	int getTaskShardingByIndex(const string &key);
	string getCacheShardingByIp(const string &key);
	int getCacheShardingByIndex(const string &key);

private:
	string sha1(const string &key);
	int ElfHash(const string &key);
	int XorHash(const string &key);
};

}
