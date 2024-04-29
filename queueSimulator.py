import heapq
from random_generator import PseudoRandomNumberGenerator


class queueSimulator:
    def __init__(self, quantityRandomNumbers, seed, firstArrivalTime, queue):
        self.prng = PseudoRandomNumberGenerator(quantityRandomNumbers, seed)
        self.quantityRandomNumbers = quantityRandomNumbers
        self.firstArrivalTime = firstArrivalTime
        self.queue = queue
        self.schedule = []
        self.eventHeap = []
        self.currentClient = 0
        self.times = 0

    def timeGenerator(self, min, max):
        randomNumber = self.prng.generate()
        return min + ((max - min) * randomNumber)

    def accumulateTime(self, eventTime):
        scheduleState = len(self.schedule)
        self.queue.accumulatedTimes[scheduleState] += (
            eventTime - self.times)
        self.times = eventTime

    def processArrival(self, eventTime):
        if len(self.schedule) < self.queue.capacity:
            self.schedule.append(self.currentClient)
            if len(self.schedule) <= self.queue.servers:
                departureTime = eventTime + \
                    self.timeGenerator(self.queue.minService,
                                       self.queue.maxService)
                heapq.heappush(self.eventHeap, (departureTime,
                               'departure', self.currentClient))
        else:
            self.queue.losses += 1
        self.currentClient += 1
        nextArrivalTime = eventTime + \
            self.timeGenerator(self.queue.minArrival, self.queue.maxArrival)
        heapq.heappush(self.eventHeap, (nextArrivalTime,
                       'arrival', self.currentClient))

    def processDeparture(self, eventTime):
        self.schedule.pop(0)
        if self.schedule and len(self.schedule) >= self.queue.servers:
            nextClient = self.schedule[self.queue.servers - 1]
            nextDepartureTime = eventTime + \
                self.timeGenerator(self.queue.minService,
                                   self.queue.maxService)
            heapq.heappush(self.eventHeap, (nextDepartureTime,
                           'departure', nextClient))

    def simulate(self):
        heapq.heappush(self.eventHeap, (self.firstArrivalTime,
                       'arrival', self.currentClient))

        while self.quantityRandomNumbers > 0 and self.eventHeap:

            eventTime, eventType, currentClient = heapq.heappop(self.eventHeap)

            self.accumulateTime(eventTime)

            if eventType == 'arrival':
                self.processArrival(eventTime)
            elif eventType == 'departure':
                self.processDeparture(eventTime)

            self.quantityRandomNumbers -= 1

        print("Simulation Results:")
        for i in range(self.queue.capacity + 1):
            probability = self.queue.accumulatedTimes[i] / self.times * 100
            print(f"State {i}: Accumulated time {
                self.queue.accumulatedTimes[i]:.4f}, Probability {probability:.2f}%")

        print(f"Lost customers: {self.queue.losses}")
        print(f"Total simulation time: {self.times:.4f}\n")
