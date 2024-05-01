from queueSimulator import queueSimulator
from queueClass import Queue
from yamlConfig import readYamlFile, validateYamlFile


yamlData = readYamlFile("config.yaml")
validateYamlFile(yamlData['configfile'])

firstArrivalTime = yamlData['configfile']['firstArrivalTime']
quantityRandomNumbers = yamlData['configfile']['quantityRandomNumbers']
seed = yamlData['configfile']['seed']
queueList = yamlData['configfile']['queueList']

maxCapacity = 999999
queueListObj = []

for queue in queueList:
    network = queue.get('network', [])
    network.sort(key=lambda x: x['probability'])
    eachQueue = Queue(queue['name'], queue['servers'], queue.get('capacity', maxCapacity),
                      queue.get('minArrival', -1), queue.get('maxArrival', -1),
                      queue['minService'], queue['maxService'], network)
    queueListObj.append(eachQueue)

simulator = queueSimulator(
    firstArrivalTime, quantityRandomNumbers, seed, queueListObj)
simulator.simulate()
