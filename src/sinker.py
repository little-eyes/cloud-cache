'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	The Sink Node is used to receive all the solutions comes out
	of the Slave Node which is isolated from the Master Node.

	The change of the design comes from a benchmark which indicates
	the Master Node cannot bear the burden from many Slave Node. Then
	the execution efficiency becomes slow.
'''


import socket
import threading
import SocketServer
import tools
import configure
import logging
import simplejson
import time


# setup logging.
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


# global variable.
DataSinkHandler = open(configure.JOB_OUTPUT_URI, 'a')


class SinkerThreadedTcpHandler(SocketServer.BaseRequestHandler):
	'''listen to the results from the Slave Node and udpate the status.'''
	def handle(self):
		# receive the <task, result> pair.
		message = ''
		while True:
			chunk = self.request.recv(4096).strip()
			if len(chunk) == 0:
				break
			message += chunk
		# store.
		helper = tools.JobDataHelper()
		global DataSinkHandler
		helper.sinkToDisk(message, DataSinkHandler)
		logging.info('Receive solution updates from Slave Node %s', self.client_address[0])


class SinkerThreadedTcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == '__main__':
	# start the Sinker Node as daemon.
	NetworkMgr = tools.LocalNetworkManager()
	IpAddress = NetworkMgr.getLocalIpAddress()
	SinkerServer = SinkerThreadedTcpServer((IpAddress, configure.SINKER_PORT), 
		SinkerThreadedTcpHandler)
	logging.info('** Sinker Node running at %s:%d', str(IpAddress), configure.SINKER_PORT)
	SinkerServerThread = threading.Thread(target=SinkerServer.serve_forever)
	SinkerServerThread.start()
