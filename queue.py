class Queue:
    def __init__(self, servers, capacity, min_arrival, max_arrival, min_service, max_service):
        self.servers = servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service
        self.customers = 0
        self.loss = 0
        self.times = [0] * (self.capacity + 1)

    def status(self):
        return self.customers

    def get_capacity(self):
        return self.capacity

    def get_servers(self):
        return self.servers

    def increment_loss(self):
        self.loss += 1

    def check_in(self):
        if self.customers < self.capacity:
            self.customers += 1
            return True
        else:
            self.increment_loss()
            return False

    def check_out(self):
        if self.customers > 0:
            self.customers -= 1

    def generate_arrival_time(self):
        return self.min_arrival + ((self.max_arrival - self.min_arrival) * NextRandom())

    def generate_service_time(self):
        return self.min_service + ((self.max_service - self.min_service) * NextRandom())

    def update_times(self, time_spent, current_time):
        if self.customers <= self.capacity:
            self.times[self.customers] += time_spent
        else:
            # If over capacity, accumulate at last index
            self.times[-1] += time_spent
        return current_time
