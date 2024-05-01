from queueSimulator import queueSimulator
from queueClass import Queue
import configparser

inf = 999999

config = configparser.ConfigParser()
config.read("config.ini")
firstArrivalTime = eval(config.get("configfile", "firstArrivalTime"))
quantityRandomNumbers = int(config.get("configfile", "quantityRandomNumbers"))
seed = int(config.get("configfile", "seed"))
# get filas
queueList = eval(config.get("configfile", "queueList"))
queueListObj = []

for queue in queueList:
    network = queue[7]
    network.sort(key=lambda x: x[1])
    eachQueue = Queue(queue[0], queue[1], queue[2],
                      queue[3], queue[4], queue[5], queue[6], network)
    queueListObj.append(eachQueue)

simulator = queueSimulator(
    firstArrivalTime, quantityRandomNumbers, seed, queueListObj)
simulator.simulate()

for queue in simulator.queueList:
    print(f'Queue: {queue.name}')
    limiter = 0
    for index in range(len(queue.accumulatedTimes)):
        if limiter < 30:
            print(f'State: {index}, Time: {queue.accumulatedTimes[index]}, Probability: {
                  round((queue.accumulatedTimes[index]/simulator.times)*100, 4)}%')
        else:
            break
        limiter += 1
    print(f'Losses: {queue.losses}')
print(f'queueSimulator time: {simulator.times}')
input()
