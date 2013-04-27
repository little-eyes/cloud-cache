'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	This package provides some tools such as load/store data, load balance,
	hash functions, etc.
'''


import socket
import configure
import simplejson
import redis
import logging


# setup logger.
logging.basicConfig(level=logging.DEBUG)


class JobDataHelper(object):
	'''load/store job data'''
	def loadFromDisk(self, uri):
		'''the data will be string array, each string is a task.'''
		data = []
		with open(uri, 'r') as dataReader:
			data = dataReader.readlines()
		logging.info('Job data loaded, total tasks = %d', len(data))
		return data

	def storeToDisk(self, data, uri):
		'''write the result list to the specific data URI.'''
		dataWriter = open(uri, 'w')
		for line in data:
			dataWriter.write(self._serializeArray(line) + '\n')
		logging.info('Jon results stored, total results = %d', len(data))

	def _serializeArray(self, array):
		'''serialize the array to a string.'''
		sequence = ''
		for item in array:
			sequence += str(array) + ','
		return sequence[0:len(sequence)-1]


class SlaveNodeSelector(object):
	'''the Slave Node selector for a task.'''
	def __init__(self, status):
		self._SlaveNodeStatusTable = status
	
	def select(self):
		for slave in self._SlaveNodeStatusTable.keys():
			if self._SlaveNodeStatusTable[slave] == configure.SLAVE_STATUS_READY:
				return slave
		return configure.SLAVE_STATUS_NOT_AVAILABLE


class TaskIssuer(object):
	'''issue the task to the Slave Node.'''
	def __init__(self, slave, task):
		self._Ip = slave
		self._Port = configure.SLAVE_PORT
		self._Task = self._serialzeTask(task)
	
	def _serializeTask(self, task):
		return simplejson.dumps({'task':task})

	def issue(self):
		sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sendSocket.connect((self._Ip, self._Port))
		try:
			sendSocket.sendall(self._Task)
		except socket.error:
			logging.warn('Task issue failed because socket failure ...')
		finally:
			sendSocket.close()


class TaskReporter(object):
	'''report the task results to the Master Node'''
	def __init__(self, task, result):
		self._Ip = configure.MASTER_NODE[0]
		self._Port = configure.MASTER_PORT
		self._Report = self._serializeReport(task, result)
	
	def _serializeReport(self, task, result):
		return simplejson.dumps({'task':self._Task, 'result':self._Result})

	def report(self):
		sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sendSocket.connect((self._Ip, self._Port))
		try:
			sendSocket.sendall(self._Report)
		except socket.error:
			logging.warn('Task report failed because socket failure ...')
		finally:
			sendSocket.close()

class LocalNetworkManager(object):
	'''manage the local network environment, such as local IP address.'''
	def getLocalIpAddress(self):
		probeSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		probeSocket.connect(("www.google.com",80))
		IpAddress = probeSocket.getsockname()[0]
		logging.info('Slave Node service IP: %s', IpAddress)
		probeSocket.close()
		return IpAddress
	
	def probeHost(self, host, port):
		probeSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		probeSocket.settimeout(1.0) # timeout is set to be 1 second.
		probeSocket.connect((host, port))
		try:
			probeSocket.sendall(configure.MASTER_PROBE_MESSAGE)
			response = probeSocket.recv(1024).strip()
			return True if response == configure.SLAVE_READY_MESSAGE else False
		except socket.timeout:
			logging.info('Slave Node probe failure: %s ', host)
		finally:
			probeSocket.close()

class PersistentStorageManager(object):
	'''manage the persistent key/value (both JSON strings) storage on Redis server.'''
	def __init__(self):
		self._RedisConnector = redis.Redis()

	def query(self, key):
		'''query if the given key exist.'''
		return self._RedisConnector.get(key)

	def push(self, key, value):
		'''cache the solution to the redis server. return True/False.'''
		return self._RedisConnector.set(key, value)
