'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	The Kernel package is the place to define and implement any kind of
	kernel-solver. Each task needs a kernel-solver to solve. The 
	kernel-solver can use the cloud cache to speed up the process,
	but it runs only on ONE machine. Cloud Cache provides the query APIs
	to see if there is existing results in the cloud.
'''
import logging
import tools


# setup logging.
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class BaseKernel3SAT(object):
	'''the brute-force approach to solve 3-SAT problem.'''
	def __init__(self, task, pool):
		self._NumberOfVariable = eval(task.split(',')[0])
		self._NumberOfExpression = eval(task.split(',')[1])
		self._Expression = [eval(o) for o in task.split(',')[2:]]
		self._Assignment = [False for o in range(self._NumberOfVariable)]
		self._Pool = pool
		logging.info('BaseKernel 3-SAT initialized. n = %d, m = %d', 
			self._NumberOfVariable, self._NumberOfExpression)
			
	def solve(self):
		'''public interface for the base kernel-solver.'''
		solution = self._RecurrsiveSolve(self._Assignment, 0)
		selector = tools.DataNodeSelector(self._Expression)
		storageMgr = tools.PersistentStorageManager(self._Pool[selector.getDataNode()])
		storageMgr.push(self._Expression, solution)
		logging.info('Solution cached in the Redis ...')
		return solution

	def _RecurrsiveSolve(self, assignment, index):
		'''internal recurrsive solution.'''
		if index == len(assignment):
			result = self._AssignmentValidation(self._Expression, assignment)
			if result:
				return assignment
			else:
				return []
		result = self._RecurrsiveSolve(assignment, index + 1)
		if result != []:
			return result
		assignment[index] = (not assignment[index])
		result = self._RecurrsiveSolve(assignment, index + 1)
		if result != []:
			return result
		return []

	def _AssignmentValidation(self, expression, assignment):
		'''expression and assignment are lists.'''
		result = True
		for i in range(len(expression)/3):
			a = expression[i*3]
			b = expression[i*3 + 1]
			c = expression[i*3 + 2]
			va = assignment[abs(a)] if a > 0 else (not assignment[abs(a)])
			vb = assignment[abs(b)] if b > 0 else (not assignment[abs(b)])
			vc = assignment[abs(c)] if c > 0 else (not assignment[abs(c)])
			result &= (va | vb | vc)
			if not result:
				return False
		return True


class CloudCacheKernel3SAT(object):
	'''the cloud cache approach to solve the 3-SAT problem.'''
	def __init__(self, task, pool):
		self._NumberOfVariable = eval(task.split(',')[0])
		self._NumberOfExpression = eval(task.split(',')[1])
		self._Expression = [eval(o) for o in task.split(',')[2:]]
		self._Assignment = [False for o in range(self._NumberOfVariable)]
		self._BaseKernel = BaseKernel3SAT(task, pool)
		self._Pool = pool
		logging.info('CloudCacheKernel 3-SAT initialized. n = %d, m = %d', 
			self._NumberOfVariable, self._NumberOfExpression)

	def solve(self):
		# linear traverse the problem and query the Redis server.
		for i in range(0, len(self._Expression), 3):
			subtask = self._Expression[i:]
			selector = tools.DataNodeSelector(subtask)
			storageMgr = tools.PersistentStorageManager(self._Pool[selector.getDataNode()])
			assignment = storageMgr.query(subtask)
			if assignment == []:
				logging.info('*** Cache Hit! ***')
				return []
			if assignment != None and self._AssignmentValidation(self._Expression, assignment):
				storageMgr.push(self._Expression, assignment)
				logging.info('*** Cache Hit! ***')
				return assignment
		# if query failed, then use base kernel to solve.
		return self._BaseKernel.solve()

	def _AssignmentValidation(self, expression, assignment):
		'''expression and assignment are lists.'''
		result = True
		for i in range(len(expression)/3):
			a = expression[i*3]
			b = expression[i*3 + 1]
			c = expression[i*3 + 2]
			if abs(a) >= len(assignment) or abs(b) >= len(assignment) or abs(c) >= len(assignment):
				return False
			va = assignment[abs(a)] if a > 0 else (not assignment[abs(a)])
			vb = assignment[abs(b)] if b > 0 else (not assignment[abs(b)])
			vc = assignment[abs(c)] if c > 0 else (not assignment[abs(c)])
			result &= (va | vb | vc)
			if not result:
				return False
		return True
