'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	This package provides some tools such as load/store data, load balance,
	hash functions, etc.
'''


import socket


class JobDataHelper(object):
	'''load/store job data'''
	def loadFromDisk(self, uri):
		'''the data will be string array, each string is a task.'''
		data = []
		with open(uri, 'r') as dataReader:
			data = dataReader.readlines()
		return data

	def storeToDisk(self, data, uri):
		'''write the string array data to the specific data URI.'''
		dataWriter = open(uri, 'w')
		for line in data:
			dataWriter.write(line + '\n')


class LoadBalanceHelper(object):
	pass


class HashFunctionProvider(object):
	pass


class MessageSender(object):
	'''send a message to any destination through TCP connection.'''
	def __init__(self, ip, port, message):
		self._Ip = ip
		self._Port = port
		self._Message = message
	
	def send(self):
		sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sendSocket.connect((self._Ip, self._Port))
		try:
			sendSocket.sendall(message)
		finally:
			sendSocket.close()


class LocalNetworkManager(object):
	'''manage the local network environment, such as local IP address.'''
	def getLocalIpAddress(self):
		probeSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		probeSocket.connect(("www.google.com",80))
		IpAddress = probeSocket.getsockname()[0]
		probeSocket.close()
		return IpAddress

