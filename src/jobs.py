'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	This package defines the complete workflow of a Job. For example,
	the 3-SAT problem, we may be asked to solve 1 million expressions,
	then the complete job flow includes: load expression, solve single
	expression with kernel-solver, and receive the results.
'''


class Base3SATJob(object):
	pass
