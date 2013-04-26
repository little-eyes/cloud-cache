'''
	CS594 Cloud Computing Course Project.
	Author: Jilong Liao (jliao2@utk.edu)

	The Kernel package is the place to define and implement any kind of
	kernel-solver. Each task needs a kernel-solver to solve. The 
	kernel-solver can use the cloud cache to speed up the process,
	but it runs only on ONE machine. Cloud Cache provides the query APIs
	to see if there is existing results in the cloud.
'''


class BaseKernel3SAT(object):
	'''the brute-force approach to solve 3-SAT problem.'''
	def __init__(self, task):
		self._NumberOfVariable = eval(task.split(',')[0])
		self._NumberOfExpression = eval(task.split('.')[1])
		self._Expression = [eval(o) for o in task.split('.')[2:]]
		self._Assignment = [False for o in range(self._NumberOfVariable)]
		
	def solve(self):
		'''public interface for the base kernel-solver.'''
		return self._RecurrsiveSolve(self._Expression, 0)

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
	pass
