'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	The global configuration file, both Master Node and Slave Nodes
	rely on this file to configure the system.
'''

MASTER_NODE = ['10.208.175.127']
SLAVE_NODE = ['10.198.129.131', '10.210.205.29', '10.96.37.25', '10.96.245.71']

MASTER_PORT = 12530
SLAVE_PORT = 12531


SLAVE_STATUS_READY = '0'
SLAVE_STATUS_BUSY = '1'
SLAVE_STATUS_NOT_AVAILABLE = '2'


TASK_STATUS_READY = '3'
TASK_STATUS_WORKING = '4'
TASK_STATUS_FINISHED = '5'

JOB_DATA_INPUT_URI = 'external/3-sat.in'
JOB_OUTPUT_URI = 'solution.txt'
