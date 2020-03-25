import numpy as np

class Circuit:

	def __init__(self, lines, name):
		self.name = name
		self.components = []
		self.vSources = []
		self.k = 0
		self.freq = 0

		# Parsing lines
		inCircuit = False
		for line in lines:
			if ('#' in line):
				line = line.split("#", 1)[0]
			if (line[-1] == "\n"):
				line = line[:-1]
			if (line == ".circuit"):
				inCircuit = True
			elif (inCircuit):
				if (line == ".end"):
					inCircuit = False
				else:
					self.addComponent(line.split())
			if (line[:3] == '.ac'):
				self.setFreq(2 * np.pi * float(line.split()[-1]))

		# self.printVals()

	def setFreq(self, freq):
		self.freq = freq
		for component in self.components:
			if freq != 0:
				if component.type == 'L':
					component.value *= 1j * freq
				if component.type == 'C':
					component.value = -1j / (freq * component.value)

	def addComponent(self, component):
		if (not isinstance(component, (Component, list))):
			print("Invalid Component")
		else:
			if (isinstance(component, list)):
				component = Component(component)
			if component.type in ('V', 'E', 'H'):
				component.assignNumber(self.k)
				self.vSources.append(component)
				self.k += 1
			self.components.append(component)

	def printVals(self):

		# Prints details of all the components
		print()
		print("Circuit " + self.name + " :")
		for _ in range(len(self.components)):
			print("Component " + str(_ + 1) + " : ", end = '')
			self.components[_].printVals()
		print()

	def solve(self):

		# Making a list of nodes
		self.nodes = ['GND']
		for comp in self.components:
			for node in comp.nodes:
				if node not in self.nodes:
					self.nodes.append(node)

		for comp in self.components:
			comp.nodes = [self.nodes.index(node) for node in comp.nodes]

		n = self.n = len(self.nodes)
		k = self.k

		# Constructing M & b
		M = np.zeros((k + n, k + n), dtype = (float if self.freq == 0 else complex))
		b = np.zeros((k + n), dtype = (float if self.freq == 0 else complex))
		M[0][0] = 1

		for i in range(1,n):
			for comp in self.components:
				if i in comp.nodes[:2]:	
					if comp.type in ('R', 'L', 'C'):
						M[i][i] += 1 / comp.value
						M[i][comp.nodes[1 - comp.nodes.index(i)]] -= 1 / comp.value

					if comp.type in ('V', 'E', 'H'):
						M[i][n + comp.number] += (1 if comp.nodes[0] == i else -1)

					if comp.type == 'I':
						b[i] += (comp.value * (-1 if comp.nodes[0] == i else 1))

					if comp.type == 'G':
						M[i][comp.nodes[2]] -= comp.value
						M[i][comp.nodes[3]] += comp.value

					if comp.type == 'F':
						M[i][n + [v.number for v in self.vSources if comp.source == v.name][0]] -= comp.value

		for comp in self.components:
			if comp.type in ('V', 'E', 'H'):	
				M[n + comp.number][comp.nodes[0]] -= 1
				M[n + comp.number][comp.nodes[1]] += 1

				if comp.type == 'V':
					b[n + comp.number] += comp.value

				if comp.type == 'E':
					M[n + comp.number][comp.nodes[2]] += comp.value
					M[n + comp.number][comp.nodes[3]] -= comp.value

				if comp.type == 'H':
					M[n + comp.number][n + [v.number for v in self.vSources if comp.source == v.name][0]] -= comp.value


		# print(M, b)
		# Finding the solution and formatting display
		self.solution = list(np.linalg.solve(M,b))
		self.nodeV = [self.nodes[i] + " : " + str(self.solution[i]) for i in range(n)]
		self.iThroughV = [self.vSources[i].name + " : " + str(self.solution[i + n]) for i in range(k)]


	def printSolution(self):

		# Prints the solution
		if 'self.nodeV' not in locals():
			self.solve()

		print()
		print('Circuit ' + str(self.name) + " :")
		print("Node Voltages : ", end = '')
		print(self.nodeV)
		print("Currents through voltage sources : ", end = '')
		print(self.iThroughV)


class Component:

	def __init__(self, listIn):
		self.name, *self.nodes, self.value = listIn

		try:
			self.value = float(self.value)
		except ValueError:
			self.value = 0.0
		self.type = self.name[0]

		self.nodes = [str(node) for node in self.nodes]

		if (self.nodes[-1] == 'dc'):
			self.nodes = self.nodes[:2]

		if (self.nodes[-2] == 'ac'):
			self.value = float(self.nodes[-1]) * (np.cos(self.value) + 1j * np.sin(self.value)) / 2
			self.nodes = self.nodes[:2]

		if (self.nodes[-1][0] == 'V'):
			self.source = self.nodes[-1]
			self.nodes = self.nodes[:-1]

	def assignNumber(self, num):
		self.number = num

	def printVals(self):
		print(self.type, self.name, self.nodes, self.value)
