<p align="center">
  <a href="https://ko-fi.com/D1D11CZNM1">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support me on Ko-fi" />
  </a>
</p>


# TSP-Genetic-Algorithm-Solver
This repository contains a Python implementation of a Traveling Salesman Problem (TSP) solver using Genetic Algorithms hybridized with 2-Opt heuristic optimization and Simulated Annealing. The solver also includes metaheuristic optimizations like Ant Colony Optimization (AOC), also, an Interactive GUI with path highlighting and a city diagram drawer.
## What is TSP ?
The traveling salesman problem (TSP) poses the question: "Given a set of cities and the distances between each pair of cities, what is the shortest route that visits each city exactly once and returns to the starting city?" This problem is classified as NP-hard in combinatorial optimization and is of major importance in the realms of theoretical computer science and operations research (OR).
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
### Plotting
Once the search finishes for GA/AOC, the search history will be plotted for analysis and estimation (Generation/Iteration vs Distance).
## To Add
* Implement other metaheuristics like Particle Swarm Optimization.
* Improve the GA structure, Elitism and Population Diversity, Adaptive Mutation Rate.
* Experiment with the Lin Kernighan Algorithm.
* Improve the GUI for better user communication and clarity, also add the ability to customize the diagram from the GUI.
* Expand the program to Solve other operational search problems (A* Algorithm, Djikstra's Algorithmm,...).
* Organize the code into seperate files, add comments.
## Requirements
It requires `numpy`, `tkinterr`, `matplotlib`:
```
$ pip install numpy tkinter matplotlib
```
Install & launch using:
```
$ git clone https://github.com/yanpuri/TSP-Genetic-Algorithm-Solver.git
$ cd TSP-Genetic-Algorithm-Solver
$ python tsp_solver.py
```

You can also modify other parameters for better tunning (alpha, beta, ...)


## Support Me
If you find RepoUp useful, consider supporting me by:

- Starring the repository on GitHub
- Sharing the tool with others
- Providing feedback and suggestions
- Follow me for more :)

<a href="https://ko-fi.com/D1D11CZNM1">
  <img src="https://github.com/user-attachments/assets/ba118768-9054-416f-b7b2-adaa69a53434" alt="Support me on Ko-fi" width="200" />
</a>
    
---
For any issues or feature requests, please open an issue on GitHub. Happy coding!
<center>
<div style="text-align: center;">
  <p align="center">
    <img src="https://github.com/user-attachments/assets/36a3e590-bad2-463d-a25e-f56d65c26761" alt="octodance" width="100" height="100" style="margin-right: 10px;"/>
  </p>
</div>
</center>

