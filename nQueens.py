import tkinter as tk
from tkinter import messagebox

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Problem Solver")

        # Frame to input number of queens
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Enter number of queens: ").pack(side=tk.LEFT)
        self.n_input = tk.Entry(self.frame)
        self.n_input.pack(side=tk.LEFT)
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.start_game)
        self.submit_button.pack(side=tk.LEFT)

        # Variables to track game state
        self.n = 0
        self.move_history = []
        self.board_canvas = None
        self.heuristic_value = 0

        # Placeholders for the GUI elements
        self.instruction_label = None
        self.go_back_button = None
        self.next_moves_button = None
        self.ai_solve_button = None

    def start_game(self):
        try:
            self.n = int(self.n_input.get())
            if self.n <= 0:
                raise ValueError
            self.move_history = []
            self.heuristic_value = 0
            self.reset_gui()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of queens")

    def reset_gui(self):
        # Clear previous widgets except the input frame
        for widget in self.root.winfo_children():
            if widget != self.frame:
                widget.destroy()

        # Instruction display
        self.instruction_label = tk.Label(self.root, text="Choose the cell with the least heuristic value")
        self.instruction_label.pack(pady=10)

        # Create the board
        self.create_board()

        # Create button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Show buttons
        self.go_back_button = tk.Button(button_frame, text="Go Back", command=self.go_back)
        self.go_back_button.pack(side=tk.LEFT, padx=5)

        self.next_moves_button = tk.Button(button_frame, text="Show Next Moves", command=self.show_next_moves)
        self.next_moves_button.pack(side=tk.LEFT, padx=5)

        self.ai_solve_button = tk.Button(button_frame, text="AI Solve", command=self.ai_solve)
        self.ai_solve_button.pack(side=tk.LEFT, padx=5)

    def create_board(self):
        # Create a new canvas for the current board state
        self.board_canvas = tk.Canvas(self.root, width=400, height=400)
        self.board_canvas.pack(padx=10, pady=20)

        # Draw the grid and queens
        self.draw_grid()

    def draw_grid(self):
        cell_size = 400 // self.n
        for i in range(self.n):
            for j in range(self.n):
                self.board_canvas.create_rectangle(i * cell_size, j * cell_size,
                                                    (i + 1) * cell_size, (j + 1) * cell_size)

        # Calculate and display heuristic values for each cell
        heuristic_values = self.calculate_heuristic_values()
        for (x, y), value in heuristic_values.items():
            self.board_canvas.create_text(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2, text=str(value))

        # Draw queens
        for x, y in self.move_history:
            self.draw_queen(x, y)

    def draw_queen(self, x, y):
        cell_size = 400 // self.n
        x0, y0 = x * cell_size, y * cell_size
        x1, y1 = (x + 1) * cell_size, (y + 1) * cell_size
        self.board_canvas.create_oval(x0, y0, x1, y1, fill="red")

    def show_next_moves(self):
        moves = self.get_next_moves()
        if moves:
            cell_size = 400 // self.n
            for x, y in moves:
                self.board_canvas.create_rectangle(x * cell_size, y * cell_size,
                                                    (x + 1) * cell_size, (y + 1) * cell_size,
                                                    outline="green", width=3)
            self.board_canvas.bind("<Button-1>", lambda event: self.handle_click(event, moves))
        else:
            messagebox.showinfo("Game Over", "No valid moves available!")

    def handle_click(self, event, moves):
        x = event.x // (400 // self.n)
        y = event.y // (400 // self.n)

        if (x, y) in moves:
            self.move_history.append((x, y))
            self.update_heuristic()  # Update heuristic after making a move
            self.reset_gui()
            self.check_goal_state()
        else:
            messagebox.showerror("Invalid Move", "Queens under attack! Pick another move.")

    def get_next_moves(self):
        return [(x, y) for x in range(self.n) for y in range(self.n) if self.is_valid_move(x, y)]

    def is_valid_move(self, x, y):
        return all(qx != x and qy != y and abs(qx - x) != abs(qy - y) for qx, qy in self.move_history)

    def update_heuristic(self):
        attacking_pairs = 0
        for i in range(len(self.move_history) - 1):
            queen1 = self.move_history[i]
            for j in range(i + 1, len(self.move_history)):
                queen2 = self.move_history[j]
                if self.is_attacking(queen1, queen2):
                    attacking_pairs += 1
        self.heuristic_value = attacking_pairs
        print(f"Heuristic Value: {self.heuristic_value}")  # Debugging statement

    def is_attacking(self, queen1, queen2):
        x1, y1 = queen1
        x2, y2 = queen2
        return x1 == x2 or y1 == y2 or abs(x1 - x2) == abs(y1 - y2)

    def calculate_heuristic_values(self):
        heuristic_values = {}
        for x in range(self.n):
            for y in range(self.n):
                if (x, y) not in self.move_history:
                    temp_move_history = self.move_history + [(x, y)]
                    attacking_pairs = 0
                    for i in range(len(temp_move_history) - 1):
                        queen1 = temp_move_history[i]
                        for j in range(i + 1, len(temp_move_history)):
                            queen2 = temp_move_history[j]
                            if self.is_attacking(queen1, queen2):
                                attacking_pairs += 1
                    heuristic_values[(x, y)] = attacking_pairs
        return heuristic_values

    def go_back(self):
        if self.move_history:
            self.move_history.pop()
            self.update_heuristic()  # Update heuristic after going back a move
            self.reset_gui()
        else:
            messagebox.showinfo("Information", "No previous moves to go back to.")

    def check_goal_state(self):
        if len(self.move_history) == self.n and self.heuristic_value == 0:
            messagebox.showinfo("Congratulations!", f"Successfully solved the {self.n}-Queens problem!")

    def ai_solve(self):
        if self.solve_n_queens(len(self.move_history)):
            self.reset_gui()
            messagebox.showinfo("AI Solved", f"The AI has solved the {self.n}-Queens problem!")
        else:
            messagebox.showinfo("AI Failed", "The AI could not solve the problem from the current state.")
            self.reset_gui()  # Reset the GUI to allow manual interaction

    def solve_n_queens(self, row):
        if row == self.n:
            return True

        for col in range(self.n):
            if self.is_valid_move(row, col):
                self.move_history.append((row, col))
                if self.solve_n_queens(row + 1):
                    return True
                self.move_history.pop()

        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
