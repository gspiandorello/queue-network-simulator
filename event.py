class Event:
    def __init__(self, time, event_type, customer_id):
        self.time = time
        self.event_type = event_type
        self.customer_id = customer_id

    def __lt__(self, other):
        return self.time < other.time