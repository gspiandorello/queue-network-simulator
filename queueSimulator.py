from randomGenerator import PseudoRandomNumberGenerator


class queueSimulator:
    def __init__(self, quantityRandomNumbers, seed, firstArrivalTime, queueList):
        self.randomNumbers = PseudoRandomNumberGenerator(
            quantityRandomNumbers, seed).generate()
        self.quantityRandomNumbers = quantityRandomNumbers
        self.firstArrivalTime = firstArrivalTime
        self.times = 0
        self.usedRandomNumbers = 0
        self.queueList = queueList
        # self.losses = 0
        self.scheduler = []
        # self.events = []

    def timeGenerator(self, min, max):
        randomNumber = min + \
            ((max - min) * self.randomNumbers[self.usedRandomNumbers])
        self.usedRandomNumbers += 1
        return randomNumber

    # atualizar função, caso eu decida usar ela
    def accumulateTime(self, eventTime):
        scheduleState = len(self.scheduler)
        # atualizar o tempo em todas as filas
        self.queue.accumulatedTimes[scheduleState] += (
            eventTime - self.times)
        self.times = eventTime

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
            # self.losses += 1
            queue.losses += 1
        # verificar se é necessário passar a queue2
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
            # self.losses += 1
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
            queue2 = ''
            for queue in self.queueList:
                if queue.name == destination:
                    queue2 = queue
                self.eventSchedule('passage', queue, queue2)

    def chooseDestination(self, queue, probability):
        aux = 0
        # verificar o nome destination baseado de como eu vou ler os dados do arquivo
        for destination in queue.network:
            aux += destination[1]
            if probability <= aux:
                # print(destination[0])
                return destination[0]
        return 'departure'

    def eventSchedule(self, eventType, queue1, queue2=None):
        if self.usedRandomNumbers >= self.quantityRandomNumbers:
            print("No more random numbers available")
            return
        if eventType == 'arrival':
            # verificar se é necessário colocar o round
            eventTime = self.timeGenerator(
                queue1.minArrival, queue1.maxArrival) + self.times
            event = {'eventType': 'arrival',
                     'eventTime': eventTime, 'queue': queue1}
        # verificar se pode ser elif ao invés de if
        elif eventType == 'passage' and queue2 is not None:
            eventTime = self.timeGenerator(
                queue1.minService, queue1.maxService) + self.times
            event = {'eventType': 'passage',
                     'eventTime': eventTime, 'queue1': queue1, 'queue2': queue2}
        elif eventType == 'departure':
            eventTime = self.timeGenerator(
                queue1.minService, queue1.maxService) + self.times
            event = {'eventType': 'departure',
                     'eventTime': eventTime, 'queue': queue1}

        self.scheduler.append(event)

        self.scheduler.sort(key=lambda x: float(x['eventTime']))
        # self.scheduler = sorted(
        #     self.scheduler, key=lambda x: float(x['eventTime']))

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

            if event.get('eventType') == 'passage':
                # verificar se é necessário fazer isso
                print(f'eventType: {event.get('eventType')}, eventTime: {event.get('eventTime')}, queue1: {event.get('queue1').name}, queue2: {
                      event.get('queue2').name}, {event.get('queue1').clients}, {event.get('queue2').clients}', end='\n\n')
            else:
                # verificar se é necessário fazer isso
                print(f'eventType: {event.get('eventType')}, eventTime: {event.get('eventTime')}, queue: {
                      event.get('queue').name}, {event.get('queue').clients}', end='\n\n')

            for queue in self.queueList:
                queue.accumulatedTimes[queue.clients] += (
                    event.get('eventTime') - self.times)

            self.times = event.get('eventTime')
            if event.get('eventType') == 'arrival':
                self.processArrival(event.get('queue'))
            elif event.get('eventType') == 'passage':
                self.processPassage(
                    event.get('queue1'), event.get('queue2'))
            elif event.get('eventType') == 'departure':
                self.processDeparture(event.get('queue'))

        print("Simulation Results:")
        for i in range(self.queue.capacity + 1):
            probability = self.queue.accumulatedTimes[i] / self.times * 100
            print(f"State {i}: Accumulated time {
                self.queue.accumulatedTimes[i]:.4f}, Probability {probability:.2f}%")

        print(f"Lost customers: {self.queue.losses}")
        print(f"Total simulation time: {self.times:.4f}\n")
