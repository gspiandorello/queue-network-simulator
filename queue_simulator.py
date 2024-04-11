import heapq
from queue_class import Queue
from event import Event

# Pseudo-função para acumulação de tempo para ambas as filas
def AccumulatesTime(queue1, queue2, last_event_time, current_time):
    time_spent = current_time - last_event_time
    queue1.update_times(time_spent, current_time)
    queue2.update_times(time_spent, current_time)


# Funções process_* atualizadas para lidar com ambas as filas
def process_arrival(ev, queue1, queue2, event_heap, last_event_time):
    AccumulatesTime(queue1, queue2, last_event_time, ev.time)
    if queue1.check_in():
        if queue1.status() <= queue1.get_servers():
            next_departure_time = ev.time + queue1.generate_service_time()
            heapq.heappush(event_heap, Event(next_departure_time, 'passage', ev.customer_id))
    else:
        queue1.increment_loss()
    # Agendar próximo evento de chegada
    next_arrival_time = ev.time + queue1.generate_arrival_time()
    heapq.heappush(event_heap, Event(next_arrival_time, 'arrival', ev.customer_id + 1))

def process_departure(ev, queue1, queue2, event_heap, last_event_time):
    AccumulatesTime(queue1, queue2, last_event_time, ev.time)
    queue2.check_out()

    # Se ainda houver clientes na fila e eles estiverem sendo atendidos, agende a próxima saída.
    if queue2.status() >= queue2.get_servers():
        next_departure_time = ev.time + queue2.generate_service_time()
        heapq.heappush(event_heap, Event(next_departure_time, 'departure', ev.customer_id))


def process_passage(ev, queue1, queue2, event_heap, last_event_time):
    AccumulatesTime(queue1, queue2, last_event_time, ev.time)
    queue1.check_out()

    # Se há clientes suficientes em Fila1 para preencher todos os servidores, agende um novo evento de passagem.
    if queue1.status() >= queue1.get_servers():
        next_passage_time = ev.time + queue1.generate_service_time()
        heapq.heappush(event_heap, Event(next_passage_time, 'passage', ev.customer_id))

    if queue2.status() < queue2.get_capacity():
        queue2.check_in()
        # Se há servidores disponíveis para o novo cliente em Fila2, agende um evento de saída.
        if queue2.status() <= queue2.get_servers():
            next_departure_time = ev.time + queue2.generate_service_time()
            heapq.heappush(event_heap, Event(next_departure_time, 'departure', ev.customer_id))
    else:
        # O cliente é perdido se Fila2 estiver cheia.
        queue2.increment_loss()


# Função simulate_queue atualizada para tratar as duas filas
def simulate_queue(queue1, queue2, first_arrival_time, count=100000):
    event_heap = []
    last_event_time = 0
    
    # Coloca o primeiro evento de chegada na heap
    heapq.heappush(event_heap, Event(first_arrival_time, 'arrival', 0))

    while count > 0 and event_heap:
        ev = heapq.heappop(event_heap)
        
        # Atualiza o acumulador de tempo nas duas filas
        AccumulatesTime(queue1, queue2, last_event_time, ev.time)
        
        if ev.event_type == 'arrival':
            process_arrival(ev, queue1, queue2, event_heap, last_event_time)
        elif ev.event_type == 'departure':
            process_departure(ev, queue1, queue2, event_heap, last_event_time)
        elif ev.event_type == 'passage':
            process_passage(ev, queue1, queue2, event_heap, last_event_time)

        last_event_time = ev.time
        count -= 1

    # Apresenta os resultados para ambas as filas
    print("Resultados da Simulação:")
    print("\nQueue 1:")
    queue1.display_results()
    print("\nQueue 2:")
    queue2.display_results()
    global_time = last_event_time  # último tempo de evento processado
    print(f"\nTempo global da simulação: {global_time}")

# Parâmetros de acordo com a especificação da simulação
QUEUE1_PARAMS = {
    'servers': 2,
    'capacity': 3,
    'min_arrival': 1,
    'max_arrival': 4,
    'min_service': 3,
    'max_service': 4
}

QUEUE2_PARAMS = {
    'servers': 1,
    'capacity': 5,
    'min_arrival': 0,  # Fila 2 não tem chegadas externas
    'max_arrival': 0,
    'min_service': 2,
    'max_service': 3
}

queue1 = Queue(**QUEUE1_PARAMS)
queue2 = Queue(**QUEUE2_PARAMS)
simulate_queue(queue1, queue2, first_arrival_time=1.5)
