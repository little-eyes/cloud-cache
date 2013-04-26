'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	This file is the Master Node design. The Master Node is used to
	accept the job from the client, then distribute the jobs to many
	different Slave Node. The Master Node needs to know the global
	configuration of the system.

	The Master Node has the two-way TCP communication between any
	Slave Node. The communication port can be configured from the
	configure.py.
'''


import socket
import threading
import SocketServer
import tools
import configure


# Global variables.
ExecutionBookKeeper = {}

class MasterThreadedTcpHandler(SocketServer.BaseRequestHandler):
	'''listen to the results from the Slave Node. '''
	def handle(self):
		pass


class MasterThreadedTcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == '__main__':
	# start the Master Node as daemon.
	MasterServer = MasterThreadedTcpServer((configure.MASTER_NODE[0], 
		configure.MASTER_PORT), MasterThreadedTcpHandler)
	MasterServerThread = threading.Thread(target=MasterServer.serve_forever)
	MasterServerThread.daemon = True
	MasterServerThread.start()

	# start load job

	# turn off Tcp server.
	MasterServer.shutdown()
