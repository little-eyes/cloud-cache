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


# setup logging.
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class SlaveThreadedTcpRequestHandler(SocketServer.BaseRequestHandler):
	'''The slave handler to run a single kernel-solver.'''
	def handle(self):
		# receive and extract task.
		message = self.request.recv(4096).strip()
		# special case for probe message.
		if message == configure.MASTER_PROBE_MESSAGE:
			self.request.sendall(configure.SLAVE_READY_MESSAGE)
		else:	
			logging.info('Receive task from Master ...')
			task = simplejson.loads(message)['task']
			# run the kernel-solver for the task.
			solver = kernel.CloudCacheKernel3SAT(task)
			__start_timer__ = time.time() # statistics collection.
			result = solver.solve()
			__end_timer__ = time.time()
			logging.info('Task finished, cost = %f ...', __end_timer__ - __start_timer__)
			# report the results.
			reporter = tools.TaskReporter(task, result)
			reporter.report()


class SlaveThreadedTcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass


if __name__ == '__main__':
	# start the TCP server and always listen to the task from Master Node.
	NetworkMgr = tools.LocalNetworkManager()
	IpAddress = NetworkMgr.getLocalIpAddress()
	logging.info('** Slave Node service at %s:%d **', str(IpAddress), configure.SLAVE_PORT)
	SlaveServer = SlaveThreadedTcpServer((IpAddress, configure.SLAVE_PORT), 
		SlaveThreadedTcpRequestHandler)
	SlaveServerThread = threading.Thread(target=SlaveServer.serve_forever)
	SlaveServerThread.start()
