from queueSimulator import queueSimulator
from queueClass import Queue

q1 = Queue('q1', 1, 5, 2, 5, 3, 5)
q2 = Queue('q2', 2, 5, 2, 5, 3, 5)

simulator1 = queueSimulator(100000, 12345, 2, q1)
simulator2 = queueSimulator(100000, 12345, 2, q2)

print("Simulation 1: G/G/1/5")
simulator1.simulate()
print("Simulation 2: G/G/2/5")
simulator2.simulate()
