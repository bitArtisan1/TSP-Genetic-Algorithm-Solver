# TSP-Genetic-Algorithm-Solver
This repository contains a Python implementation of a Traveling Salesman Problem (TSP) solver using Genetic Algorithms hybridized with 2-Opt heuristic optimization and Simulated Annealing. The solver also includes metaheuristic optimizations like Ant Colony Optimization (AOC), also, an Interactive GUI with path highlighting and a city diagram drawer.
## Features
* TSP Solver using Genetic Algorithms (GA):
- The Genetic Algorithm is employed to find an approximate solution to the Traveling Salesman Problem.
- The algorithm evolves a population of tours over generations, favoring shorter tours.
- Tournament selection is used to select parents for the crossover process.
- Ordered crossover (OX) is used to create offspring from selected parents.
- Mutation is applied to the offspring with a specified mutation rate to maintain genetic diversity.
