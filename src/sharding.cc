/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
 *     * Lipeng Wan (??)
 *
 * This is the sharding classes implementation. Sharding
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
#include "sharding.h"

namespace std {

ShardingProvider::ShardingProvider() {

};

ShardingProvider::~ShardingProvider() {

};

string ShardingProvider::getTaskSharding(const string &key) {
	
	return NULL;
};

string ShardingProvider::getCacheSharding(const string &key) {

	return NULL;
};

string ShardingProvider::sha1(const string &key) {

	return NULL;
};

}

