from randomGenerator import PseudoRandomNumberGenerator


class queueSimulator:
    def __init__(self, firstArrivalTime, quantityRandomNumbers, seed, queueList):
        self.firstArrivalTime = firstArrivalTime
        self.randomNumbers = PseudoRandomNumberGenerator(
            quantityRandomNumbers, seed).generate()
        self.quantityRandomNumbers = quantityRandomNumbers
        self.times = 0
        self.usedRandomNumbers = 0
        self.queueList = queueList
        self.scheduler = []

    def timeGenerator(self, min, max):
        randomNumber = min + \
            ((max - min) * self.randomNumbers[self.usedRandomNumbers])
        self.usedRandomNumbers += 1
        return randomNumber

    def accumulateTime(self, event):
        for queue in self.queueList:
            queue.accumulatedTimes[queue.clients] += (
                event.get('eventTime') - self.times)

    def processArrival(self, queue):
        # self.accumulateTime(eventTime)
        if queue.clients < queue.capacity:
            queue.clients += 1
            if queue.clients <= queue.servers:
                if self.usedRandomNumbers >= self.quantityRandomNumbers:
                    print("No more random numbers available")
                    return
                self.destinationSchedule(queue, self.chooseDestination(
                    queue, self.timeGenerator(0, 1)))
        else:
            queue.losses += 1
        self.eventSchedule('arrival', queue)

    def processPassage(self, queue1, queue2):
        queue1.clients -= 1
        if queue1.clients >= queue1.servers:
            if self.usedRandomNumbers >= self.quantityRandomNumbers:
                print("No more random numbers available")
                return
            self.destinationSchedule(queue1, self.chooseDestination(
                queue1, self.timeGenerator(0, 1)))
        if queue2.clients < queue2.capacity:
            queue2.clients += 1
            if queue2.clients <= queue2.servers:
                if self.usedRandomNumbers >= self.quantityRandomNumbers:
                    print("No more random numbers available")
                    return
                self.destinationSchedule(queue2, self.chooseDestination(
                    queue2, self.timeGenerator(0, 1)))
        else:
            queue2.losses += 1

    def processDeparture(self, queue):
        queue.clients -= 1
        if queue.clients >= queue.servers:
            if self.usedRandomNumbers >= self.quantityRandomNumbers:
                print("No more random numbers available")
                return
            self.destinationSchedule(queue, self.chooseDestination(
                queue, self.timeGenerator(0, 1)))

    def destinationSchedule(self, queue, destination):
        if destination == 'departure':
            self.eventSchedule('departure', queue)
        else:
            queue2 = None
            for q in self.queueList:
                if q.name == destination:
                    queue2 = q
                    break
            if (queue2):
                self.eventSchedule('passage', queue, queue2)

    def chooseDestination(self, queue, probability):
        aux = 0
        for destination in queue.network:
            aux += destination[1]
            if probability <= aux:
                return destination[0]
        return 'departure'

    def eventSchedule(self, eventType, queue1, queue2=None):
        if self.usedRandomNumbers >= self.quantityRandomNumbers:
            print("No more random numbers available")
            return
        if eventType == 'arrival':
            eventTime = self.timeGenerator(
                queue1.minArrival, queue1.maxArrival) + self.times
            event = {'eventType': eventType,
                     'eventTime': eventTime, 'queue': queue1}
        elif eventType == 'passage' and queue2 is not None:
            eventTime = self.timeGenerator(
                queue1.minService, queue1.maxService) + self.times
            event = {'eventType': eventType,
                     'eventTime': eventTime, 'queue1': queue1, 'queue2': queue2}
        elif eventType == 'departure':
            eventTime = self.timeGenerator(
                queue1.minService, queue1.maxService) + self.times
            event = {'eventType': eventType,
                     'eventTime': eventTime, 'queue': queue1}

        self.scheduler.append(event)

        self.scheduler.sort(key=lambda x: float(x['eventTime']))

    def simulate(self):
        for queue in self.queueList:
            for time in self.firstArrivalTime:
                if time[0] == queue.name:
                    firstSchedule = {'eventType': 'arrival',
                                     'eventTime': time[1], 'queue': queue}
                    self.scheduler.append(firstSchedule)
        self.scheduler.sort(key=lambda x: float(x['eventTime']))

        while self.usedRandomNumbers < self.quantityRandomNumbers:
            event = self.scheduler.pop(0)

            # debbug mode
            # if event.get('eventType') == 'passage':
            #     print(f'eventType: {event.get('eventType')}, eventTime: {event.get('eventTime')}, queue1: {event.get('queue1').name}, queue2: {
            #           event.get('queue2').name}, {event.get('queue1').clients}, {event.get('queue2').clients}', end='\n\n')
            # else:
            #     print(f'eventType: {event.get('eventType')}, eventTime: {event.get('eventTime')}, queue: {
            #           event.get('queue').name}, {event.get('queue').clients}', end='\n\n')

            self.accumulateTime(event)

            self.times = event.get('eventTime')
            if event.get('eventType') == 'arrival':
                self.processArrival(event.get('queue'))
            elif event.get('eventType') == 'passage':
                self.processPassage(
                    event.get('queue1'), event.get('queue2'))
            elif event.get('eventType') == 'departure':
                self.processDeparture(event.get('queue'))

        self.printResults()

    def printResults(self):
        for queue in self.queueList:
            print(f'\n*****************************************************************')
            print(f'Queue: {
                queue.name} (G/G/{queue.servers}/{queue.capacity if queue.capacity != 999999 else ''})')
            if queue.minArrival != -1 and queue.maxArrival != -1:
                print(f'Arrival: {queue.minArrival}...{queue.maxArrival}')
            print(f'Service: {queue.minService}...{queue.maxService}')
            print(f'*****************************************************************')
            for index in range(len(queue.accumulatedTimes)):
                if queue.accumulatedTimes[index] > 0:
                    print(f'State: {index}, Time: {round(queue.accumulatedTimes[index], 4)}, Probability: {
                        round((queue.accumulatedTimes[index]/self.times)*100, 4)}%')
            print(f'\nNumber of losses: {queue.losses}')

        print(f'\n=================================================================')
        print(f'Simulation average time: {round(self.times, 4)}')
        print(f'=================================================================')
