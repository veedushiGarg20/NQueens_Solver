# N-Queens Problem Solver

This Python GUI is built using `tkinter` to visualize how backtracking algorithm works to solve the N-Queens puzzle. You can place queens on the board, see valid moves, and even get help from an AI to solve it.


## Features
- **Interactive board**: Place queens manually and watch the board update in real-time.
- **Heuristic updates**: Display attacking pair of queens after every move (lesser pairs = better!).
- **Valid moves**: Highlights safe cells for next queen moves.
- **AI solver:** Take help from AI to solve the puzzle if you get stuck.
- **Undo button**: Go back a step if you want to try a different move.

## Requirements
- **Python 3.6** (with `tkinter` support)
- No additional libraries needed (pure python!).

## How It Works

1. Start by entering the number of queens you want to solve for.
2. Click on a cell on the board to place the queen (the app will show you safe and danger cells).
3. See valid cells after every move, undo your last step, or let the AI handle it!
