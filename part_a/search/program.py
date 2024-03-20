# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction
from .utils import render_board
from queue import PriorityQueue


def a_star_search(board, start, goal):
    open_set = PriorityQueue()
    open_set.put((0, start))  # (f-score, node)
    came_from = {}
    g_score = {start: 0}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path

        for neighbor in get_neighbors(current,board, goal):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(board, neighbor, goal)
                open_set.put((f_score, neighbor))

    return None  # No path found

def check_conseq_neighbours(current, direction, board, goal):
    conseq_empty = 0
    while conseq_empty < 4:
        if direction == "DOWN":
            new_r = current.r + 1
            if new_r == 11:
                new_r = 0
            new_c = current.c
        elif direction == "UP":
            new_r = current.r - 1
            if new_r == -1:
                new_r = 10
            new_c = current.c
        elif direction == "RIGHT":
            new_r = current.r
            new_c = current.c + 1
            if new_c == 11:
                new_c = 0
        else:
            new_r = current.r
            new_c = current.c - 1
            if new_c == -1:
                new_c = 10

        if Coord(new_r, new_c) in get_neighbors(current, board, goal):
            conseq_empty += 1
        else:
            return conseq_empty
    return conseq_empty

def manhatten_dist_finder(current, goal):
    row = abs(current.r - goal.r)
    column = abs(current.c - goal.c)

    dis_row = min(row, 11 - row)
    dis_column = min(column, 11 - column)

    return dis_row + dis_column

def heuristic(board, current, goal):
    # Calculate Manhattan distance to the goal
    manhattan_dist = manhatten_dist_finder(current, goal)

    # Determine if it's easier to fill the row or column of the goal block
    row_spaces = sum(1 for coord, color in board.items() if coord.r == goal.r and color == None)
    col_spaces = sum(1 for coord, color in board.items() if coord.c == goal.c and color == None)

    # Adjust heuristic based on the easier option
    if row_spaces <= col_spaces:
        return manhattan_dist + row_spaces
    else:
        return manhattan_dist + col_spaces

def get_neighbors(coord, board, target):
    """
    Get the neighboring coordinates of a given coordinate,
    considering obstacles on the board.
    """
    neighbors = []
    for row, column in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_r, new_c = coord.r + row, coord.c + column
        # Take into account that edge pieces are connected across the board
        if new_r == 11:
            new_r = 0
        elif new_r == -1:
            new_r = 10
        if new_c == 11:
            new_c = 0
        elif new_c == -1:
            new_c = 10

        # Check if the new coordinate is not obstructed by a blue block
        if board.get(Coord(new_r, new_c)) != PlayerColor.BLUE and board.get(Coord(new_r, new_c)) != PlayerColor.RED:
            neighbors.append(Coord(new_r, new_c))  # Add the neighboring coordinate
        if new_r == target.r and new_c == target.c:
            neighbors.append(Coord(new_r, new_c))
    return neighbors

# Helper function to reconstruct path
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path
    
def findRedCoordinates(board: dict[Coord, PlayerColor]) -> list:
    red_blocks = [coord for coord, color in board.items() if color == PlayerColor.RED]
    return red_blocks

def search(
    board: dict[Coord, PlayerColor], 
    target: Coord
) -> list[PlaceAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, target, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...
    path = a_star_search(board, Coord(2,4), target)
    if path:
        print("Shortest path from start to goal:", path)
    else:
        print("No path exists from start to goal.")

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
        PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
        PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    ]
