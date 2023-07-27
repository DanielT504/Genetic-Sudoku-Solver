import random

class GeneticAlgorithm:
    def __init__(self, population_size=100, max_generations=1000, mutation_rate=0.05, tournament_size=10, random_selection_portion=0.1):
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.random_selection_portion = random_selection_portion

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
                        # if no valid numbers, leave it as 0, 
                        # the mutation function in the next generation might find a valid number
                        solution[i][j] = 0
        return solution

    def mutate(self, solution):
        mutated_solution = [row.copy() for row in solution]
        for i in range(9):
            for j in range(9):
                if random.random() < self.mutation_rate:
                    mutated_solution[i][j] = random.randint(1, 9)
        return mutated_solution

    def evolve_population(self, population):
        new_population = []
        num_random_selection = int(len(population) * self.random_selection_portion)
        num_tournament_selection = len(population) - num_random_selection

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
        if self.is_solved(best_solution):  # Check if the Sudoku is solved
            return best_solution
        
        return new_population

    def is_solved(self, grid):
        # A solved Sudoku grid is a grid with fitness equal to zero (no conflict)
        return self.evaluate_fitness(grid) == 0

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