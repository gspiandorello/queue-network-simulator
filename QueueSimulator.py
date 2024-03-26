import heapq

# Initialization of pseudo-random number generator parameters
a = 1664525
c = 1013904223
M = 2**32
seed = 12345

def NextRandom():
    global seed
    seed = (a * seed + c) % M
    return seed / M

# Function to simulate the queue
def simulate_queue(arrival_interval_min, arrival_interval_max, service_interval_min, service_interval_max, num_servers, queue_capacity, first_arrival_time):
    # Helper functions to generate arrival and service times based on parameters
    def generate_arrival_time():
        return arrival_interval_min + ((arrival_interval_max - arrival_interval_min) * NextRandom())

    def generate_service_time():
        return service_interval_min + ((service_interval_max - service_interval_min) * NextRandom())

    # Initial state of the simulation
    queue = []
    event_heap = []
    accumulated_times = [0] * (queue_capacity + 1)
    lost_customers = 0
    current_customer = 0
    last_event_time = 0

    # Add first arrival event
    heapq.heappush(event_heap, (first_arrival_time, 0, current_customer))  # 0 is the type of arrival event

    # Main simulation loop
    count = 100000
    while count > 0 and event_heap:
        event_time, event_type, customer_id = heapq.heappop(event_heap)
        if event_type == 0:  # Arrival
            if len(queue) < queue_capacity:
                queue.append(current_customer)
                if len(queue) <= num_servers:
                    departure_time = event_time + generate_service_time()
                    heapq.heappush(event_heap, (departure_time, 1, current_customer))  # 1 is the type of departure event
            else:
                lost_customers += 1
            current_customer += 1
            next_arrival_time = event_time + generate_arrival_time()
            heapq.heappush(event_heap, (next_arrival_time, 0, current_customer))
        elif event_type == 1:  # Departure
            queue.pop(0)
            if queue and len(queue) >= num_servers:
                next_customer = queue[num_servers - 1]
                next_departure_time = event_time + generate_service_time()
                heapq.heappush(event_heap, (next_departure_time, 1, next_customer))

        queue_state = len(queue)
        accumulated_times[queue_state] += (event_time - last_event_time)
        last_event_time = event_time
        count -= 1

    # Calculating and displaying results
    print("Simulation Results:")
    for i in range(queue_capacity + 1):
        probability = accumulated_times[i] / last_event_time * 100
        print(f"State {i}: Accumulated time {accumulated_times[i]:.2f}, Probability {probability:.2f}%")

    print(f"Lost customers: {lost_customers}")
    print(f"Total simulation time: {last_event_time:.2f}\n")

# Simulating the queues
print("Simulation 1: G/G/1/5")
simulate_queue(2, 5, 3, 5, 1, 5, 2)
print("Simulation 2: G/G/2/5")
simulate_queue(2, 5, 3, 5, 2, 5, 2)
