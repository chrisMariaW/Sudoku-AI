# Sudoku AI

A Sudoku solver and interactive Sudoku game built with Python, Z3, and `ipywidgets`.

## Features

- Solves Sudoku using Z3 constraint solving and the predicate `Val(r, c, d)`.
- Models Sudoku rules for cells, rows, columns, and 3×3 boxes.
- Provides an interactive 9×9 board.
- Lets players select cells and enter numbers.
- Checks answers for row, column, and 3×3-box conflicts.
- Includes **Solve with AI**, **Get Hint**, and **Reset Game** controls.
- Validates the computed solution and confirms that the original clues are preserved.

## Files

- `Math_Project_Sudoku.ipynb` — original runnable Google Colab/Jupyter notebook, including the interactive game and validation tests.
- `sudoku_ai.py` — Python source export of the notebook's code cells. The interactive interface is designed to run in a notebook environment.
- `README.md` — project overview and setup instructions.

## Run in Google Colab

1. Upload `Math_Project_Sudoku.ipynb` to Google Colab, or open it from your GitHub repository.
2. Run the notebook cells from top to bottom.
3. The first cell installs the required packages. If prompted, allow the installation to finish before continuing.
4. Use the interactive board to select an empty cell, choose a number, and use the game controls.

## Run locally in Jupyter

Install the dependencies:

```bash
python -m pip install z3-solver ipywidgets
```

Then open `Math_Project_Sudoku.ipynb` in Jupyter Notebook or JupyterLab and run the cells from top to bottom.

> The interactive controls require a notebook environment with `ipywidgets` support. The `.py` file is provided as a source-code export; the notebook is the recommended way to run the full interactive game.

## Solver approach

The solver represents the statement “cell `(r, c)` contains digit `d`” with the Boolean predicate `Val(r, c, d)`. Z3 constraints encode the Sudoku rules and the original puzzle clues, then the solver searches for a satisfying assignment.

## Dependencies

- Python 3
- `z3-solver`
- `ipywidgets`
- IPython (available in Google Colab and Jupyter environments)
