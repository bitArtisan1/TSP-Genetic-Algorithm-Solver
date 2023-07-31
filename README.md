# TSP-Genetic-Algorithm-Solver
This repository contains a Python implementation of a Traveling Salesman Problem (TSP) solver using Genetic Algorithms hybridized with 2-Opt heuristic optimization and Simulated Annealing. The solver also includes metaheuristic optimizations like Ant Colony Optimization (AOC), also, an Interactive GUI with path highlighting and a city diagram drawer.
## Features
### TSP Solver using Genetic Algorithms (GA):
- The Genetic Algorithm is employed to find an approximate solution to the Traveling Salesman Problem.
- The algorithm evolves a population of tours over generations, favoring shorter tours.
- Tournament selection is used to select parents for the crossover process.
- Ordered crossover (OX) is used to create offspring from selected parents.
- Mutation is applied to the offspring with a specified mutation rate to maintain genetic diversity.
### 2-Opt Heuristic Optimization:
After obtaining the best tour from the Genetic Algorithm, a 2-Opt heuristic is applied to further optimize the tour.
The 2-Opt algorithm iteratively swaps pairs of edges in the tour to improve its length.
The process continues until no further improvement is possible.
### Simulated Annealing (SA) Optimization:
Additionally, the 2-Opt optimized tour is subjected to Simulated Annealing optimization to escape local minima and potentially improve the result.
Simulated Annealing is a probabilistic optimization method that allows the algorithm to accept worse solutions with a certain probability based on the current "temperature".
The temperature reduces over time, leading the algorithm to converge toward the optimal solution.
### Pheromone Ant Colony Meta-heuristic Optimization Search (AOC):
The program also implements a separate search using Pheromone-Based Ant Colony Optimization, Pheromone-based ACO algorithm guides the ants to build a solution collectively, based on the pheromone trails deposited on the edges.
## To Add
* Implement other metaheuristics like Particle Swarm Optimization
* Improve the GA structure, Elitism and Population Diversity, Adaptive Mutation Rate
* Experiment with the Lin Kernighan Algorithm
* Improve the GUI for better user communication and clarity, also add the ability to customize the diagram from the GUI
* Expand the program to Solve other operational search problems (A* Algorithm, Djikstra's Algorithmm,...)
## Requirements
It requires `numpy`, `tkinterr`, `matplotlib`:
```
$ pip install numpy tkinter matplotlib

```
