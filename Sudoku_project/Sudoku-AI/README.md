# Sudoku AI Using First-Order Predicate Calculus

## Overview

This project implements a 9 × 9 Sudoku solver and interactive game using Python, the Z3 SMT solver, and `ipywidgets`.

The objective is to fill the Sudoku grid with digits from 1 to 9 so that each digit appears exactly once in every row, every column, and every 3 × 3 box, while preserving the original puzzle clues.

## Objectives

- Represent digit placement using the predicate `Val(r, c, d)`.
- Express Sudoku rules as logical constraints using Z3.
- Use quantified constraints to model cell and row/column requirements.
- Enforce the 3 × 3 box rules and preserve the original puzzle clues.
- Find a satisfying assignment using the Z3 SMT solver.
- Provide an interactive Sudoku board in a notebook environment.
- Allow users to select empty cells and enter numbers.
- Check answers for duplicate values in rows, columns, and 3 × 3 boxes.
- Provide **Solve with AI**, **Get Hint**, and **Reset Game** controls.
- Validate the solution and verify that all original clues are preserved.

## Technologies Used

- Python 3
- Z3 SMT Solver (`z3-solver`)
- `ipywidgets`
- IPython display tools
- First-Order Predicate Calculus / logical constraint modelling

## Project Structure

- `Math_Project_Sudoku.ipynb` — complete notebook containing the solver, interactive Sudoku game, and validation tests.
- `sudoku_ai.py` — Python source export of the notebook's code cells.
- `README.md` — project overview and instructions.

## Installation

### Run in Google Colab

1. Upload `Math_Project_Sudoku.ipynb` to Google Colab, or open the notebook from your GitHub repository.
2. Run the notebook cells from top to bottom.
3. The notebook installs the required packages in its setup cell.
4. Use the interactive Sudoku board after the interface appears.

### Run locally in Jupyter

1. Install Python 3.
2. Install the required packages:

   ```bash
   python -m pip install z3-solver ipywidgets
   ```

3. Open `Math_Project_Sudoku.ipynb` in Jupyter Notebook or JupyterLab.
4. Run the cells from top to bottom.

> **Note:** The full interactive interface is designed for Google Colab or a Jupyter environment with `ipywidgets` support. The notebook is the recommended way to run the complete project.

## How to Use the Game

1. Select an empty cell on the Sudoku board.
2. Choose a number from the number pad.
3. Click **Check Answers** to check for conflicts and determine whether the puzzle is complete and correct.
4. Click **Get Hint** to fill one empty cell with its solution value.
5. Click **Solve with AI** to display the Z3 solver's solution.
6. Click **Reset Game** to restore the original puzzle.

The original clue cells are locked and cannot be edited through the interface.

## Logical Model

The predicate `Val(r, c, d)` means that cell `(r, c)` contains digit `d`.

The solver encodes these rules:

1. **Cell rule:** Every cell contains exactly one digit from 1 to 9.
2. **Row rule:** Every digit from 1 to 9 appears exactly once in each row.
3. **Column rule:** Every digit from 1 to 9 appears exactly once in each column.
4. **Box rule:** Every digit from 1 to 9 appears exactly once in each 3 × 3 box.
5. **Clue rule:** Every non-zero value in the original puzzle is preserved.

Z3 checks whether the constraints are satisfiable and returns a model representing a completed Sudoku grid.

## Validation and Testing

The notebook includes validation checks to confirm that:

- The solver finds a solution for the provided puzzle.
- Each row contains the digits 1 through 9 exactly once.
- Each column contains the digits 1 through 9 exactly once.
- Each 3 × 3 box contains the digits 1 through 9 exactly once.
- All original puzzle clues remain unchanged.

The included notebook output reports that the validation tests passed for the provided puzzle.


