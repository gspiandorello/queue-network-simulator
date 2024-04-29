class Queue:

    # , network):
    def __init__(self, name, servers, capacity, minArrival, maxArrival, minService, maxService):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.minArrival = minArrival
        self.maxArrival = maxArrival
        self.minService = minService
        self.maxService = maxService
        # self.network = network
        self.clients = 0
        self.losses = 0
        self.accumulatedTimes = [0] * (self.capacity + 1)
