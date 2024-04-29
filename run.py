from queueSimulator import queueSimulator
from queueClass import Queue
import configparser

inf = 999999

# leitura do arquivo de configuracao
config = configparser.ConfigParser()
config.read("config.ini")
firstArrivalTime = eval(config.get("configfile", "firstArrivalTime"))
quantityRandomNumbers = int(config.get("configfile", "quantityRandomNumbers"))
seed = int(config.get("configfile", "seed"))
# get filas
queueArray = eval(config.get("configfile", "queueList"))
queueObjects = []

for queue in queueArray:
    queue[5].sort(key=lambda x: x[1])
    simQueue = Queue(queue[0], queue[1], queue[2],
                     queue[3], queue[4], queue[5])
    queueObjects.append(simQueue)


# instanciacao e start da simulacao
simulator = queueSimulator(
    firstArrivalTime, quantityRandomNumbers, seed, queueObjects)
simulator.simulate()

for queue in simulator.queueList:
    print(f'Queue: {queue.name}')
    limiter = 0
    for index in range(len(queue.accumulatedTimes)):
        if limiter < 30:
            print(f'State: {index}, Time: {queue.accumulatedTimes[index]}, Probability: {
                  round((queue.accumulatedTimes[index]/simulator.time)*100, 4)}%')
        else:
            break
        limiter += 1
    print(f'Losses: {queue.losses}')
print(f'Simulation time: {simulator.time}')
input()

# from queueSimulator import queueSimulator
# from queueClass import Queue

# q1 = Queue('q1', 1, 5, 2, 5, 3, 5)
# q2 = Queue('q2', 2, 5, 2, 5, 3, 5)

# simulator1 = queueSimulator(100000, 12345, 2, q1)
# simulator2 = queueSimulator(100000, 12345, 2, q2)

# print("Simulation 1: G/G/1/5")
# simulator1.simulate()
# print("Simulation 2: G/G/2/5")
# simulator2.simulate()
