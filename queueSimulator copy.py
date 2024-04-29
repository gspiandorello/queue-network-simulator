import heapq
from random_generator import PseudoRandomNumberGenerator


class queueSimulator:
    def __init__(self, initialTime, quantityRandomNumbers, seed, queue):
        self.times = float(0)
        self.initialEventTime = float(initialTime)
        self.randomNumbers = PseudoRandomNumberGenerator(
            quantityRandomNumbers, seed).generate()
        self.usedrandomNumbers = 0
        self.quantityRandomNumbers = quantityRandomNumbers
        # self.queuesList = queuesList
        self.queue = queue
        self.losses = 0
        # self.scheduler = []
        # self.events = []
        self.eventHeap = []
        self.clientId = 0
        self.activeClients = []

    def timeGenerator(self, min, max):
        timeGenerated = min + \
            ((max - min) * self.randomNumbers[self.usedrandomNumbers])
        self.usedrandomNumbers += 1
        return float(timeGenerated)

    def accumulateTime(self, eventTime):
        self.queue.timeAtService[self.queue.clients] += eventTime - self.times
        self.times = eventTime

    def processArrival(self, eventTime):
        self.accumulateTime(eventTime)
        if self.queue.clients < self.queue.capacity:
            self.queue.clients += 1
            if self.queue.clients <= self.queue.servers:
                departureTime = eventTime + \
                    self.timeGenerator(self.queue.minService,
                                       self.queue.maxService)
                heapq.heappush(self.eventHeap, (departureTime,
                               'departure', self.clientId))
                # Adiciona o cliente à lista de ativos
                self.activeClients.append(self.clientId)
        else:
            self.queue.losses += 1
        self.clientId += 1
        nextArrivalTime = eventTime + \
            self.timeGenerator(self.queue.minArrival, self.queue.maxArrival)
        heapq.heappush(self.eventHeap, (nextArrivalTime,
                       'arrival', self.clientId))

    def processDeparture(self, eventTime, clientId):
        self.accumulateTime(eventTime)
        self.queue.clients -= 1
        self.activeClients.remove(clientId)
        if self.queue.clients >= self.queue.servers:
            if self.usedrandomNumbers >= self.quantityRandomNumbers:
                return
            if self.activeClients:
                nextClientId = self.activeClients[0]
                nextDepartureTime = eventTime + \
                    self.timeGenerator(self.queue.minService,
                                       self.queue.maxService)
                heapq.heappush(
                    self.eventHeap, (nextDepartureTime, 'departure', nextClientId))

    def simulate(self):
        heapq.heappush(self.eventHeap, (self.initialEventTime,
                       'arrival', self.clientId))

        while self.quantityRandomNumbers > 0:

            eventTime, eventType, currentClient = heapq.heappop(self.eventHeap)

            if eventType == 'arrival':
                self.processArrival(eventTime)
            elif eventType == 'departure':
                self.processDeparture(eventTime, currentClient)

            self.quantityRandomNumbers -= 1

        print("Simulation Results:")
        for i in range(self.queue.capacity + 1):
            probability = self.queue.timeAtService[i] / self.times * 100
            print(f"State {i}: Accumulated time {
                self.queue.timeAtService[i]:.4f}, Probability {probability:.2f}%")

        print(f"Lost customers: {self.queue.losses}")
        print(f"Total simulation time: {self.times:.4f}\n")
