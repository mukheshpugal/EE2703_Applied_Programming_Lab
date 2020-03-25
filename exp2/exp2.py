class Circuit:

	def __init__(self, name):
		self.name = name
		self.components = []

	def addComponent(self, component):
		if (not isinstance(component, (Component, list))):
			print("Invalid Component")
		else:
			if (isinstance(component, list)):
				component = Component(component)
			self.components.append(component)

	def printVals(self):
		print("Circuit " + self.name + " :")
		for _ in range(len(self.components)):
			print("Component " + str(_ + 1) + " : ", end = '')
			self.components[_].printVals()
		print()

	# def solve(self):
		

class Component:

	def __init__(self, listIn):
		self.name, *self.nodes, self.value = listIn

	def printVals(self):
		print(self.name, self.nodes, self.value)
		

# c = Circuit()
# c.addComponent(Component(['V1432', 'n1', 'n2', 1.24]))
# c.addComponent(['X1432', 'n1', 'n2', 'n3', 2.24])
# c.addComponent(3)
# c.printVals()