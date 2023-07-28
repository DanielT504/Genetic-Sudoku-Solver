import time
import tkinter as tk

from genetic_algorithm import GeneticAlgorithm

# Create a Sudoku UI class
class SudokuUI:
    def __init__(self, grid_file):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.grid = self.load_grid(grid_file)
        self.iteration = 0
        self.create_ui()
        self.button_clicked = False

    def load_grid(self, grid_file):
        grid = []
        with open(grid_file, 'r') as file:
            for line in file:
                row = [int(num) for num in line.strip().split()]
                grid.append(row)
        return grid

    def create_ui(self):
        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 16, 'bold'), justify='center')
                entry.grid(row=i, column=j, sticky='nsew')
                row_entries.append(entry)
            self.entries.append(row_entries)

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].config(state='readonly')

        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        solve_button = tk.Button(self.root, text="Fill in obvious squares", command=self.fill_obvious_squares_button_clicked)
        solve_button.grid(row=9, columnspan=9)

    def fill_obvious_squares_button_clicked(self):
        print("Filling in")
        solve_button = self.root.grid_slaves(row=9)[0]
        solve_button.grid_forget()
        self.fill_obvious_squares()
            
    def fill_obvious_squares(self):
        while True:
            squares_filled = False
            for i in range(9):
                for j in range(9):
                    if self.grid[i][j] == 0:
                        pencil_marks = self.calculate_pencil_marks(i, j)
                        if len(pencil_marks) == 1:
                            value = pencil_marks.pop()
                            self.grid[i][j] = value
                            self.entries[i][j].delete(0, tk.END)
                            self.entries[i][j].insert(0, str(value))
                            self.root.update()
                            squares_filled = True
                            time.sleep(0.1)  # delay of 100ms
            if not squares_filled:
                self.run_after_no_changes()
                break
            
    def run_after_no_changes(self):
        print("No more obvious squares")
        
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.entries[i][j].config(state='readonly')
        
        solve_genetic_button = tk.Button(self.root, text="Solve with genetic algorithm", command=self.solve_with_genetic_algorithm)
        solve_genetic_button.grid(row=9, columnspan=9)
        
    def solve_with_genetic_algorithm(self):
        print("Solving")

        solve_genetic_button = self.root.grid_slaves(row=9)[0]
        solve_genetic_button.grid_forget()

        genetic_solver = GeneticAlgorithm()
        population = genetic_solver.initialize_population(self.grid)
        for generation in range(genetic_solver.max_generations):
            best_solution = genetic_solver.get_best_solution(population)
            best_fitness = genetic_solver.evaluate_fitness(best_solution)
            print(f"Generation {generation+1}: Best Fitness: {best_fitness}/243")
            self.display_solution(best_solution)

            population = genetic_solver.evolve_population(population)
            
            # check if a solution is found in the population
            solved_solution = genetic_solver.get_solved_solution(population)
            if solved_solution is not None:
                print("Solution found!")
                self.display_solution(solved_solution)
                return

            self.root.update_idletasks() # update the UI
            
    def display_solution(self, solution):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(solution[i][j]))

    def calculate_pencil_marks(self, row, col):
        pencil_marks = set(range(1, 10))  # initialize with all possible values

        # remove conflicting values in the same row
        for j in range(9):
            if self.grid[row][j] != 0:
                pencil_marks.discard(self.grid[row][j])

        # remove conflicting values in the same column
        for i in range(9):
            if self.grid[i][col] != 0:
                pencil_marks.discard(self.grid[i][col])

        # remove conflicting values in the same 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] != 0:
                    pencil_marks.discard(self.grid[i][j])
        return pencil_marks

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    print("\n\nGenetic Sudoku Solver")
    grid_file = 'sudoku_grid.txt'
    sudoku_ui = SudokuUI(grid_file)
    sudoku_ui.run()
