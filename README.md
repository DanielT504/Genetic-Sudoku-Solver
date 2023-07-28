# Genetic-Sudoku-Solver

The application starts by initializing a population of Sudoku grids with random numbers in the unsolved spaces, while keeping the pre-filled cells constant as per the input puzzle. Fitness of each solution in the population is evaluated based on the number of unique numbers in each row, column and block. The higher the fitness value, the closer the solution is to a valid Sudoku grid.

Three main genetic operations are performed on the population:

1. **Selection** : A combination of elitism, tournament and random selection are used to choose individuals for creating the next generation. Elitism ensures the best solutions are carried over to the next generation. Tournament selection introduces competition amongst a randomly selected subset of individuals, and the best amongst this subset is chosen. Random selection introduces diversity in the population.
2. **Crossover** : For every pair of parents selected, a new child solution is created by mixing the genes of the parents. This is done by randomly splitting the parent grids at certain points and combining the parts to form the child grid.
3. **Mutation** : Each child solution is subjected to mutation, where a certain number of cells are randomly selected and their values are changed. This introduces randomness and helps the algorithm explore the solution space more widely.

The process of selection, crossover, and mutation is repeated over a specified number of generations. The best solution from the final generation is returned as the solved Sudoku grid. The algorithm can solve most easy to medium difficulty puzzles within a reasonable time frame. However, the performance on hard puzzles with fewer clues may vary.
