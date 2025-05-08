import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog
import random
import string
import math
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import json

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


class TSPGeneticAlgorithm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced TSP Solver")
        self.geometry("1000x800")

        style = ttk.Style(self)
        available_themes = style.theme_names()
        try:
            style.theme_use("clam")
        except tk.TclError:
            style.theme_use(style.theme_names()[0])

        self.cities = default_cities.copy()
        self.finished_generations = False
        self.best_distances = []

        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas_frame = ttk.Frame(main_pane, padding=5)
        main_pane.add(self.canvas_frame, weight=3)

        self.canvas = tk.Canvas(
            self.canvas_frame, bg="white", scrollregion=(0, 0, 1000, 1000)
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas_scrollbar_y = ttk.Scrollbar(
            self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.canvas_scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.canvas_scrollbar_y.set)

        self.canvas_scrollbar_x = ttk.Scrollbar(
            self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        self.canvas_scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.canvas_scrollbar_x.set)

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.control_panel = ttk.Frame(main_pane, padding=10)
        main_pane.add(self.control_panel, weight=1)

        params_labelframe = ttk.LabelFrame(
            self.control_panel, text="Algorithm Parameters", padding=10
        )
        params_labelframe.pack(fill=tk.X, pady=5)

        ga_params_frame = ttk.Frame(params_labelframe)
        ga_params_frame.pack(fill=tk.X)
        ttk.Label(
            ga_params_frame, text="Genetic Algorithm:", font=("Helvetica", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        ttk.Label(ga_params_frame, text="Population Size:").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.population_size_var = tk.IntVar(value=100)
        ttk.Spinbox(
            ga_params_frame,
            from_=10,
            to=1000,
            increment=10,
            textvariable=self.population_size_var,
            width=8,
        ).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(ga_params_frame, text="Generations:").grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.generations_var = tk.IntVar(value=150)
        ttk.Spinbox(
            ga_params_frame,
            from_=10,
            to=2000,
            increment=10,
            textvariable=self.generations_var,
            width=8,
        ).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(ga_params_frame, text="Mutation Rate:").grid(
            row=3, column=0, sticky="w", padx=5, pady=2
        )
        self.mutation_rate_var = tk.DoubleVar(value=0.2)
        ttk.Scale(
            ga_params_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.mutation_rate_var,
        ).grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(ga_params_frame, textvariable=self.mutation_rate_var, width=4).grid(
            row=3, column=2, sticky="w"
        )

        aco_params_frame = ttk.Frame(params_labelframe)
        aco_params_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(
            aco_params_frame,
            text="Ant Colony Optimization:",
            font=("Helvetica", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        ttk.Label(aco_params_frame, text="Num Ants:").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.num_ants_var = tk.IntVar(value=50)
        ttk.Spinbox(
            aco_params_frame,
            from_=5,
            to=500,
            increment=5,
            textvariable=self.num_ants_var,
            width=8,
        ).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(aco_params_frame, text="Iterations (ACO):").grid(
            row=2, column=0, sticky="w", padx=5, pady=2
        )
        self.aco_iterations_var = tk.IntVar(value=100)
        ttk.Spinbox(
            aco_params_frame,
            from_=10,
            to=1000,
            increment=10,
            textvariable=self.aco_iterations_var,
            width=8,
        ).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(aco_params_frame, text="Pheromone Init:").grid(
            row=3, column=0, sticky="w", padx=5, pady=2
        )
        self.pheromone_init_var = tk.DoubleVar(value=0.1)
        ttk.Entry(aco_params_frame, textvariable=self.pheromone_init_var, width=8).grid(
            row=3, column=1, sticky="ew", padx=5, pady=2
        )

        ttk.Label(aco_params_frame, text="Evaporation Rate:").grid(
            row=4, column=0, sticky="w", padx=5, pady=2
        )
        self.evaporation_rate_var = tk.DoubleVar(value=0.1)
        ttk.Scale(
            aco_params_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.evaporation_rate_var,
        ).grid(row=4, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(
            aco_params_frame, textvariable=self.evaporation_rate_var, width=4
        ).grid(row=4, column=2, sticky="w")

        ttk.Label(aco_params_frame, text="Alpha (Pheromone):").grid(
            row=5, column=0, sticky="w", padx=5, pady=2
        )
        self.alpha_var = tk.DoubleVar(value=1.0)
        ttk.Scale(
            aco_params_frame,
            from_=0.0,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.alpha_var,
        ).grid(row=5, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(aco_params_frame, textvariable=self.alpha_var, width=4).grid(
            row=5, column=2, sticky="w"
        )

        ttk.Label(aco_params_frame, text="Beta (Heuristic):").grid(
            row=6, column=0, sticky="w", padx=5, pady=2
        )
        self.beta_var = tk.DoubleVar(value=2.0)
        ttk.Scale(
            aco_params_frame,
            from_=0.0,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.beta_var,
        ).grid(row=6, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(aco_params_frame, textvariable=self.beta_var, width=4).grid(
            row=6, column=2, sticky="w"
        )

        city_management_labelframe = ttk.LabelFrame(
            self.control_panel, text="City Management", padding=10
        )
        city_management_labelframe.pack(fill=tk.X, pady=10)

        add_city_frame = ttk.Frame(city_management_labelframe)
        add_city_frame.pack(fill=tk.X)
        ttk.Label(add_city_frame, text="Name:").grid(row=0, column=0, padx=2, pady=2)
        self.city_name_entry = ttk.Entry(add_city_frame, width=5)
        self.city_name_entry.grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(add_city_frame, text="X:").grid(row=0, column=2, padx=2, pady=2)
        self.city_x_entry = ttk.Entry(add_city_frame, width=5)
        self.city_x_entry.grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(add_city_frame, text="Y:").grid(row=0, column=4, padx=2, pady=2)
        self.city_y_entry = ttk.Entry(add_city_frame, width=5)
        self.city_y_entry.grid(row=0, column=5, padx=2, pady=2)
        self.add_specific_city_btn = ttk.Button(
            add_city_frame, text="Add City", command=self.add_specific_city
        )
        self.add_specific_city_btn.grid(row=0, column=6, padx=5, pady=2)

        self.add_random_city_btn = ttk.Button(
            city_management_labelframe,
            text="Add Random City",
            command=self.add_random_city,
        )
        self.add_random_city_btn.pack(fill=tk.X, pady=2)

        remove_city_frame = ttk.Frame(city_management_labelframe)
        remove_city_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(remove_city_frame, text="Remove City (Name):").grid(
            row=0, column=0, padx=2, pady=2
        )
        self.remove_city_name_entry = ttk.Entry(remove_city_frame, width=10)
        self.remove_city_name_entry.grid(row=0, column=1, padx=2, pady=2)
        self.remove_specific_city_btn = ttk.Button(
            remove_city_frame, text="Remove", command=self.remove_specific_city
        )
        self.remove_specific_city_btn.grid(row=0, column=2, padx=5, pady=2)

        self.remove_last_city_btn = ttk.Button(
            city_management_labelframe,
            text="Remove Last Added City",
            command=self.remove_last_city,
        )
        self.remove_last_city_btn.pack(fill=tk.X, pady=2)

        self.clear_cities_btn = ttk.Button(
            city_management_labelframe,
            text="Clear All Cities",
            command=self.clear_all_cities,
        )
        self.clear_cities_btn.pack(fill=tk.X, pady=2)

        city_file_frame = ttk.Frame(city_management_labelframe)
        city_file_frame.pack(fill=tk.X, pady=(5, 0))
        self.save_cities_btn = ttk.Button(
            city_file_frame, text="Save Cities", command=self.save_cities_to_file
        )
        self.save_cities_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.load_cities_btn = ttk.Button(
            city_file_frame, text="Load Cities", command=self.load_cities_from_file
        )
        self.load_cities_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        algo_control_labelframe = ttk.LabelFrame(
            self.control_panel, text="Algorithm Controls", padding=10
        )
        algo_control_labelframe.pack(fill=tk.X, pady=10)

        self.start_ga_btn = ttk.Button(
            algo_control_labelframe,
            text="Start Genetic Algorithm",
            command=self.run_genetic_algorithm,
        )
        self.start_ga_btn.pack(fill=tk.X, pady=3)

        self.start_aco_btn = ttk.Button(
            algo_control_labelframe,
            text="Run Ant Colony Optimization",
            command=self.run_ant_colony_optimization,
        )
        self.start_aco_btn.pack(fill=tk.X, pady=3)

        self.stop_algo_btn = ttk.Button(
            algo_control_labelframe,
            text="Stop Algorithm",
            command=self.stop_algorithm,
            state=tk.DISABLED,
        )
        self.stop_algo_btn.pack(fill=tk.X, pady=3)
        self.running_algorithm = False

        stats_labelframe = ttk.LabelFrame(
            self.control_panel, text="Statistics", padding=10
        )
        stats_labelframe.pack(fill=tk.BOTH, expand=True, pady=5)

        self.best_tour_label = ttk.Label(
            stats_labelframe, text="Best Tour: N/A", anchor="w", wraplength=200
        )
        self.best_tour_label.pack(padx=5, pady=2, fill=tk.X)

        self.distance_label = ttk.Label(stats_labelframe, text="Distance: N/A")
        self.distance_label.pack(padx=5, pady=2, fill=tk.X)

        self.generation_label = ttk.Label(
            stats_labelframe, text="Generation/Iteration: N/A"
        )
        self.generation_label.pack(padx=5, pady=2, fill=tk.X)

        self.current_distance_label = ttk.Label(
            stats_labelframe, text="Current Best Distance: N/A"
        )
        self.current_distance_label.pack(padx=5, pady=2, fill=tk.X)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            stats_labelframe,
            orient=tk.HORIZONTAL,
            mode="determinate",
            variable=self.progress_var,
        )
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)

        self.draw_cities()
        self.last_added_city_key = None

    def prompt_input(self, title, prompt_text, default_value=None):
        return simpledialog.askfloat(
            title, prompt_text, initialvalue=default_value, parent=self
        )

    def disable_buttons_during_run(self):
        self.start_ga_btn.config(state=tk.DISABLED)
        self.start_aco_btn.config(state=tk.DISABLED)
        self.add_specific_city_btn.config(state=tk.DISABLED)
        self.add_random_city_btn.config(state=tk.DISABLED)
        self.remove_specific_city_btn.config(state=tk.DISABLED)
        self.remove_last_city_btn.config(state=tk.DISABLED)
        self.clear_cities_btn.config(state=tk.DISABLED)
        self.save_cities_btn.config(state=tk.DISABLED)
        self.load_cities_btn.config(state=tk.DISABLED)
        self.stop_algo_btn.config(state=tk.NORMAL)

    def enable_buttons_after_run(self):
        self.start_ga_btn.config(state=tk.NORMAL)
        self.start_aco_btn.config(state=tk.NORMAL)
        self.add_specific_city_btn.config(state=tk.NORMAL)
        self.add_random_city_btn.config(state=tk.NORMAL)
        self.remove_specific_city_btn.config(state=tk.NORMAL)
        self.remove_last_city_btn.config(state=tk.NORMAL)
        self.clear_cities_btn.config(state=tk.NORMAL)
        self.save_cities_btn.config(state=tk.NORMAL)
        self.load_cities_btn.config(state=tk.NORMAL)
        self.stop_algo_btn.config(state=tk.DISABLED)
        self.running_algorithm = False
        self.progress_var.set(0)

    def stop_algorithm(self):
        self.running_algorithm = False
        messagebox.showinfo(
            "Algorithm Stopped", "The algorithm has been stopped by the user."
        )
        self.enable_buttons_after_run()

    def add_specific_city(self):
        name = self.city_name_entry.get().strip().upper()
        x_str = self.city_x_entry.get().strip()
        y_str = self.city_y_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "City name cannot be empty.")
            return
        if name in self.cities:
            messagebox.showerror("Error", f"City '{name}' already exists.")
            return
        if not name.isalpha() or len(name) > 2:
            messagebox.showerror(
                "Error", "City name should be 1 or 2 alphabetic characters."
            )
            return

        try:
            x = int(x_str)
            y = int(y_str)
            if not (0 <= x <= 1000 and 0 <= y <= 1000):
                raise ValueError("Coordinates out of typical range.")
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid coordinates. Please enter numbers (e.g., 0-1000)."
            )
            return

        self.cities[name] = (x, y)
        self.last_added_city_key = name
        self.draw_cities()
        self.city_name_entry.delete(0, tk.END)
        self.city_x_entry.delete(0, tk.END)
        self.city_y_entry.delete(0, tk.END)

    def add_random_city(self):
        alphabet = string.ascii_uppercase + "".join(
            [
                f"{c1}{c2}"
                for c1 in string.ascii_uppercase
                for c2 in string.ascii_uppercase
            ]
        )
        existing_cities = set(self.cities.keys())

        new_city_name = None
        for char_code in range(ord("A"), ord("Z") + 1):
            name = chr(char_code)
            if name not in existing_cities:
                new_city_name = name
                break
        if not new_city_name:
            for i in range(26):
                for j in range(26):
                    name = chr(ord("A") + i) + chr(ord("A") + j)
                    if name not in existing_cities:
                        new_city_name = name
                        break
                if new_city_name:
                    break

        if not new_city_name:
            messagebox.showinfo(
                "No Cities to Add", "Maximum default city names reached. Add manually."
            )
            return

        max_attempts = 10
        for _ in range(max_attempts):
            x = random.randint(
                50,
                min(
                    750,
                    self.canvas.winfo_width() - 50
                    if self.canvas.winfo_width() > 100
                    else 750,
                ),
            )
            y = random.randint(
                50,
                min(
                    450,
                    self.canvas.winfo_height() - 50
                    if self.canvas.winfo_height() > 100
                    else 450,
                ),
            )

            too_close = False
            for ox, oy in self.cities.values():
                if math.sqrt((x - ox) ** 2 + (y - oy) ** 2) < 30:
                    too_close = True
                    break
            if not too_close:
                break
        else:
            x = random.randint(50, 750)
            y = random.randint(50, 450)

        self.cities[new_city_name] = (x, y)
        self.last_added_city_key = new_city_name
        self.draw_cities()

    def remove_specific_city(self):
        name_to_remove = self.remove_city_name_entry.get().strip().upper()
        if not name_to_remove:
            messagebox.showerror("Error", "Please enter a city name to remove.")
            return
        if name_to_remove in self.cities:
            del self.cities[name_to_remove]
            if self.last_added_city_key == name_to_remove:
                self.last_added_city_key = None
            self.draw_cities()
            self.remove_city_name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"City '{name_to_remove}' not found.")

    def remove_last_city(self):
        if self.last_added_city_key and self.last_added_city_key in self.cities:
            del self.cities[self.last_added_city_key]
            self.last_added_city_key = None
            self.draw_cities()
        elif self.cities:
            city_name = list(self.cities.keys())[-1]
            del self.cities[city_name]
            self.draw_cities()
        else:
            messagebox.showinfo("Info", "No cities to remove.")

    def clear_all_cities(self):
        if messagebox.askyesno(
            "Confirm", "Are you sure you want to remove all cities?"
        ):
            self.cities.clear()
            self.last_added_city_key = None
            self.draw_cities()
            self.best_tour_label.config(text="Best Tour: N/A")
            self.distance_label.config(text="Distance: N/A")
            self.generation_label.config(text="Generation/Iteration: N/A")
            self.current_distance_label.config(text="Current Best Distance: N/A")
            self.canvas.delete("path_blue", "path_green")

    def save_cities_to_file(self):
        if not self.cities:
            messagebox.showinfo("No Cities", "There are no cities to save.")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Cities As",
        )
        if filepath:
            try:
                with open(filepath, "w") as f:
                    json.dump(self.cities, f, indent=4)
                messagebox.showinfo("Success", f"Cities saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Error Saving File", f"Could not save cities: {e}")

    def load_cities_from_file(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Cities From File",
        )
        if filepath:
            try:
                with open(filepath, "r") as f:
                    loaded_cities = json.load(f)
                if not isinstance(loaded_cities, dict):
                    raise ValueError("File does not contain a valid city dictionary.")
                for name, coords in loaded_cities.items():
                    if not (
                        isinstance(name, str)
                        and isinstance(coords, list)
                        and len(coords) == 2
                        and all(isinstance(c, (int, float)) for c in coords)
                    ):
                        raise ValueError("Invalid city data format in file.")

                if messagebox.askyesno(
                    "Confirm Load", "Loading will replace current cities. Continue?"
                ):
                    self.cities = {
                        name: tuple(coords) for name, coords in loaded_cities.items()
                    }
                    self.last_added_city_key = None
                    self.draw_cities()
                    messagebox.showinfo("Success", f"Cities loaded from {filepath}")
            except Exception as e:
                messagebox.showerror(
                    "Error Loading File", f"Could not load cities: {e}"
                )

    def draw_cities(self):
        self.canvas.delete("all")
        if not self.cities:
            self.canvas.config(scrollregion=(0, 0, 100, 100))
            return

        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")

        for city, (x, y) in self.cities.items():
            self.canvas.create_oval(
                x - 6,
                y - 6,
                x + 6,
                y + 6,
                fill="dodgerblue",
                outline="blue",
                width=1,
                tags=city,
            )
            self.canvas.create_text(
                x,
                y - 15,
                text=city,
                font=("Arial", 10, "bold"),
                fill="black",
                tags=city,
            )
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        if len(self.cities) < 20:
            for city1 in self.cities:
                for city2 in self.cities:
                    if city1 != city2:
                        x1, y1 = self.cities[city1]
                        x2, y2 = self.cities[city2]
                        self.canvas.create_line(
                            x1, y1, x2, y2, fill="lightgrey", width=1, dash=(2, 2)
                        )

        for city_tag in self.cities.keys():
            self.canvas.tag_raise(city_tag)

        pad = 50
        s_min_x = min_x - pad if min_x != float("inf") else 0
        s_min_y = min_y - pad if min_y != float("inf") else 0
        s_max_x = max_x + pad if max_x != float("-inf") else self.canvas.winfo_width()
        s_max_y = max_y + pad if max_y != float("-inf") else self.canvas.winfo_height()
        self.canvas.config(scrollregion=(s_min_x, s_min_y, s_max_x, s_max_y))
        self.update_idletasks()

    def calculate_distance(self, tour):
        if not tour or len(tour) < 2:
            return 0
        return sum(
            self.distance(tour[i], tour[i + 1]) for i in range(len(tour) - 1)
        ) + self.distance(tour[-1], tour[0])

    def distance(self, city1_name, city2_name):
        if city1_name not in self.cities or city2_name not in self.cities:
            print(
                f"Warning: City not found in distance calculation: {city1_name} or {city2_name}"
            )
            return float("inf")
        x1, y1 = self.cities[city1_name]
        x2, y2 = self.cities[city2_name]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def initialize_population(self, population_size_val):
        cities_list = list(self.cities.keys())
        if not cities_list:
            return []
        return [
            random.sample(cities_list, len(cities_list))
            for _ in range(population_size_val)
        ]

    def tournament_selection(self, population, num_parents):
        parents = []
        if not population:
            return []

        tournament_size = 5
        if len(population) < tournament_size:
            tournament_size = len(population)

        for _ in range(num_parents):
            if not population:
                break
            if tournament_size == 0:
                break
            tournament_contestants = random.sample(population, tournament_size)
            winner = min(
                tournament_contestants, key=lambda tour: self.calculate_distance(tour)
            )
            parents.append(winner)
        return parents

    def ordered_crossover(self, parent1, parent2):
        if not parent1 or not parent2:
            return []
        size = len(parent1)
        child = [-1] * size

        start, end = sorted(random.sample(range(size), 2))

        child[start : end + 1] = parent1[start : end + 1]

        pointer = 0
        for i in range(size):
            if child[i] == -1:
                while parent2[pointer] in child:
                    pointer += 1
                child[i] = parent2[pointer]
                pointer += 1
        return child

    def mutate(self, tour, mutation_rate_val):
        if not tour or len(tour) < 2:
            return
        if random.random() < mutation_rate_val:
            idx1, idx2 = random.sample(range(len(tour)), 2)
            tour[idx1], tour[idx2] = tour[idx2], tour[idx1]

    def draw_path(self, tour, color="blue", tag_suffix=""):
        tag = f"path_{color}{tag_suffix}"
        self.canvas.delete(tag)
        if not tour or len(tour) < 2:
            return

        for i in range(len(tour) - 1):
            city1 = tour[i]
            city2 = tour[i + 1]
            if city1 not in self.cities or city2 not in self.cities:
                continue
            x1, y1 = self.cities[city1]
            x2, y2 = self.cities[city2]
            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                tags=tag,
                width=2,
                smooth=True,
                arrow=tk.LAST if len(tour) < 15 else None,
            )

        first_city = tour[0]
        last_city = tour[-1]
        if first_city not in self.cities or last_city not in self.cities:
            return
        x1, y1 = self.cities[last_city]
        x2, y2 = self.cities[first_city]
        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            tags=tag,
            width=2,
            smooth=True,
            arrow=tk.LAST if len(tour) < 15 else None,
        )
        self.canvas.tag_lower(tag)

    def run_genetic_algorithm(self):
        if len(self.cities) < 3:
            messagebox.showinfo(
                "Not Enough Cities",
                "Please add at least 3 cities to run the algorithm.",
            )
            return

        self.running_algorithm = True
        self.disable_buttons_during_run()

        POPULATION_SIZE_VAL = self.population_size_var.get()
        GENERATIONS_VAL = self.generations_var.get()
        MUTATION_RATE_VAL = self.mutation_rate_var.get()

        population = self.initialize_population(POPULATION_SIZE_VAL)
        if not population:
            self.enable_buttons_after_run()
            return

        self.best_distances = []
        self.finished_generations = False
        self.progress_bar.config(maximum=GENERATIONS_VAL)
        self.progress_var.set(0)

        self.canvas.delete("path_blue")
        self.canvas.delete("path_green")
        self.draw_cities()

        initial_best_tour = min(
            population, key=lambda tour: self.calculate_distance(tour)
        )
        self.draw_path(initial_best_tour, color="orange", tag_suffix="_initial_ga")

        def run_generation_step(generation, current_population):
            if not self.running_algorithm:
                self.enable_buttons_after_run()
                return

            if generation >= GENERATIONS_VAL:
                if not self.finished_generations:
                    self.finished_generations = True
                    final_best_tour = min(
                        current_population,
                        key=lambda tour: self.calculate_distance(tour),
                    )
                    final_best_distance = self.calculate_distance(final_best_tour)

                    print(f"\nGA Final Result (before 2-opt optimization):")
                    print(f"Best Tour: {final_best_tour}")
                    print(f"Distance: {final_best_distance:.2f}")

                    best_tour_opt2, best_distance_opt2 = self.opt2_heuristic(
                        final_best_tour
                    )
                    best_tour_sa, best_distance_sa = self.simulated_annealing(
                        best_tour_opt2,
                        initial_temperature=100.0,
                        temperature_reduction_rate=0.95,
                        max_iterations=100,
                    )

                    print(f"\nGA Final Result (after 2-opt & SA optimization):")
                    print(f"Best Tour: {best_tour_sa}")
                    print(f"Distance: {best_distance_sa:.2f}")

                    messagebox.showinfo(
                        "Genetic Algorithm - Final Result",
                        f"Initial Best Tour (Generation 0): {initial_best_tour}\nDistance: {self.calculate_distance(initial_best_tour):.2f}\n\n"
                        f"Best Tour (Before Opt): {final_best_tour}\nDistance: {final_best_distance:.2f}\n\n"
                        f"Best Tour (After 2-opt & SA): {best_tour_sa}\n"
                        f"Distance (Optimized): {best_distance_sa:.2f}",
                    )
                    self.draw_cities()
                    self.draw_path(
                        final_best_tour, color="blue", tag_suffix="_final_pre_opt"
                    )
                    self.draw_path(
                        best_tour_sa, color="green", tag_suffix="_final_post_opt"
                    )
                    self.update()
                    self.best_distances.append(best_distance_sa)
                    self.enable_buttons_after_run()
                    self.plot_best_distances("GA Best Distances over Generations")
                return

            fitness_values = [
                self.calculate_distance(tour) for tour in current_population
            ]
            best_tour_index = fitness_values.index(min(fitness_values))
            current_best_tour_in_gen = current_population[best_tour_index]
            current_best_distance_in_gen = fitness_values[best_tour_index]

            self.best_tour_label.config(
                text=f"Best Tour: {'-'.join(current_best_tour_in_gen)}"
            )
            self.distance_label.config(
                text=f"Distance: {current_best_distance_in_gen:.2f}"
            )
            self.generation_label.config(
                text=f"Generation: {generation}/{GENERATIONS_VAL}"
            )
            self.current_distance_label.config(
                text=f"Current Gen Best: {current_best_distance_in_gen:.2f}"
            )

            parents = self.tournament_selection(
                current_population, int(POPULATION_SIZE_VAL / 2)
            )
            offspring = []
            for i in range(0, len(parents) - 1, 2):
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child = self.ordered_crossover(parent1, parent2)
                offspring.append(child)

            for tour in offspring:
                self.mutate(tour, MUTATION_RATE_VAL)

            current_population.extend(offspring)
            current_population.sort(key=lambda tour: self.calculate_distance(tour))
            new_population = current_population[:POPULATION_SIZE_VAL]

            self.draw_cities()
            self.draw_path(
                current_best_tour_in_gen, color="blue", tag_suffix="_ga_current"
            )
            self.update()
            self.best_distances.append(current_best_distance_in_gen)
            self.progress_var.set(generation + 1)

            self.after(10, run_generation_step, generation + 1, new_population)

        run_generation_step(0, population)

    def initialize_pheromone(self, pheromone_init_val):
        num_cities = len(self.cities)
        if num_cities == 0:
            self.pheromone = np.array([[]])
            self.city_indices = {}
            return

        self.pheromone = np.full((num_cities, num_cities), pheromone_init_val)
        self.city_indices = {
            city: index for index, city in enumerate(self.cities.keys())
        }
        self.index_to_city = {index: city for city, index in self.city_indices.items()}

    def evaporate_pheromone(self, evaporation_rate_val):
        if hasattr(self, "pheromone") and self.pheromone.size > 0:
            self.pheromone *= 1.0 - evaporation_rate_val

    def ant_colony_tour(self, alpha_val, beta_val):
        cities_list = list(self.cities.keys())
        num_cities = len(cities_list)
        if num_cities == 0:
            return []

        tour = []
        current_city_name = random.choice(cities_list)
        tour.append(current_city_name)

        visited_indices = {self.city_indices[current_city_name]}

        while len(tour) < num_cities:
            current_city_idx = self.city_indices[current_city_name]
            probabilities = []
            available_next_cities_indices = []

            for next_city_idx in range(num_cities):
                if next_city_idx not in visited_indices:
                    next_city_name_candidate = self.index_to_city[next_city_idx]
                    dist = self.distance(current_city_name, next_city_name_candidate)
                    if dist == 0:
                        dist = 1e-6

                    pheromone_level = self.pheromone[current_city_idx][next_city_idx]
                    heuristic_info = 1.0 / dist

                    prob = (pheromone_level**alpha_val) * (heuristic_info**beta_val)
                    probabilities.append(prob)
                    available_next_cities_indices.append(next_city_idx)

            if not probabilities:
                break

            probabilities_sum = sum(probabilities)
            if probabilities_sum == 0:
                next_city_idx = random.choice(available_next_cities_indices)
            else:
                normalized_probabilities = [
                    p / probabilities_sum for p in probabilities
                ]
                next_city_idx = np.random.choice(
                    available_next_cities_indices, p=normalized_probabilities
                )

            next_city_name = self.index_to_city[next_city_idx]
            tour.append(next_city_name)
            visited_indices.add(next_city_idx)
            current_city_name = next_city_name

        return tour

    def run_ant_colony_optimization(self):
        if len(self.cities) < 2:
            messagebox.showinfo(
                "Not Enough Cities", "Please add at least 2 cities for ACO."
            )
            return

        self.running_algorithm = True
        self.disable_buttons_during_run()

        NUM_ANTS_VAL = self.num_ants_var.get()
        ACO_ITERATIONS_VAL = self.aco_iterations_var.get()
        PHEROMONE_INIT_VAL = self.pheromone_init_var.get()
        EVAPORATION_RATE_VAL = self.evaporation_rate_var.get()
        ALPHA_VAL = self.alpha_var.get()
        BETA_VAL = self.beta_var.get()

        self.initialize_pheromone(PHEROMONE_INIT_VAL)
        if not self.city_indices:
            self.enable_buttons_after_run()
            return

        self.best_distances = []
        overall_best_tour = []
        overall_best_distance = float("inf")

        self.progress_bar.config(maximum=ACO_ITERATIONS_VAL)
        self.progress_var.set(0)

        self.canvas.delete("path_blue")
        self.canvas.delete("path_green")
        self.draw_cities()

        def run_aco_iteration(iteration):
            nonlocal overall_best_tour, overall_best_distance
            if not self.running_algorithm:
                self.enable_buttons_after_run()
                if overall_best_tour:
                    self.best_tour_label.config(
                        text=f"Best Tour: {'-'.join(overall_best_tour)}"
                    )
                    self.distance_label.config(
                        text=f"Distance: {overall_best_distance:.2f}"
                    )
                return

            if iteration >= ACO_ITERATIONS_VAL:
                messagebox.showinfo(
                    "Ant Colony Optimization - Final Result",
                    f"Best Tour: {'-'.join(overall_best_tour)}\nDistance: {overall_best_distance:.2f}",
                )
                self.draw_cities()
                self.draw_path(
                    overall_best_tour, color="green", tag_suffix="_aco_final"
                )
                self.update()
                self.enable_buttons_after_run()
                self.plot_best_distances("ACO Best Distances over Iterations")
                return

            ants_tours = [
                self.ant_colony_tour(ALPHA_VAL, BETA_VAL) for _ in range(NUM_ANTS_VAL)
            ]
            ants_tours = [tour for tour in ants_tours if tour]

            if not ants_tours:
                self.after(10, run_aco_iteration, iteration + 1)
                return

            current_iter_best_tour = min(
                ants_tours, key=lambda tour: self.calculate_distance(tour)
            )
            current_iter_best_distance = self.calculate_distance(current_iter_best_tour)

            if current_iter_best_distance < overall_best_distance:
                overall_best_tour = current_iter_best_tour
                overall_best_distance = current_iter_best_distance

            self.evaporate_pheromone(EVAPORATION_RATE_VAL)
            for tour in ants_tours:
                if not tour:
                    continue
                tour_distance = self.calculate_distance(tour)
                if tour_distance == 0:
                    continue
                for i in range(len(tour) - 1):
                    city1_name = tour[i]
                    city2_name = tour[i + 1]
                    if (
                        city1_name in self.city_indices
                        and city2_name in self.city_indices
                    ):
                        idx1, idx2 = (
                            self.city_indices[city1_name],
                            self.city_indices[city2_name],
                        )
                        self.pheromone[idx1][idx2] += 1.0 / tour_distance
                        self.pheromone[idx2][idx1] += 1.0 / tour_distance

                if len(tour) > 1:
                    city_last_name, city_first_name = tour[-1], tour[0]
                    if (
                        city_last_name in self.city_indices
                        and city_first_name in self.city_indices
                    ):
                        idx_last, idx_first = (
                            self.city_indices[city_last_name],
                            self.city_indices[city_first_name],
                        )
                        self.pheromone[idx_last][idx_first] += 1.0 / tour_distance
                        self.pheromone[idx_first][idx_last] += 1.0 / tour_distance

            self.best_tour_label.config(
                text=f"Best Tour: {'-'.join(overall_best_tour)}"
            )
            self.distance_label.config(text=f"Distance: {overall_best_distance:.2f}")
            self.generation_label.config(
                text=f"Iteration: {iteration}/{ACO_ITERATIONS_VAL}"
            )
            self.current_distance_label.config(
                text=f"Current Iter Best: {current_iter_best_distance:.2f}"
            )

            self.draw_cities()
            self.draw_path(overall_best_tour, color="blue", tag_suffix="_aco_current")
            self.update()
            self.best_distances.append(overall_best_distance)
            self.progress_var.set(iteration + 1)

            self.after(10, run_aco_iteration, iteration + 1)

        run_aco_iteration(0)

    def plot_best_distances(self, title="Evolution of Best Tour Distance"):
        if not self.best_distances:
            messagebox.showinfo("No Data", "No distance data to plot.")
            return
        plt.figure()
        plt.plot(range(len(self.best_distances)), self.best_distances)
        plt.xlabel("Generation/Iteration")
        plt.ylabel("Best Distance")
        plt.title(title)
        plt.grid(True)
        plt.show()

    def opt2_heuristic(self, tour):
        if not tour or len(tour) < 4:
            return tour, self.calculate_distance(tour)

        num_cities = len(tour)
        current_best_tour = tour[:]
        best_distance = self.calculate_distance(current_best_tour)
        improved = True

        while improved:
            improved = False
            for i in range(1, num_cities - 2):
                for j in range(i + 1, num_cities - 1):
                    new_tour = (
                        current_best_tour[:i]
                        + current_best_tour[i : j + 1][::-1]
                        + current_best_tour[j + 1 :]
                    )

                    new_distance = self.calculate_distance(new_tour)
                    if new_distance < best_distance:
                        current_best_tour = new_tour
                        best_distance = new_distance
                        improved = True
            if not improved:
                for i in range(num_cities - 1):
                    for j in range(i + 2, num_cities):
                        pass

        return current_best_tour, best_distance

    def simulated_annealing(
        self, tour, initial_temperature, temperature_reduction_rate, max_iterations
    ):
        if not tour or len(tour) < 2:
            return tour, self.calculate_distance(tour)

        def acceptance_probability(new_distance, current_distance, temperature):
            if new_distance < current_distance:
                return 1.0
            elif temperature <= 1e-6:
                return 0.0
            else:
                return math.exp((current_distance - new_distance) / temperature)

        current_tour = tour[:]
        current_distance = self.calculate_distance(current_tour)

        best_tour = current_tour[:]
        best_distance = current_distance

        temperature = initial_temperature

        for _ in range(max_iterations):
            if temperature <= 1e-6:
                break

            new_tour_candidate = current_tour[:]

            if len(new_tour_candidate) >= 2:
                idx1, idx2 = random.sample(range(len(new_tour_candidate)), 2)
                new_tour_candidate[idx1], new_tour_candidate[idx2] = (
                    new_tour_candidate[idx2],
                    new_tour_candidate[idx1],
                )

            new_distance = self.calculate_distance(new_tour_candidate)

            if (
                acceptance_probability(new_distance, current_distance, temperature)
                > random.random()
            ):
                current_tour = new_tour_candidate[:]
                current_distance = new_distance

                if current_distance < best_distance:
                    best_tour = current_tour[:]
                    best_distance = current_distance

            temperature *= temperature_reduction_rate

        return best_tour, best_distance


if __name__ == "__main__":
    app = TSPGeneticAlgorithm()
    app.mainloop()
