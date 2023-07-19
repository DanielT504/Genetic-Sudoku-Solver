import random

class GeneticAlgorithm:
    def __init__(self, population_size=100, max_generations=1000, mutation_rate=0.1):
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate

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
                    solution[i][j] = random.randint(1, 9)
        return solution

    def evolve_population(self, population):
        for generation in range(self.max_generations):
            new_population = []
            for _ in range(self.population_size):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            best_solution = self.get_best_solution(new_population)
            best_fitness = self.evaluate_fitness(best_solution)
            print(f"Generation {generation+1}: Best Fitness: {best_fitness}")
            population = new_population
        return population

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

    def mutate(self, solution):
        # Mutation: Randomly select a gene and replace it with a random value
        mutated_solution = solution.copy()
        for i in range(9):
            if random.random() < self.mutation_rate:
                mutated_solution[i] = random.randint(1, 9)
        return mutated_solution

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
