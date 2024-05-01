# Queue Network Simulator

## Overview
The Queue Network Simulator is a powerful tool designed to simulate various network topologies, with a particular focus on queue networks featuring variable routing. This simulator facilitates the modeling of complex systems such as computer networks and advanced logistical systems, making it an essential tool for research and educational purposes in network analysis and operations management.

## Features
- Simulation of diverse queue network topologies.
- Variable routing based on probabilistic models.
- Detailed tracking of system states and queue statistics.
- Loss statistics to analyze queue capacity limitations.
- Configuration through YAML files for flexible simulation setups.

## How It Works
The simulator initializes with a set of parameters defined in a YAML configuration file, which includes the number of servers, queue capacities, arrival and service times, and routing probabilities between queues. The simulation progresses through events such as arrivals, services, and transitions between queues, based on generated pseudo-random numbers and the defined network structure.

## Usage
To use the simulator, define your network configuration in a YAML file according to the example provided. Ensure all dependencies are installed, and run the simulation script via a Python environment.

## Example:
```yaml
configfile:
  firstArrivalTime: [["Q1", 2.0]]
  quantityRandomNumbers: 100000
  seed: 12345
  queueList:
    - name: "Q1"
      servers: 1
      minArrival: 2.0
      maxArrival: 4.0
      minService: 1.0
      maxService: 2.0
      network:
        - target: "Q2"
          probability: 0.8
        - target: "Q3"
          probability: 0.2
    - name: "Q2"
      servers: 2
      capacity: 5
      minService: 4.0
      maxService: 8.0
      network:
        - target: "Q1"
          probability: 0.3
        - target: "Q2"
          probability: 0.5
    - name: "Q3"
      servers: 2
      capacity: 10
      minService: 5.0
      maxService: 15.0
      network:
        - target: "Q3"
          probability: 0.7

```

## Results
The simulator outputs detailed logs of queue states throughout the simulation, providing insights into the dynamics of each queue. It includes statistics on queue utilization, service times, and loss rates due to capacity constraints.

## Conclusion
This simulator is an invaluable resource for anyone looking to understand or teach the dynamics of complex queuing networks and their applications in various fields such as telecommunications, computer networking, and transportation logistics.
