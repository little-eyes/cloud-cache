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


class SlaveThreadedTcpRequestHandler(SocketServer.BaseRequestHandler):
	'''The slave handler to run a single kernel-solver.'''
	def handle(self):
		pass


class SlaveThreadedTcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass


if __name__ == '__main__':
	# start the TCP server and always listen to the task from Master Node.
	NetworkMgr = tools.LocalNetworkManager()
	IpAddress = NetworkMgr.getLocalIpAddress()
	SlaveServer = SlaveThreadedTcpServer((IpAddress, configure.SLAVE_PORT), 
		SlaveThreadedTcpRequestHandler)
	SlaveServerThread = threading.Thread(target=SlaveServer.serve_forever)
	SlaveServerThread.start()
