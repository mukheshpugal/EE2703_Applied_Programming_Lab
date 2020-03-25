import sys

#Reading arguments

if (len(sys.argv) < 2):
	print("Enter netlist file name as argument")
	exit()

if (len(sys.argv) > 2):
	print("Too many arguments")
	exit()

#Reading netlist file

try:
	with open(sys.argv[1]) as f:
		lines = f.readlines()
except FileNotFoundError:
	print("File not found")
	exit()

#Parsing lines

circuits = []
currentCircuit = []
startCircuit = False

for line in lines:
	if (line[-1:] == "\n"):
		line = line[:-1]
	if (line == ".circuit"):
		startCircuit = True
	elif (startCircuit):
		if (line == ".end"):
			circuits.append(currentCircuit)
			currentCircuit = []
			startCircuit = False
		else:
			currentCircuit.append(line.split())

#Printing in reverse order

for _ in range(len(circuits)):
	for component in reversed(circuits[_]):
		print(' '.join(component[::-1]))
	print()
