import heapq
from random_generator import PseudoRandomNumberGenerator


class queueSimulator:
    def __init__(self, quantityRandomNumbers, seed, minArrival, maxArrival, minService, maxService, queueServers, queueCapacity, initialTime):
        self.prng = PseudoRandomNumberGenerator(quantityRandomNumbers, seed)
        self.quantityRandomNumbers = quantityRandomNumbers
        self.initialEventTime = initialTime
        self.queue = []
        self.eventHeap = []
        self.accumulatedTimes = [0] * (queueCapacity + 1)
        self.queueCapacity = queueCapacity
        self.queueServers = queueServers
        self.minArrival = minArrival
        self.maxArrival = maxArrival
        self.minService = minService
        self.maxService = maxService
        self.losses = 0
        self.currentClient = 0
        self.lastTimeEvent = 0

    def timeGenerator(self, min, max):
        randomNumber = self.prng.generate()
        return min + ((max - min) * randomNumber)

    def accumulateTime(self, eventTime):
        queueState = len(self.queue)
        self.accumulatedTimes[queueState] += (eventTime - self.lastTimeEvent)
        self.lastTimeEvent = eventTime

    def processArrival(self, eventTime):
        if len(self.queue) < self.queueCapacity:
            self.queue.append(self.currentClient)
            if len(self.queue) <= self.queueServers:
                departureTime = eventTime + \
                    self.timeGenerator(self.minService,
                                       self.maxService)
                heapq.heappush(self.eventHeap, (departureTime,
                               'departure', self.currentClient))
        else:
            self.losses += 1
        self.currentClient += 1
        nextArrivalTime = eventTime + \
            self.timeGenerator(self.minArrival, self.maxArrival)
        heapq.heappush(self.eventHeap, (nextArrivalTime,
                       'arrival', self.currentClient))

    def processDeparture(self, eventTime, clientId):
        self.queue.pop(0)
        if self.queue and len(self.queue) >= self.queueServers:
            nextClient = self.queue[self.queueServers - 1]
            nextDepartureTime = eventTime + \
                self.timeGenerator(self.minService, self.maxService)
            heapq.heappush(self.eventHeap, (nextDepartureTime,
                           'departure', nextClient))

    def simulate(self):
        heapq.heappush(self.eventHeap, (self.initialEventTime,
                       'arrival', self.currentClient))

        while self.quantityRandomNumbers > 0 and self.eventHeap:

            eventTime, eventType, currentClient = heapq.heappop(self.eventHeap)

            self.accumulateTime(eventTime)

            if eventType == 'arrival':
                self.processArrival(eventTime)
            elif eventType == 'departure':
                self.processDeparture(eventTime, currentClient)

            self.quantityRandomNumbers -= 1

        print("Simulation Results:")
        for i in range(self.queueCapacity + 1):
            probability = self.accumulatedTimes[i] / self.lastTimeEvent * 100
            print(f"State {i}: Accumulated time {
                self.accumulatedTimes[i]:.4f}, Probability {probability:.2f}%")

        print(f"Lost customers: {self.losses}")
        print(f"Total simulation time: {self.lastTimeEvent:.4f}\n")
