# Install dependencies in a terminal or notebook:
# pip install z3-solver ipywidgets


from z3 import (
    Function, IntSort, BoolSort, Bool, Solver,
    ForAll, Implies, And, Sum, If, sat
)


# DEFINE THE PUZZLE

PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


# PREDICATE: Val(r, c, d)
# Meaning: cell (r, c) contains digit d.


Val = Function(
    "Val",
    IntSort(), IntSort(), IntSort(),
    BoolSort()
)


def solve_sudoku(board):
    solver = Solver()

    # Logical variables for universal quantification
    r, c, d = IntSort().cast(0), IntSort().cast(0), IntSort().cast(0)

    from z3 import Int
    r = Int("r")
    c = Int("c")
    d = Int("d")


    # RULE 1: Every cell contains exactly one digit 1-9.
    # For all r,c in the grid:
    # exactly one Val(r,c,d) is true.


    cell_digit_count = Sum([
        If(Val(r, c, digit), 1, 0)
        for digit in range(1, 10)
    ])

    solver.add(
        ForAll(
            [r, c],
            Implies(
                And(r >= 0, r < 9, c >= 0, c < 9),
                cell_digit_count == 1
            )
        )
    )


    # RULE 2: Each digit occurs exactly once in each row.
    # For every row r and digit d, exactly one column
    # contains that digit.


    row_count = Sum([
        If(Val(r, column, d), 1, 0)
        for column in range(9)
    ])

    solver.add(
        ForAll(
            [r, d],
            Implies(
                And(r >= 0, r < 9, d >= 1, d <= 9),
                row_count == 1
            )
        )
    )


    # RULE 3: Each digit occurs exactly once in each column.


    column_count = Sum([
        If(Val(row, c, d), 1, 0)
        for row in range(9)
    ])

    solver.add(
        ForAll(
            [c, d],
            Implies(
                And(c >= 0, c < 9, d >= 1, d <= 9),
                column_count == 1
            )
        )
    )


    # RULE 4: Each digit occurs exactly once in each 3x3 box.
    # The nine boxes are explicitly enumerated.

    for box_r in range(0, 9, 3):
        for box_c in range(0, 9, 3):
            for digit in range(1, 10):

                box_count = Sum([
                    If(Val(rr, cc, digit), 1, 0)
                    for rr in range(box_r, box_r + 3)
                    for cc in range(box_c, box_c + 3)
                ])

                solver.add(box_count == 1)


    # RULE 5: Original clues are facts in the knowledge base.
    # Example: if board[0][0] == 5, assert Val(0,0,5).


    for row in range(9):
        for column in range(9):
            given = board[row][column]

            if given != 0:
                solver.add(Val(row, column, given))


    # INFERENCE: Find an assignment satisfying all rules.


    if solver.check() == sat:
        model = solver.model()
        result = []

        for row in range(9):
            result_row = []

            for column in range(9):
                value_found = None

                for digit in range(1, 10):
                    if model.evaluate(
                        Val(row, column, digit),
                        model_completion=True
                    ) == True:
                        value_found = digit
                        break

                result_row.append(value_found)

            result.append(result_row)

        return result

    return None



# TEST THE PREDICATE-CALCULUS-BASED SUDOKU SOLVER


solution = solve_sudoku(PUZZLE)

if solution is not None:
    print("Sudoku solved using Val(r,c,d) and quantified constraints!")
    print("\nSolved Sudoku:")

    for row in solution:
        print(row)
else:
    print("No valid solution exists.")

import ipywidgets as widgets
from IPython.display import display, HTML
import copy
import random

# Keep the original puzzle and the current game board
original_puzzle = copy.deepcopy(PUZZLE)
current_board = copy.deepcopy(PUZZLE)
selected_cell = [None]

#GAME MESSAGE
message = widgets.HTML(
    value="<span style='color:#475569;font-weight:bold'>"
          "Select an empty cell, then choose a number.</span>"
)

#  SUDOKU GRID
cells = []

for r in range(9):
    row = []

    for c in range(9):
        value = current_board[r][c]

        cell = widgets.Button(
            description=str(value) if value else "",
            disabled=(value != 0),
            layout=widgets.Layout(
                width="48px",
                height="48px",
                min_width="48px",
                padding="0px",
                margin="1px",
                border="1px solid #94A3B8"
            ),
            style={
                "button_color": "#CBD5E1" if value else "#FFFFFF",
                "font_weight": "bold",
                "font_size": "18px",
                "text_color": "#172554"
            }
        )

        row.append(cell)

    cells.append(row)


#  SELECT A CELL
def select_cell(button, r, c):
    if original_puzzle[r][c] != 0:
        message.value = (
            "<span style='color:#475569;font-weight:bold'>"
            "This is an original clue and cannot be changed.</span>"
        )
        return

    selected_cell[0] = (r, c)

    # Highlight the selected empty cell
    for rr in range(9):
        for cc in range(9):
            if original_puzzle[rr][cc] == 0:
                if (rr, cc) == (r, c):
                    cells[rr][cc].style.button_color = "#C4B5FD"
                elif current_board[rr][cc] == 0:
                    cells[rr][cc].style.button_color = "#FFFFFF"
                else:
                    cells[rr][cc].style.button_color = "#EDE9FE"

    message.value = (
        f"<span style='color:#4338CA;font-weight:bold'>"
        f"Selected row {r+1}, column {c+1}. Choose a number below.</span>"
    )


# Connect each cell to its position
for r in range(9):
    for c in range(9):
        cells[r][c].on_click(
            lambda button, r=r, c=c: select_cell(button, r, c)
        )


#  DISPLAY GRID WITH BOX BORDERS
board_rows = []

for r in range(9):
    row_cells = []

    for c in range(9):
        # Wrapper creates thicker boundaries around each 3x3 box
        borders = []
        if c % 3 == 0:
            borders.append("border-left: 3px solid #334155")
        if r % 3 == 0:
            borders.append("border-top: 3px solid #334155")
        if c == 8:
            borders.append("border-right: 3px solid #334155")
        if r == 8:
            borders.append("border-bottom: 3px solid #334155")

        wrapper = widgets.Box(
            [cells[r][c]],
            layout=widgets.Layout(
                padding="0px",
                border="0px",
                width="50px",
                height="50px"
            )
        )

        # Store border information for the CSS grid
        row_cells.append(wrapper)

    board_rows.append(
        widgets.HBox(
            row_cells,
            layout=widgets.Layout(
                justify_content="center",
                margin="0px",
                padding="0px"
            )
        )
    )

board_widget = widgets.VBox(
    board_rows,
    layout=widgets.Layout(
        align_items="center",
        margin="10px auto"
    )
)


#  NUMBER PAD
number_buttons = []

def enter_number(button, number):
    if selected_cell[0] is None:
        message.value = (
            "<span style='color:#B45309;font-weight:bold'>"
            "Please select an empty cell first.</span>"
        )
        return

    r, c = selected_cell[0]

    current_board[r][c] = number
    cells[r][c].description = str(number)
    cells[r][c].style.button_color = "#EDE9FE"

    selected_cell[0] = None

    message.value = (
        f"<span style='color:#166534;font-weight:bold'>"
        f"Entered {number} at row {r+1}, column {c+1}.</span>"
    )


for number in range(1, 10):
    button = widgets.Button(
        description=str(number),
        layout=widgets.Layout(
            width="42px",
            height="42px",
            margin="3px"
        ),
        style={
            "button_color": "#E0E7FF",
            "font_weight": "bold",
            "font_size": "16px",
            "text_color": "#1E3A8A"
        }
    )

    button.on_click(
        lambda b, n=number: enter_number(b, n)
    )

    number_buttons.append(button)


# CHECK ANSWERS
def check_answers(button):
    current = copy.deepcopy(current_board)

    for r in range(9):
        for c in range(9):
            value = current[r][c]

            if value == 0:
                continue

            # Check row
            for k in range(9):
                if k != c and current[r][k] == value:
                    message.value = (
                        f"<span style='color:#DC2626;font-weight:bold'>"
                        f"Duplicate {value} in row {r+1}.</span>"
                    )
                    return

            # Check column
            for k in range(9):
                if k != r and current[k][c] == value:
                    message.value = (
                        f"<span style='color:#DC2626;font-weight:bold'>"
                        f"Duplicate {value} in column {c+1}.</span>"
                    )
                    return

            # Check 3x3 box
            box_r = (r // 3) * 3
            box_c = (c // 3) * 3

            for rr in range(box_r, box_r + 3):
                for cc in range(box_c, box_c + 3):
                    if (rr, cc) != (r, c) and current[rr][cc] == value:
                        message.value = (
                            "<span style='color:#DC2626;font-weight:bold'>"
                            "Duplicate number in a 3x3 box.</span>"
                        )
                        return

    if any(0 in row for row in current):
        message.value = (
            "<span style='color:#B45309;font-weight:bold'>"
            "No conflicts found so far. Keep going!</span>"
        )
    elif current == solution:
        message.value = (
            "<span style='color:#15803D;font-size:18px;font-weight:bold'>"
            "Congratulations! You solved Sudoku! 🎉</span>"
        )
    else:
        message.value = (
            "<span style='color:#DC2626;font-weight:bold'>"
            "The board is full, but some answers are incorrect.</span>"
        )


# SOLVE WITH Z3 AI
def solve_game(button):
    answer = solve_sudoku(original_puzzle)

    if answer is None:
        message.value = (
            "<span style='color:#DC2626'>No valid solution exists.</span>"
        )
        return

    for r in range(9):
        for c in range(9):
            current_board[r][c] = answer[r][c]
            cells[r][c].description = str(answer[r][c])

            if original_puzzle[r][c] == 0:
                cells[r][c].style.button_color = "#DCFCE7"

    selected_cell[0] = None

    message.value = (
        "<span style='color:#15803D;font-size:18px;font-weight:bold'>"
        "Z3 AI solved the Sudoku successfully! 🤖</span>"
    )


# GET A HINT
def give_hint(button):
    empty_cells = [
        (r, c)
        for r in range(9)
        for c in range(9)
        if current_board[r][c] == 0
    ]

    if not empty_cells:
        message.value = "There are no empty cells remaining!"
        return

    r, c = random.choice(empty_cells)
    current_board[r][c] = solution[r][c]
    cells[r][c].description = str(solution[r][c])
    cells[r][c].style.button_color = "#FEF3C7"
    selected_cell[0] = None

    message.value = (
        f"<span style='color:#92400E;font-weight:bold'>"
        f"Hint: row {r+1}, column {c+1} contains {solution[r][c]}.</span>"
    )


# RESET GAME
def reset_game(button):
    for r in range(9):
        for c in range(9):
            current_board[r][c] = original_puzzle[r][c]

            cells[r][c].description = (
                str(original_puzzle[r][c])
                if original_puzzle[r][c] != 0 else ""
            )

            cells[r][c].disabled = (original_puzzle[r][c] != 0)

            cells[r][c].style.button_color = (
                "#CBD5E1" if original_puzzle[r][c] != 0
                else "#FFFFFF"
            )

    selected_cell[0] = None
    message.value = (
        "<span style='color:#475569;font-weight:bold'>"
        "Game reset. Try again!</span>"
    )


#  GAME BUTTONS
check_button = widgets.Button(
    description="Check Answers",
    button_style="info",
    icon="check"
)

solve_button = widgets.Button(
    description="Solve with AI",
    button_style="success",
    icon="lightbulb"
)

hint_button = widgets.Button(
    description="Get Hint",
    button_style="warning",
    icon="question"
)

reset_button = widgets.Button(
    description="Reset Game",
    icon="refresh"
)

check_button.on_click(check_answers)
solve_button.on_click(solve_game)
hint_button.on_click(give_hint)
reset_button.on_click(reset_game)


# IMPROVED VISUAL STYLE
display(HTML("""
<style>
.widget-button button,
.jupyter-widgets button {
    color: #172554 !important;
    font-weight: bold !important;
}
</style>

<div style="
    text-align:center;
    padding:15px;
    background:#F8FAFC;
    border-radius:14px;
    margin-bottom:12px;
">
    <h1 style="color:#4338CA;margin:0;font-size:32px">
        Sudoku AI
    </h1>
    <p style="color:#475569;margin:8px 0 0">
        Select a cell · Choose a number · Challenge the AI
    </p>
</div>
"""))

display(board_widget)

display(HTML(
    "<h4 style='text-align:center;color:#334155'>Choose a number</h4>"
))

display(widgets.HBox(
    number_buttons,
    layout=widgets.Layout(
        justify_content="center",
        flex_flow="row wrap"
    )
))

display(widgets.HBox(
    [check_button, solve_button],
    layout=widgets.Layout(
        justify_content="center",
        flex_flow="row wrap",
        gap="8px"
    )
))

display(widgets.HBox(
    [hint_button, reset_button],
    layout=widgets.Layout(
        justify_content="center",
        flex_flow="row wrap",
        gap="8px"
    )
))

display(message)

def validate_solution(grid):
    expected = set(range(1, 10))

    # Check rows
    for row in grid:
        if set(row) != expected:
            return False

    # Check columns
    for c in range(9):
        if {grid[r][c] for r in range(9)} != expected:
            return False

    # Check all 3x3 boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box = {
                grid[r][c]
                for r in range(br, br + 3)
                for c in range(bc, bc + 3)
            }
            if box != expected:
                return False

    return True


assert solution is not None, "Z3 could not solve the puzzle."
assert validate_solution(solution), "The solution failed validation."

# Verify that every original clue is preserved
for r in range(9):
    for c in range(9):
        if original_puzzle[r][c] != 0:
            assert solution[r][c] == original_puzzle[r][c]

print("All tests passed!")
print("The Z3 solution is valid.")
print("All original clues are preserved.")
