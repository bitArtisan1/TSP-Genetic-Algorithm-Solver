import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import random
import string
import math
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Define the default cities and their coordinates
default_cities = {
    "A": (50, 50),
    "B": (100, 150),
    "C": (200, 100),
    "D": (150, 200),
    "E": (250, 250),
    "F": (300, 50),
    "G": (350, 200),
    "H": (400, 150),
    "I": (450, 250),
    "J": (500, 100),
    "K": (600, 600),
    "L": (550, 50),
    "M": (20, 650),
    "N": (300, 700),
}

# Genetic Algorithm parameters
POPULATION_SIZE = 100
GENERATIONS = 150
MUTATION_RATE = 0.2

PHEROMONE_INIT = 0.1
PHEROMONE_EVAPORATION_RATE = 0.1
ALPHA = 1.0  # Pheromone importance factor
BETA = 2.0


class TSPGeneticAlgorithm(tk.Tk):
    def __init__(self):

        super().__init__()
        self.title("TSP Genetic Algorithm")
        self.geometry("800x700")

        self.cities = default_cities
        self.finished_generations = False

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.canvas_frame, bg="white", scrollregion=(0, 0, 1000, 1000)
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas_scrollbar = ttk.Scrollbar(
            self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.canvas_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.canvas_scrollbar.set)

        self.canvas_hscrollbar = ttk.Scrollbar(
            self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        self.canvas_hscrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.canvas_hscrollbar.set)

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.stats_frame = tk.Frame(self.control_frame)
        self.stats_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.best_tour_label = tk.Label(
            self.stats_frame, text="Best Tour: ", anchor="w", wraplength=150
        )
        self.best_tour_label.pack(padx=10, pady=5)

        self.distance_label = tk.Label(self.stats_frame, text="Distance: ")
        self.distance_label.pack(padx=10, pady=5)

        self.generation_label = tk.Label(self.stats_frame, text="Generation: ")
        self.generation_label.pack(padx=10, pady=5)

        self.current_distance_label = tk.Label(
            self.stats_frame, text="Current Distance"
        )
        self.current_distance_label.pack(padx=10, pady=5)

        self.buttons_frame = tk.Frame(self.control_frame)
        self.buttons_frame.pack(side=tk.RIGHT)

        btn_width = 25
        btn_height = 1

        self.start_btn = tk.Button(
            self.buttons_frame,
            text="Start Genetic Algorithm",
            command=self.run_genetic_algorithm,
            width=btn_width,
            height=btn_height,
        )
        self.start_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.aco_btn = tk.Button(
            self.buttons_frame,
            text="Run Ant Colony Optimization",
            command=self.run_ant_colony_optimization,
            width=btn_width,
            height=btn_height,
        )
        self.aco_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.add_city_btn = tk.Button(
            self.buttons_frame,
            text="Add City",
            command=self.add_random_city,
            width=btn_width,
            height=btn_height,
        )
        self.add_city_btn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.remove_city_btn = tk.Button(
            self.buttons_frame,
            text="Remove City",
            command=self.remove_city,
            width=btn_width,
            height=btn_height,
        )
        self.remove_city_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.draw_cities()

    def prompt_input(self, title, prompt_text, default_value=None):
        return simpledialog.askfloat(
            title, prompt_text, initialvalue=default_value, parent=self
        )

    def prompt_population_size(self):
        return int(
            self.prompt_input(
                "Population Size", "Enter the population size:", default_value=100
            )
        )

    def prompt_generations(self):
        return int(
            self.prompt_input(
                "Generations", "Enter the number of generations:", default_value=150
            )
        )

    def prompt_mutation_rate(self):
        return self.prompt_input(
            "Mutation Rate",
            "Enter the mutation rate (between 0 and 1):",
            default_value=0.1,
        )

    def prompt_iterations(self):
        return int(
            self.prompt_input(
                "Iterations", "Enter the number of iterations:", default_value=100
            )
        )

    def prompt_num_ants(self):
        return int(
            self.prompt_input(
                "Number of Ants", "Enter the number of ants:", default_value=100
            )
        )

    def disable_buttons(self):
        self.start_btn.config(state=tk.DISABLED)
        self.aco_btn.config(state=tk.DISABLED)
        self.add_city_btn.config(state=tk.DISABLED)
        self.remove_city_btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.start_btn.config(state=tk.NORMAL)
        self.aco_btn.config(state=tk.NORMAL)
        self.add_city_btn.config(state=tk.NORMAL)
        self.remove_city_btn.config(state=tk.NORMAL)

    def add_random_city(self):
        alphabet = string.ascii_uppercase
        existing_cities = set(self.cities.keys())

        remaining_cities = [city for city in alphabet if city not in existing_cities]

        if not remaining_cities:
            messagebox.showinfo(
                "No Cities to Add", "All cities have already been added."
            )
            return

        city_name = remaining_cities[0]
        x = random.randint(50, 750)
        y = random.randint(50, 450)
        self.add_city(city_name, x, y)

    def add_city(self, city_name, x, y):
        self.cities[city_name] = (x, y)
        self.draw_cities()

    def remove_city(self):
        if self.cities:
            city_name = random.choice(list(self.cities.keys()))
            del self.cities[city_name]
            self.draw_cities()

    def draw_cities(self):
        self.canvas.delete("all")

        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")

        for city, (x, y) in self.cities.items():
            self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5, fill="red", width=0, tags=city
            )  # Smoother nodes
            self.canvas.create_text(
                x, y - 15, text=city, font=("Arial", 10, "bold"), tags=city
            )
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        for city1 in self.cities:
            for city2 in self.cities:
                if city1 != city2:
                    x1, y1 = self.cities[city1]
                    x2, y2 = self.cities[city2]
                    self.canvas.create_line(
                        x1, y1, x2, y2, fill="gray", width=1, smooth=True
                    )

        for city in self.cities:
            self.canvas.tag_raise(city)

        self.canvas.config(
            scrollregion=(min_x - 50, min_y - 50, max_x + 50, max_y + 50)
        )

    def calculate_distance(self, tour):
        return sum(self.distance(city1, city2) for city1, city2 in zip(tour, tour[1:]))

    def distance(self, city1, city2):
        x1, y1 = self.cities[city1]
        x2, y2 = self.cities[city2]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def initialize_population(self):
        cities_list = list(self.cities.keys())
        return [
            random.sample(cities_list, len(cities_list)) for _ in range(POPULATION_SIZE)
        ]

    def ordered_crossover(self, parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [-1] * len(parent1)
        child[start : end + 1] = parent1[start : end + 1]

        remaining_cities = [city for city in parent2 if city not in child]

        # Fill the remaining positions in the child by wrapping around from the end
        index = end + 1
        for city in remaining_cities:
            if index >= len(child):
                index = 0
            if child[index] == -1:
                child[index] = city
                index += 1

        return child

    def mutate(self, tour):
        if random.random() < MUTATION_RATE:
            mutation_points = random.sample(range(len(tour)), 2)
            tour[mutation_points[0]], tour[mutation_points[1]] = (
                tour[mutation_points[1]],
                tour[mutation_points[0]],
            )

    def tournament_selection(self, population, num_parents):
        parents = []
        for _ in range(num_parents):
            tournament_contestants = random.sample(population, 5)
            winner = min(
                tournament_contestants, key=lambda tour: self.calculate_distance(tour)
            )
            parents.append(winner)
        return parents

    def plot_best_distances(self):
        plt.plot(range(len(self.best_distances)), self.best_distances)
        plt.xlabel("Generation")
        plt.ylabel("Best Distance")
        plt.title("Evolution of Best Tour Distance")
        plt.show()

    def draw_path(self, tour, color="blue"):
        self.canvas.delete(f"path_{color}")
        for i in range(len(tour) - 1):
            city1 = tour[i]
            city2 = tour[i + 1]
            x1, y1 = self.cities[city1]
            x2, y2 = self.cities[city2]
            self.canvas.create_line(
                x1, y1, x2, y2, fill=color, tags=f"path_{color}", width=2, smooth=True
            )

        # Return to the starting city to complete the loop
        first_city = tour[0]
        last_city = tour[-1]
        x1, y1 = self.cities[last_city]
        x2, y2 = self.cities[first_city]
        self.canvas.create_line(
            x1, y1, x2, y2, fill=color, tags=f"path_{color}", smooth=True
        )

    def run_genetic_algorithm(self):
        # Prompt for input parameters
        global POPULATION_SIZE, GENERATIONS, MUTATION_RATE
        POPULATION_SIZE = self.prompt_population_size()
        GENERATIONS = self.prompt_generations()
        MUTATION_RATE = self.prompt_mutation_rate()

        population = self.initialize_population()
        self.best_distances = []
        self.finished_generations = False

        def run_generation(generation, population):
            if generation == 0:
                # Draw the blue path only once before starting the genetic algorithm
                best_tour = min(
                    population, key=lambda tour: self.calculate_distance(tour)
                )
                self.draw_path(
                    best_tour, color="blue"
                )  # Draw the original path in blue
                self.update()

            if generation >= GENERATIONS:
                if not self.finished_generations:
                    self.finished_generations = (
                        True  # Mark that final generation is reached
                    )
                    best_tour = min(
                        population, key=lambda tour: self.calculate_distance(tour)
                    )
                    best_distance = self.calculate_distance(best_tour)

                    print(f"\nFinal Result (before 2-opt optimization):")
                    print(f"Best Tour: {best_tour}")
                    print(f"Distance: {best_distance}")

                    # Apply 2-opt optimization to the best tour
                    best_tour_optimized, best_distance_optimized = self.opt2_heuristic(
                        best_tour
                    )
                    # Apply simulated annealing optimization to the opt2 heuristic
                    (
                        best_tour_simulated_optimized,
                        best_distance_simulated_optimized,
                    ) = self.simulated_annealing(
                        best_tour_optimized,
                        initial_temperature=100.0,
                        temperature_reduction_rate=0.95,
                        max_iterations=100,
                    )

                    print(
                        f"\nFinal Result (after 2-opt optimization & SA optimization):"
                    )
                    print(f"Best Tour: {best_tour_simulated_optimized}")
                    print(f"Distance: {best_distance_simulated_optimized}")

                    # Show the final result with 2-opt optimization in a message box
                    messagebox.showinfo(
                        "Genetic Algorithm Result with 2-opt Optimization & SA Opt",
                        f"Best Tour (before optimization): {best_tour}\nDistance: {best_distance}\n\n"
                        f"Best Tour (after 2-opt optimization & SA Opt): {best_tour_simulated_optimized}\n"
                        f"Distance (optimized): {best_distance_simulated_optimized}",
                    )

                    # Draw the original path in blue
                    self.draw_cities()
                    self.draw_path(best_tour, color="blue")

                    # Draw the optimized path in green
                    self.draw_path(best_tour_simulated_optimized, color="green")

                    self.update()
                    self.best_distances.append(best_distance_simulated_optimized)
                    best_tour = min(
                        population, key=lambda tour: self.calculate_distance(tour)
                    )
                    best_distance = self.calculate_distance(best_tour)
                    self.enable_buttons()

                    # If you want to plot the best distances, you can call the method here
                    self.plot_best_distances()

                return  # Add a return statement here to exit the function when reaching the final generation

            self.disable_buttons()

            fitness_values = [self.calculate_distance(tour) for tour in population]
            best_tour_index = fitness_values.index(min(fitness_values))
            current_best_tour = population[best_tour_index]
            current_best_distance = self.calculate_distance(current_best_tour)

            print(
                f"Generation {generation}: Best Tour = {current_best_tour}, Distance = {current_best_distance}"
            )

            self.best_tour_label.config(text=f"Best Tour: {current_best_tour}")
            self.distance_label.config(text=f"Distance: {current_best_distance}")
            self.generation_label.config(text=f"Generation: {generation}")
            self.current_distance_label.config(
                text=f"Current Distance: {current_best_distance}"
            )

            parents = self.tournament_selection(population, int(POPULATION_SIZE / 2))
            offspring = []
            for i in range(0, len(parents), 2):
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child = self.ordered_crossover(parent1, parent2)
                offspring.append(child)

            for tour in offspring:
                self.mutate(tour)

            population.extend(offspring)
            population.sort(key=lambda tour: self.calculate_distance(tour))
            population = population[:POPULATION_SIZE]

            self.draw_cities()
            self.draw_path(current_best_tour)  # Draw path for the current best tour
            self.update()

            self.best_distances.append(current_best_distance)

            # Adjust the delay between generations (100 ms) to make the algorithm run faster
            self.after(1, run_generation, generation + 1, population)

        run_generation(0, population)

        # After the Genetic Algorithm finishes, you can show the result in a message box

    def initialize_pheromone(self):
        # This method initializes the pheromone matrix with a small constant value
        num_cities = len(self.cities)
        self.pheromone = np.full((num_cities, num_cities), PHEROMONE_INIT)

        # Create a mapping of city names to their corresponding indices in the pheromone matrix
        self.city_indices = {city: index for index, city in enumerate(self.cities)}

    def evaporate_pheromone(self):
        # This method updates the pheromone trails by evaporating a certain percentage
        # of the pheromone on all edges
        self.pheromone *= 1.0 - PHEROMONE_EVAPORATION_RATE

    def ant_colony_tour(self):
        # This method performs a single ant tour, following the pheromone trails
        cities_list = list(self.cities.keys())
        num_cities = len(cities_list)
        tour = []

        # Start from a random city
        current_city = random.choice(cities_list)
        tour.append(current_city)

        # Build the tour
        while len(tour) < num_cities:
            # Compute the probabilities for the next city selection
            available_cities = [city for city in cities_list if city not in tour]
            probabilities = [
                (
                    self.pheromone[cities_list.index(current_city)][
                        cities_list.index(city)
                    ]
                    ** ALPHA
                )
                * (1.0 / self.distance(current_city, city) ** BETA)
                for city in available_cities
            ]
            probabilities_sum = sum(probabilities)
            probabilities = [p / probabilities_sum for p in probabilities]

            # Select the next city using roulette wheel selection
            next_city = np.random.choice(available_cities, p=probabilities)
            tour.append(next_city)
            current_city = next_city

        return tour

    def run_ant_colony_optimization(self):
        global GENERATIONS, POPULATION_SIZE
        num_iterations = self.prompt_iterations()
        num_ants = self.prompt_num_ants()
        self.disable_buttons()

        self.initialize_pheromone()
        self.best_distances = []

        for iteration in range(num_iterations):
            ants_tours = [self.ant_colony_tour() for _ in range(num_ants)]

            best_tour = min(ants_tours, key=lambda tour: self.calculate_distance(tour))
            best_distance = self.calculate_distance(best_tour)

            # Update pheromone trails
            for tour in ants_tours:
                tour_distance = self.calculate_distance(tour)
                for i in range(len(tour) - 1):
                    city1 = tour[i]
                    city2 = tour[i + 1]
                    index_city1 = self.city_indices[city1]
                    index_city2 = self.city_indices[city2]
                    self.pheromone[index_city1][index_city2] += 1.0 / tour_distance

            self.evaporate_pheromone()

            print(
                f"Iteration {iteration}: Best Tour = {best_tour}, Distance = {best_distance}"
            )

            self.best_tour_label.config(text=f"Best Tour: {best_tour}")
            self.distance_label.config(text=f"Distance: {best_distance}")
            self.generation_label.config(text=f"Generation: {iteration}")
            self.current_distance_label.config(
                text=f"Current Distance: {best_distance}"
            )

            self.draw_cities()
            self.draw_path(best_tour)  # Draw path for the current best tour
            self.update()

            self.best_distances.append(best_distance)

        # After the ACO algorithm finishes, you can show the result in a message box
        messagebox.showinfo(
            "Ant Colony Optimization Result",
            f"Best Tour: {best_tour}\nDistance: {best_distance}",
        )

        # If you want to plot the best distances, you can call the method here
        self.enable_buttons()
        self.plot_best_distances()

    def opt2_heuristic(self, tour):

        num_cities = len(tour)
        improved = True
        best_distance = self.calculate_distance(tour)

        while improved:
            improved = False
            for i in range(1, num_cities - 2):
                for j in range(i + 1, num_cities):
                    if j - i == 1:
                        continue  # No improvement is possible for adjacent edges
                    new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                    new_distance = self.calculate_distance(new_tour)
                    if new_distance < best_distance:
                        tour = new_tour
                        best_distance = new_distance
                        improved = True

        return tour, best_distance

    def simulated_annealing(
        self, tour, initial_temperature, temperature_reduction_rate, max_iterations
    ):
        def acceptance_probability(new_distance, current_distance, temperature):

            if new_distance < current_distance:
                return 1.0
            else:
                return math.exp((current_distance - new_distance) / temperature)

        current_tour = tour.copy()
        current_distance = self.calculate_distance(current_tour)

        best_tour = current_tour.copy()
        best_distance = current_distance

        temperature = initial_temperature

        for iteration in range(max_iterations):
            new_tour = current_tour.copy()

            # Perform a random 2-opt swap
            i, j = random.sample(range(1, len(new_tour) - 1), 2)
            new_tour[i:j] = reversed(new_tour[i:j])

            new_distance = self.calculate_distance(new_tour)

            if (
                acceptance_probability(new_distance, current_distance, temperature)
                > random.random()
            ):
                current_tour = new_tour
                current_distance = new_distance

                if current_distance < best_distance:
                    best_tour = current_tour
                    best_distance = current_distance

            temperature *= temperature_reduction_rate

        return best_tour, best_distance


if __name__ == "__main__":
    app = TSPGeneticAlgorithm()
    app.mainloop()
