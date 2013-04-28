'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	The sample client script to run an 3-SAT solver. Before running the client,
	one should load the data file to the Master Node, then once the Master Node
	receive the client request, it will start the cloud-cache kernel solver.

	If you are willing to solve other problem, write your kernel solver, then
	give a command to your problem, run the client again. Your results are expected
	to be in the Sinker Node.

	Alternatively, if any NFS or HDFS environment is available, this framework
	can benefit a lot and reduce a large amount of job distribution time. So the
	throughput could be even higher.
'''


import socket
import configure

def command(ip, port, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, port))
	try:
		sock.sendall(message)
	finally:
		sock.close()


if __name__ == '__main__':
	command(configure.MASTER_NODE[0], 
			configure.MASTER_PORT,
			'3-sat')
