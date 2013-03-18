/*
 * For Course Project: CS594 Cloud Computing
 *
 * Authors: 
 *     * Jilong Liao (jliao2@utk.edu)
 *     * Yue Tong (ytong32@utk.edu)
 *     * Lipeng Wan (??)
 *
 * This file implements the classes for the cloud
 * cache's operations and APIs. For example the 
 * query() and insert() operation. The classes will 
 * be used in solver to interact with the cache.
 *
 * Cloud cache is supported by Redis server, which
 * the current version Redis-2.6.11 is required for
 * the cache. The developer needs to clearly specify
 * a data structure needed to store the results in
 * the cache.
 * 
 * In this layer, CloudCache needs to handle the
 * sharding issue for performance reason. The exposed
 * public APIs should not bother upper layer to consider
 * the sharding issues etc.
 *
 * Note: measure everything!
 *
 * Dependency: C++11, C++ Boost Library, Redis C Client.
 */

#include <string>
#include "ccache.h"
#include "configure.h"

namespace std {

CloudCache::CloudCache() {
	
};

CloudCache::~CloudCache() {

};

/*
 * The query will goes to the the Redis server,
 * return the string if the key found, otherwise
 * the NULL pointer is returned.
 * */
string CloudCache::query(const string &key) {

	return NULL;
};

bool insert(const string &key, const string &value) {

	return true;
};


int CloudCache::getShardingHashCode(const string &key) {

	return 0;
};

}
