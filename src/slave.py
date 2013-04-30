'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	The Slave Node is the machine to run the job coming from the
	Master Node. Besides, each Slave Node has a Redis server running
	on localhost. The Redis Server is used to store the data which
	has been previously calcuated, then the next time the Redis server
	is able to provide the existing solutions for any <key, value> pair.

	Slave Node is mutli-thread enabled in order to speed up the whole
	batch process from the Master Node.

	The Slave Node also has a two-way communication channel with the
	Master Node. No automatical start process is provided at the current
	stage, so the Slave Node needs to be turned on manually.
'''


import socket
import threading
import SocketServer
import tools
import configure
import simplejson
import kernel
import logging
import time
import redis
import csv


# setup logging.
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


# statistics collection.
runtime = csv.writer(open(configure.RUNTIME_COLLECTION_URI, 'a'), delimiter=',')


# global variable
DataNodeConnectionPool = {}
ReportChunk = ''
ReportCounter = 0


# global initialization
def GlobalInitialization():
	global DataNodeConnectionPool
	for node in configure.DATA_NODE:
		DataNodeConnectionPool[node] = redis.ConnectionPool(host=node)
		logging.info('Estabilished Redis connection: %s', node)


class SlaveThreadedTcpRequestHandler(SocketServer.BaseRequestHandler):
	'''The slave handler to run a single kernel-solver.'''
	def handle(self):
		# receive and extrac the task chunk.
		logging.info('Receive job from Master ...')
		message = ''
		while True:
			chunk = self.request.recv(4096).strip()
			message += chunk
			if len(chunk) == 0:
				break
		
		logging.info('Job has been received ...')
		subjob = simplejson.loads(message)
		# run the kernel-solver for each task.
		global DataNodeConnectionPool, ReportCounter, ReportChunk
		for task in subjob:
			#solver = kernel.CloudCacheKernel3SAT(task, DataNodeConnectionPool)
			solver = kernel.BaseKernel3SAT(task, DataNodeConnectionPool)
			__start_timer__ = time.time() # statistics collection.
			result = solver.solve()
			__end_timer__ = time.time()
			logging.info('Task finished, cost = %f ...', __end_timer__ - __start_timer__)
			runtime.writerow([__end_timer__, __start_timer__])
			# report the results.
			reporter = tools.TaskReporter()
			if ReportCounter < configure.REPORT_CHUNK_SIZE:
				ReportChunk = reporter.combine(ReportChunk, task, result)
				ReportCounter += 1
			else:
				reporter.report(ReportChunk)
				ReportCounter = 0


class SlaveThreadedTcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass


if __name__ == '__main__':
	# global initialization.
	GlobalInitialization()
	
	# start the TCP server and always listen to the task from Master Node.
	NetworkMgr = tools.LocalNetworkManager()
	IpAddress = NetworkMgr.getLocalIpAddress()
	logging.info('** Slave Node service at %s:%d **', str(IpAddress), configure.SLAVE_PORT)
	SlaveServer = SlaveThreadedTcpServer((IpAddress, configure.SLAVE_PORT), 
		SlaveThreadedTcpRequestHandler)
	SlaveServerThread = threading.Thread(target=SlaveServer.serve_forever)
	SlaveServerThread.start()
