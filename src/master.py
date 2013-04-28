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
import logging
import simplejson
import time


# setup logger.
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


# global varibles.
SlaveNodeStatusTable = {}
SlaveNodeCheckinTable = {}

# global function.
def SlaveNodeRegistration():
	'''register the slave node initially.'''
	global SlaveNodeStatusTable, SlaveNodeCheckinTable
	NetworkMgr = tools.LocalNetworkManager()
	for slave in configure.SLAVE_NODE:
		if not NetworkMgr.probeHost(slave, configure.SLAVE_PORT):
			continue
		SlaveNodeStatusTable[slave] = configure.SLAVE_STATUS_READY
		SlaveNodeCheckinTable[slave] = time.time()
		logging.info('Slave Node Registration %s: success! ...', slave)


class CloudCache3SATJob(object):
	'''the brute-force 3-SAT batch job.'''
	def __init__(self, inUri, outUri):
		self._InputUri = inUri
		self._OutputUri = outUri
		self._Helper = tools.JobDataHelper()
		self._Data = self._Helper.loadFromDisk(self._InputUri)
	
	def distribute(self):
		NumberOfSlaveNodes = len(configure.SLAVE_NODE)
		JobSplit = {}
		for slave in configure.SLAVE_NODE:
			if SlaveNodeStatusTable[slave] == configure.SLAVE_STATUS_READY:
				JobSplit[slave] = []
		# split the job.
		JobChunkSize = len(self._Data)/NumberOfSlaveNodes
		k = 0
		for slave in JobSplit.keys():
			JobSplit[slave] = self._Data[k*JobChunkSize : min((k+1)*JobChunkSize, len(self._Data))]
			k += 1
			logging.info('Split job to Slave Node %s, totoal amount = %d ... ', slave, len(JobSplit[slave]))
		# distribute subjob to Slave Node.
		for slave in JobSplit.keys():
			manager = tools.JobDispatcher(slave, JobSplit[slave])
			logging.info('start job distribution for Slave Node %s', slave)
			manager.dispatch()
			logging.info('%d task has been distribute to Slave Node %s', len(JobSplit[slave]), slave)
			JobSplit[slave] = None # clean up the memory.
		# cleanup the memory copy.
		self._Data = None


class MasterThreadedTcpHandler(SocketServer.BaseRequestHandler):
	'''listen to the results from the Slave Node and udpate the status.'''
	def handle(self):
		# receive the job submission from client.
		command = self.request.recv(4096).strip()
		if command == configure.COMMAND_3_SAT:
			SlaveNodeRegistration()
			job = CloudCache3SATJob(configure.JOB_DATA_INPUT_URI, configure.JOB_OUTPUT_URI)
			job.distribute()

class MasterThreadedTcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == '__main__':
	# start the Master Node.
	MasterServer = MasterThreadedTcpServer((configure.MASTER_NODE[0], 
		configure.MASTER_PORT), MasterThreadedTcpHandler)
	MasterServerThread = threading.Thread(target=MasterServer.serve_forever)
	MasterServerThread.start()
