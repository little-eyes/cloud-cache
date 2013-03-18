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
#include "configure.h"

namespace std {

ShardingProvider::ShardingProvider() {

};

ShardingProvider::~ShardingProvider() {

};

string ShardingProvider::getTaskShardingByIp(const string &key) {
	return SLAVE_HOSTS[ElfHash(key)];
};

int ShardingProvider::getTaskShardingByIndex(const string &key) {
	return ElfHash(key);
}

string ShardingProvider::getCacheShardingByIp(const string &key) {
	return DATA_HOSTS[XorHash(key)];
};

int ShardingProvider::getCacheShardingByIndex(const string &key) {
	return XorHash(key);
}

string ShardingProvider::sha1(const string &key) {

	return NULL;
};

/* ELF hash used to shard the data host. */
int ShardingProvider::ElfHash(const string &key) {
	unsigned long long h = 0, g = 0;
	for (int i = 0; i < key.length(); ++i) {
		h = (h << 4) + key[i];
		g = h & 0xf0000000L;
		if (g != 0)
			h ^= g >> 24;
		h &= ~g;
	}
	return (int)(h % NUM_DATA_HOSTS);
};

/* Shift-Add-Xor hash is used to shard slave host. */
int ShardingProvider::XorHash(const string &key) {
	unsigned int h = 0;
	for (int i = 0; i < key.length(); ++i)
		h ^= ( h << 5 ) + ( h >> 2 ) + key[i];
	return (int)(h % NUM_SLAVE_HOSTS);
};

}
