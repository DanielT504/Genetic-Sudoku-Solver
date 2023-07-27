import tkinter as tk

from genetic_algorithm import GeneticAlgorithm

# Create a Sudoku UI class
class SudokuUI:
    def __init__(self, grid_file):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")

        # Load the grid from the file
        self.grid = self.load_grid(grid_file)
        
        self.iteration = 0  # Initialize the iteration count

        # Create the UI elements
        self.create_ui()

        # Flag to track if the button was clicked
        self.button_clicked = False

    def load_grid(self, grid_file):
        grid = []
        with open(grid_file, 'r') as file:
            for line in file:
                row = [int(num) for num in line.strip().split()]
                grid.append(row)
        return grid

    def create_ui(self):
        # Create a 9x9 grid of Entry widgets for displaying the Sudoku grid
        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 16, 'bold'), justify='center')
                entry.grid(row=i, column=j, sticky='nsew')
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Populate the grid with initial values
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].config(state='readonly')

        # Set the row and column weights to evenly distribute the cells within the grid
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        # Add a button to fill in obvious squares
        solve_button = tk.Button(self.root, text="Fill in obvious squares", command=self.fill_obvious_squares_button_clicked)
        solve_button.grid(row=9, columnspan=9)

    def fill_obvious_squares_button_clicked(self):
        print("Filling in")
        if not self.button_clicked:
            self.fill_obvious_squares()
            self.button_clicked = True
            solve_button = self.root.grid_slaves(row=9)[0]
            solve_button.grid_forget()
            
    def fill_obvious_squares(self):
        squares_filled = True
        while squares_filled:
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
                            squares_filled = True
                            self.root.after(100, self.fill_obvious_squares)  # Schedule the next iteration after a delay
                            return

            if not squares_filled:
                self.root.after(0, self.run_after_no_changes)  # Schedule the code block after a delay
                return
            
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

        genetic_solver = GeneticAlgorithm()
        population = genetic_solver.initialize_population(self.grid)
        for generation in range(genetic_solver.max_generations):
            best_solution = genetic_solver.get_best_solution(population)
            best_fitness = genetic_solver.evaluate_fitness(best_solution)
            print(f"Generation {generation+1}: Best Fitness: {best_fitness}")

            # Display solution and then pause for 0.5 seconds
            self.display_solution(best_solution)
            #self.root.after(500) # Wait for 500 ms (0.5 seconds)

            population = genetic_solver.evolve_population(population)
            self.root.update_idletasks() # Update the UI to show the current solution
            
    def display_solution(self, solution):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(solution[i][j]))

    def calculate_pencil_marks(self, row, col):
        pencil_marks = set(range(1, 10))  # Initialize with all possible values

        # Remove conflicting values in the same row
        for j in range(9):
            if self.grid[row][j] != 0:
                pencil_marks.discard(self.grid[row][j])

        # Remove conflicting values in the same column
        for i in range(9):
            if self.grid[i][col] != 0:
                pencil_marks.discard(self.grid[i][col])

        # Remove conflicting values in the same 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] != 0:
                    pencil_marks.discard(self.grid[i][j])
        return pencil_marks

    def run(self):
        self.root.mainloop()


# Create an instance of SudokuUI and run the program
if __name__ == '__main__':
    grid_file = 'sudoku_grid_easy.txt'  # Replace with the actual file path
    sudoku_ui = SudokuUI(grid_file)
    sudoku_ui.run()
