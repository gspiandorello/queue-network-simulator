# Queue Simulation Project

## Overview
This Queue Simulation project is designed to model and analyze the behavior of queues under various configurations. By simulating the dynamics of queues with different parameters, this project helps in understanding the impact of various factors on queue performance, including customer wait times, service efficiency, and overall system throughput.

## Features
Customizable Simulation Parameters: Users can specify key parameters of the simulation, such as the arrival and service time distributions, queue capacity, and the number of servers.
Pseudo-Random Number Generation: Utilizes a linear congruential generator (LCG) for pseudo-random number generation, ensuring consistent and reproducible simulation outcomes.
Event-Driven Simulation: The simulation is driven by two main types of events - customer arrivals and service completions, managed through a priority queue to maintain chronological order.
Performance Metrics: The simulation tracks and reports various metrics, including the distribution of queue lengths over time and the number of customers lost due to queue capacity limits.

## How It Works
The simulation starts by initializing the system state and parameters, including the pseudo-random number generator and event priority queue (heapq). Customers arrive at the system according to a specified inter-arrival time distribution, and are serviced by a designated number of servers based on a specified service time distribution. The system capacity can be set to limit the number of customers in the queue. The simulation processes arrival and departure events in a loop, updating the system state and accumulating statistics until a predefined number of events have been processed or a specified simulation time has been reached.

## Usage
To run a simulation, users can call the simular_fila function with the desired parameters:

* intervalo_chegada_min and intervalo_chegada_max: Minimum and maximum inter-arrival times.
* intervalo_atendimento_min and intervalo_atendimento_max: Minimum and maximum service times.
* num_servidores: Number of servers in the system.
* capacidade_fila: Maximum queue capacity (number of customers).
* tempo_primeira_chegada: Time of the first customer arrival.

## Example:
```simular_fila(2, 5, 3, 5, 1, 5, 2)  # Simulate a G/G/1/5 queue system```

## Results
After running a simulation, the system will output the accumulated times for different queue states, the probability distribution of these states, the number of customers lost, and the total simulation time. These results provide insights into the efficiency and effectiveness of the queue system under the specified parameters.

## Conclusion
This Queue Simulation project offers a flexible tool for modeling and analyzing queue systems. It is particularly useful for students, researchers, and professionals interested in operations research, queue theory, and system optimization.
