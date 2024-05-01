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
Below are sample results from a simulation run using the provided YAML configuration. The results demonstrate the detailed statistics for each queue, including the states, time in each state, probability of the queue being in a given state, and the number of losses due to capacity limitations.

### Queue Q1 (G/G/1)
- **Arrival Rates**: 2.0 to 4.0
- **Service Rates**: 1.0 to 2.0
- **States**:
  - State 0: Time 15420.3816, Probability 34.94%
  - State 1: Time 23411.0726, Probability 53.05%
  - State 2: Time 4977.9404, Probability 11.28%
  - State 3: Time 319.7768, Probability 0.72%
  - State 4: Time 2.7539, Probability 0.01%
- **Number of Losses**: 0

### Queue Q2 (G/G/2/5)
- **Service Rates**: 4.0 to 8.0
- **States**:
  - State 0: Time 18.3511, Probability 0.04%
  - State 1: Time 18.3964, Probability 0.04%
  - State 2: Time 157.0275, Probability 0.36%
  - State 3: Time 1923.3801, Probability 4.36%
  - State 4: Time 11816.0906, Probability 26.77%
  - State 5: Time 30198.6797, Probability 68.43%
- **Number of Losses**: 8020

### Queue Q3 (G/G/2/10)
- **Service Rates**: 5.0 to 15.0
- **States**:
  - State 0: Time 97.1572, Probability 0.22%
  - State 1: Time 186.6345, Probability 0.42%
  - State 2: Time 379.2342, Probability 0.86%
  - State 3: Time 592.2975, Probability 1.34%
  - State 4: Time 1529.9138, Probability 3.47%
  - State 5: Time 1817.0644, Probability 4.12%
  - State 6: Time 2844.5489, Probability 6.45%
  - State 7: Time 4131.0371, Probability 9.36%
  - State 8: Time 7067.6882, Probability 16.01%
  - State 9: Time 10981.7741, Probability 24.88%
  - State 10: Time 14504.5755, Probability 32.87%
- **Number of Losses**: 1174

### Simulation Summary
- **Average Simulation Time**: 44131.9252 seconds

## Conclusion
This simulator is an invaluable resource for anyone looking to understand or teach the dynamics of complex queuing networks and their applications in various fields such as telecommunications, computer networking, and transportation logistics.
