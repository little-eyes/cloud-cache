import redis

connection = redis.Redis()
pipe = connection.pipeline()

for key in connection.keys():
	pipe.delete(key)

pipe.execute()

