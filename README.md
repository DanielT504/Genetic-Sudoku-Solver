# Genetic-Sudoku-Solver

This is a genetic algorithm that solves 9x9 sudoku grids using single-point crossover, adaptive mutation, elitism, and tournament selection. The fitness of each solution in the population is evaluated based on the number of unique numbers in each row, column, and 3x3 box. The higher the fitness value, the closer the solution is to a valid Sudoku grid, with a perfect grid at 9*27=243.

![sudoku](https://github.com/DanielT504/Genetic-Sudoku-Solver/assets/62156098/469fecd5-20bc-44e0-86a8-21d9810067fc)

Before starting the genetic algorithm, the "obvious" squares are filled out to lower the search space, which entails filling out any squares that only have one possible value, and any values that only have one possible square in a box.

The tournament child selection is done by randomly selecting a subset of individual candidates and picking the best, with elitism ensuring that the globally best solutions will survive whether picked for the tournament or not.
The single point crossover randomly selects a point in the array of unknown square values and trades the rightmost segment of that parent with an identically selection segment of another parent to form two children. 
I also used adaptive mutation, which starts out constant and increases up to a threshold after a certain number of generations without an improved best fitness.

These three processes are repeated over each generation, until the puzzle is solved, or gets stuck in a local optimum. The algorithm can solve most easy or medium puzzles within a reasonable time frame. However, the performance on hard puzzles with fewer clues may vary.
