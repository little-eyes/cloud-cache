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

namespace std {

StorageConnector::StorageConnector(const string &key) {
	__context = redisConnect(key.c_str(), 6379);
};

StorageConnector::~StorageConnector() {

};

int StorageConnector::getShardingHashCode(const string &key) {
	return 0;
};

redisContext *StorageConnector::getContext() {
	return __context;
};

DataManager::DataManager(const StorageConnector *connector) {
	__connector = connector;
};

DataManager::~DataManager() {

};

/*
 * The query will goes to the the Redis server,
 * return the string if the key found, otherwise
 * the empty string is returned.
 * */
string DataManager::get(const string &key) {
	redisReply *reply = redisCommand(
		__connector->getContext(), "GET %s", key.c_str());
	string reply_str(reply->str);
	if (reply->str == NULL) {
		freeReplyObject(reply);
		return "";
	}  
    else {
		freeReplyObject(reply);
		return reply_str;
	}
};

bool DataManager::put(const string &key, const string &value) {
	redisReply *reply = redisCommand(
		__connector->getContext(), "SET %s %s", key.c_str(), value.c_str());
	if (reply == NULL) {
		freeReplyObject(reply);
		return false;
    }
    else {
		freeReplyObject(reply);
		return true;
	}
};


}
