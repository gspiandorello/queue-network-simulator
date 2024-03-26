import heapq

# Inicialização de parâmetros do gerador de números pseudoaleatórios
a = 1664525
c = 1013904223
M = 2**32
seed = 12345

def NextRandom():
    global seed
    seed = (a * seed + c) % M
    return seed / M

# Função para simular a fila
def simular_fila(intervalo_chegada_min, intervalo_chegada_max, intervalo_atendimento_min, intervalo_atendimento_max, num_servidores, capacidade_fila, tempo_primeira_chegada):
    # Funções auxiliares para gerar tempos de chegada e atendimento com base nos parâmetros
    def gerar_tempo_chegada():
        return intervalo_chegada_min + ((intervalo_chegada_max - intervalo_chegada_min) * NextRandom())

    def gerar_tempo_atendimento():
        return intervalo_atendimento_min + ((intervalo_atendimento_max - intervalo_atendimento_min) * NextRandom())

    # Estado inicial da simulação
    fila = []
    heap_eventos = []
    tempos_acumulados = [0] * (capacidade_fila + 1)
    perda_clientes = 0
    cliente_atual = 0
    tempo_ultimo_evento = 0

    # Adiciona primeiro evento de chegada
    heapq.heappush(heap_eventos, (tempo_primeira_chegada, 0, cliente_atual))  # 0 é o tipo de evento de chegada

    # Main simulation loop
    count = 100000
    while count > 0 and heap_eventos:
        tempo_evento, tipo_evento, cliente_id = heapq.heappop(heap_eventos)
        if tipo_evento == 0:  # Chegada
            if len(fila) < capacidade_fila:
                fila.append(cliente_atual)
                if len(fila) <= num_servidores:
                    tempo_saida = tempo_evento + gerar_tempo_atendimento()
                    heapq.heappush(heap_eventos, (tempo_saida, 1, cliente_atual))  # 1 é o tipo de evento de saída
            else:
                perda_clientes += 1
            cliente_atual += 1
            tempo_proxima_chegada = tempo_evento + gerar_tempo_chegada()
            heapq.heappush(heap_eventos, (tempo_proxima_chegada, 0, cliente_atual))
        elif tipo_evento == 1:  # Saída
            fila.pop(0)
            if fila and len(fila) >= num_servidores:
                proximo_cliente = fila[num_servidores - 1]
                tempo_proxima_saida = tempo_evento + gerar_tempo_atendimento()
                heapq.heappush(heap_eventos, (tempo_proxima_saida, 1, proximo_cliente))

        estado_fila = len(fila)
        tempos_acumulados[estado_fila] += (tempo_evento - tempo_ultimo_evento)
        tempo_ultimo_evento = tempo_evento
        count -= 1

    # Cálculo e exibição dos resultados
    print("Resultados da Simulação:")
    for i in range(capacidade_fila + 1):
        probabilidade = tempos_acumulados[i] / tempo_ultimo_evento * 100
        print(f"Estado {i}: Tempo acumulado {tempos_acumulados[i]:.2f}, Probabilidade {probabilidade:.2f}%")

    print(f"Perda de clientes: {perda_clientes}")
    print(f"Tempo global de simulação: {tempo_ultimo_evento:.2f}\n")

# Simulando as filas
print("Simulação 1: G/G/1/5")
simular_fila(2, 5, 3, 5, 1, 5, 2)
print("Simulação 2: G/G/2/5")
simular_fila(2, 5, 3, 5, 2, 5, 2)
