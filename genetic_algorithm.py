import random
import heapq

class GeneticAlgorithm:
    def __init__(self, population_size=1000, max_generations=100000, mutation_rate=0.04, tournament_size=10, random_selection_portion=0.1, elitism_portion=0.1):
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.random_selection_portion = random_selection_portion
        self.elitism_portion = elitism_portion
        self.generations_without_improvement = 0
        self.best_fitness_so_far = float('-inf')

    def initialize_population(self, grid):
        population = []
        for _ in range(self.population_size):
            solution = self.generate_random_solution(grid)
            population.append(solution)
        return population

    def generate_random_solution(self, grid):
        solution = [[0] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    solution[i][j] = grid[i][j]
                else:
                    valid_numbers = self.get_valid_numbers(solution, i, j)
                    if valid_numbers:
                        solution[i][j] = random.choice(valid_numbers)
                    else:
                        
                        solution[i][j] = random.randint(1, 9)
        return solution

    def mutate(self, solution):
        mutated_solution = [row.copy() for row in solution]
        
        for i in range(9):
            if random.random() < self.mutation_rate:
                # Determine if we're swapping in a row, column, or box
                mutation_type = random.choice(['row', 'column', 'box'])
                
                if mutation_type == 'row':
                    # Swap two cells in this row
                    j1, j2 = random.sample(range(9), 2)
                    mutated_solution[i][j1], mutated_solution[i][j2] = mutated_solution[i][j2], mutated_solution[i][j1]
                    
                elif mutation_type == 'column':
                    # Swap two cells in this column
                    i1, i2 = random.sample(range(9), 2)
                    mutated_solution[i1][i], mutated_solution[i2][i] = mutated_solution[i2][i], mutated_solution[i1][i]
                    
                else:  # mutation_type == 'box'
                    # Swap two cells in this box
                    start_row, start_col = (i // 3) * 3, (i % 3) * 3
                    box_cells = [(start_row + r, start_col + c) for r in range(3) for c in range(3)]
                    (i1, j1), (i2, j2) = random.sample(box_cells, 2)
                    mutated_solution[i1][j1], mutated_solution[i2][j2] = mutated_solution[i2][j2], mutated_solution[i1][j1]
                    
        return mutated_solution

    def evolve_population(self, population):
        new_population = []

        # Select the fittest individuals to be passed onto the new population
        num_elitism = int(len(population) * self.elitism_portion)
        population_sorted_by_fitness = heapq.nlargest(num_elitism, population, key=self.evaluate_fitness)
        new_population.extend(population_sorted_by_fitness)

        num_random_selection = int((len(population) - num_elitism) * self.random_selection_portion)
        num_tournament_selection = len(population) - num_elitism - num_random_selection

        for _ in range(num_random_selection):
            new_population.append(random.choice(population))

        for _ in range(num_tournament_selection):
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            child = self.crossover(parent1, parent2)
            new_population.append(child)

        for i in range(len(new_population)):
            new_population[i] = self.mutate(new_population[i])
            
        best_solution = self.get_best_solution(new_population)
        best_fitness = self.evaluate_fitness(best_solution)
        if best_fitness > self.best_fitness_so_far:
            self.best_fitness_so_far = best_fitness
            self.generations_without_improvement = 0
        else:
            self.generations_without_improvement += 1

        if self.generations_without_improvement >= 50:  # 50 generations without improvement
            print("Starting local search...")  # Debugging line
            for i in range(9):
                for j in range(9):
                    current_fitness = self.evaluate_fitness(best_solution)
                    original_value = best_solution[i][j]
                    for num in range(1, 10):  # Try each possible value
                        best_solution[i][j] = num
                        if self.evaluate_fitness(best_solution) > current_fitness:  # If the fitness improved, keep the new value
                            print(f"Improved solution: {self.evaluate_fitness(best_solution)}")  # Debugging line
                            break  # Go to next cell
                        else:  # If the fitness didn't improve, revert the value
                            best_solution[i][j] = original_value

        if self.is_solved(best_solution):  # Check if the Sudoku is solved
            return [best_solution]  # return a population containing the single best solution

        return new_population  # return the population as is

    def is_solved(self, grid):
        # A solved Sudoku grid is a grid with fitness equal to zero (no conflict)
        return self.evaluate_fitness(grid) == 243
    
    def get_solved_solution(self, population):
        for solution in population:
            if self.is_solved(solution):
                return solution  # return the solution, not the population
        return None  # return None if no valid solution exists within the population

    def selection(self, population):
        # Tournament selection: Randomly select two individuals, and return the one with the higher fitness
        individual1 = random.choice(population)
        individual2 = random.choice(population)
        fitness1 = self.evaluate_fitness(individual1)
        fitness2 = self.evaluate_fitness(individual2)
        return individual1 if fitness1 > fitness2 else individual2

    def crossover(self, parent1, parent2):
        # Single-point crossover: Randomly select a crossover point and create a child by combining parent chromosomes
        crossover_point = random.randint(0, 8)
        child = []
        for i in range(9):
            if i < crossover_point:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def evaluate_fitness(self, solution):
        # Fitness evaluation: Count the number of unique values in each row, column, and 3x3 box
        fitness = 0
        for i in range(9):
            row_values = set(solution[i])
            column_values = set(solution[j][i] for j in range(9))
            box_values = set(
                solution[j][k]
                for j in range(i // 3 * 3, i // 3 * 3 + 3)
                for k in range(i % 3 * 3, i % 3 * 3 + 3)
            )
            fitness += len(row_values) + len(column_values) + len(box_values)
        return fitness

    def get_best_solution(self, population):
        best_fitness = float('-inf')
        best_solution = None
        for solution in population:
            fitness = self.evaluate_fitness(solution)
            if fitness > best_fitness:
                best_fitness = fitness
                best_solution = solution
        return best_solution

    def get_valid_numbers(self, grid, row, col):
        valid_numbers = set(range(1, 10))
        
        # Remove conflicting values in the same row
        for j in range(9):
            valid_numbers.discard(grid[row][j])

        # Remove conflicting values in the same column
        for i in range(9):
            valid_numbers.discard(grid[i][col])

        # Remove conflicting values in the same 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                valid_numbers.discard(grid[i][j])
        
        return list(valid_numbers)
    
    def tournament_selection(self, population):
        # Choose a random number of individuals from the population
        tournament = random.sample(population, self.tournament_size)
        
        # Return the best individual among the chosen
        return self.get_best_solution(tournament)