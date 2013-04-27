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
TaskStatusTable = {}
SlaveNodeStatusTable = {}
TaskSolutionTable = {}
JobProgress = 0

def GlobalInitialization():
	'''the global initialization function.'''
	global TaskStatusTable
	global SlaveNodeStatusTable
	global TaskSolutionTable
	global JobProgress
	TaskStatusTable = {}
	SlaveNodeStatusTable = {}
	TaskSolutionTable = {}
	JobProgress = 0

class CloudCache3SATJob(object):
	'''the brute-force 3-SAT batch job.'''
	def __init__(self, inUri, outUri):
		self._InputUri = inUri
		self._OutputUri = outUri
		self._Helper = tools.JobDataHelper()
		self._Data = self._Helper.loadFromDisk(self._InputUri)
	
	def execute(self):
		'''for each task, select proper Slave Node to execute.'''
		while JobProgress < len(self._Data):
			# select a task.
			task = ''
			for item in self._Data:
				if item not in TaskStatusTable.keys():
					task = item
					break
					
			# select a Slave Node if possible.
			selector = tools.SlaveNodeSelector(SlaveNodeStatusTable)
			slave = selector.select()
			if slave == configure.SLAVE_STATUS_NOT_AVAILABLE:
				continue

			# issue the task to slave, update the status information.
			issuer = tools.TaskIssuer(slave, task)
			issuer.issue()
			TaskStatusTable[task] = configure.TASK_STATUS_WORKING
			SlaveNodeStatusTable[slave] = configure.SLAVE_STATUS_BUSY
			JobProgress += 1
		# when finished, store the results to disk.
		results = [TaskSolutionTable[task] for task in self._Data]
		self._Helper.storeToDisk(results, self._OutputUri)


class MasterThreadedTcpHandler(SocketServer.BaseRequestHandler):
	'''listen to the results from the Slave Node and udpate the status.'''
	def handle(self):
		# receive the <task, result> pair.
		message = self.request.recv(4096).strip()
		message = simplejson.load(message)
		task = message['task']
		result = message['result']
		# update status.
		TaskStatusTable[task] = configure.TASK_STATUS_FINISHED
		SlaveNodeStatusTable[self.client_address[0]] = configure.SLAVE_NODE_READY
		TaskSolutionTable[task] = result


class MasterThreadedTcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == '__main__':
	# global initialization.
	GlobalInitialization()
	
	# start the Master Node as daemon.
	MasterServer = MasterThreadedTcpServer((configure.MASTER_NODE[0], 
		configure.MASTER_PORT), MasterThreadedTcpHandler)
	MasterServerThread = threading.Thread(target=MasterServer.serve_forever)
	MasterServerThread.daemon = True
	MasterServerThread.start()

	# start load job
	job = CloudCache3SATJob(configure.JOB_DATA_INPUT_URI, configure.JOB_OUTPUT_URI)
	job.execute()

	# turn off Tcp server.
	MasterServer.shutdown()
