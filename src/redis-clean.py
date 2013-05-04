'''
	CS594 Cloud Computing Course Project
	Author: Jilong Liao (jliao2@utk.edu)

	This file is used to cleanup the Redis server on Data Node.
'''


import redis

connection = redis.Redis()
pipe = connection.pipeline()

for key in connection.keys():
	pipe.delete(key)

pipe.execute()

