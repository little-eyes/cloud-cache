'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	The global configuration file, both Master Node and Slave Nodes
	rely on this file to configure the system.
'''

MASTER_NODE = ['10.208.175.127']
#MASTER_NODE = ['domU-12-31-39-06-A8-71.compute-1.internal']
#MASTER_NODE = ['ec2-54-234-172-153.compute-1.amazonaws.com']
#MASTER_NODE = ['localhost']
SLAVE_NODE = ['10.198.129.131', '10.210.205.29', '10.96.37.25', '10.96.245.71']
#SLAVE_NODE = ['domU-12-31-39-10-82-79.compute-1.internal', 'domU-12-31-39-09-CA-D3.compute-1.internal', 'domU-12-31-39-16-26-EF.compute-1.internal', 'domU-12-31-39-16-F6-BD.compute-1.internal']
#SLAVE_NODE = ['ec2-54-225-2-34.compute-1.amazonaws.com', 'ec2-54-242-129-207.compute-1.amazonaws.com', 'ec2-54-225-22-165.compute-1.amazonaws.com', 'ec2-50-16-144-197.compute-1.amazonaws.com']
#PRIVATE_TO_PUBLIC_TABLE = {'10.198.129.131':'ec2-54-225-2-34.compute-1.amazonaws.com', '10.210.205.29':'ec2-54-242-129-207.compute-1.amazonaws.com', '10.96.37.25':'ec2-54-225-22-165.compute-1.amazonaws.com', '10.96.245.71':'ec2-50-16-144-197.compute-1.amazonaws.com'}
#MASTER_NODE = ['192.168.10.144']
#SLAVE_NODE = ['192.168.10.144'] 

MASTER_PORT = 12535
SLAVE_PORT = 12536


SLAVE_STATUS_READY = '0'
SLAVE_STATUS_BUSY = '1'
SLAVE_STATUS_NOT_AVAILABLE = '2'


TASK_STATUS_READY = '3'
TASK_STATUS_WORKING = '4'
TASK_STATUS_FINISHED = '5'

MASTER_PROBE_MESSAGE = '6'
SLAVE_READY_MESSAGE = '7'

JOB_DATA_INPUT_URI = 'external/3-sat.in'
JOB_OUTPUT_URI = 'solution.txt'
