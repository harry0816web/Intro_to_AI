import numpy as np
import random
import game

def print_INFO():
    """
    Prints your homework submission details.
    Please replace the placeholders (date, name, student ID) with valid information
    before submitting.
    """
    print(
        """========================================
        DATE: 2025/3/31
        STUDENT NAME: 楊弘奕
        STUDENT ID: 112550097
        ========================================
        """)


#
# Basic search functions: Minimax and Alpha‑Beta
#

def minimax(grid, depth, maximizingPlayer, dep=4):
    """
    TODO (Part 1): Implement recursive Minimax search for Connect Four.

    Return:
      (boardValue, {setOfCandidateMoves})

    Where:
      - boardValue is the evaluated utility of the board state
      - {setOfCandidateMoves} is a set of columns that achieve this boardValue
    """
    # Placeholder return to keep function structure intac
    candidate_moves = set()

    if grid.terminate() or depth == 0:
        return get_heuristic(grid), {0}

    if maximizingPlayer:  # choose max for self
        value = -np.inf
        # for each possible move
        for col in grid.valid:
            new_grid = game.drop_piece(grid, col)
            new_value, _ = minimax(new_grid, depth-1, False, dep)
            if new_value > value:
                value = new_value
                candidate_moves = {col}
            elif new_value == value:
                candidate_moves.add(col)
    else:             # choose min for opponent
        value = np.inf
        for col in grid.valid:
            new_grid = game.drop_piece(grid, col)
            new_value, _ = minimax(new_grid, depth-1, True, dep)
            if new_value < value:
                value = new_value
                candidate_moves = {col}
            elif new_value == value:
                candidate_moves.add(col)
    return value, candidate_moves


def alphabeta(grid, depth, maximizingPlayer, alpha, beta, dep=4):
    """
    TODO (Part 2): Implement Alpha-Beta pruning as an optimization to Minimax.

    Return:
      (boardValue, {setOfCandidateMoves})

    Where:
      - boardValue is the evaluated utility of the board state
      - {setOfCandidateMoves} is a set of columns that achieve this boardValue
      - Prune branches when alpha >= beta
    """
    candidate_moves = set()

    if grid.terminate() or depth == 0:
        return get_heuristic(grid), {0}
    
    if maximizingPlayer:  # choose max for self
        value = -np.inf
        for col in grid.valid:
            new_grid = game.drop_piece(grid, col)
            new_value, _ = alphabeta(new_grid, depth-1, False, alpha, beta, dep)
            if new_value > value:
                value = new_value
                candidate_moves = {col}
            elif new_value == value:
                candidate_moves.add(col)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    else:
        value = np.inf
        for col in grid.valid:
            new_grid = game.drop_piece(grid, col)
            new_value, _ = alphabeta(new_grid, depth-1, True, alpha, beta, dep)
            if new_value < value:
                value = new_value
                candidate_moves = {col}
            elif new_value == value:
                candidate_moves.add(col)
            beta = min(beta, value)
            if alpha >= beta:
                break
    return value, candidate_moves

    # Placeholder return to keep function structure intact


#
# Basic agents
#

def agent_minimax(grid):
    """
    Agent that uses the minimax() function with a default search depth (e.g., 4).
    Must return a single column (integer) where the piece is dropped.
    """
    return random.choice(list(minimax(grid, 4, True)[1]))


def agent_alphabeta(grid):
    """
    Agent that uses the alphabeta() function with a default search depth (e.g., 4).
    Must return a single column (integer) where the piece is dropped.
    """
    return random.choice(list(alphabeta(grid, 4, True, -np.inf, np.inf)[1]))


def agent_reflex(grid):
    """
    A simple reflex agent provided as a baseline:
      - Checks if there's an immediate winning move.
      - Otherwise picks a random valid column.
    """
    wins = [c for c in grid.valid if game.check_winning_move(grid, c, grid.mark)]
    if wins:
        return random.choice(wins)
    return random.choice(grid.valid)


def agent_strong(grid):
    """
    TODO (Part 3): Design your own agent (depth = 4) to consistently beat the Alpha-Beta agent (depth = 4).
    This agent will typically act as Player 2.
    """
    # Placeholder logic that calls your_function().
     # Using our stronger search function with depth 4.
    value, candidate_moves = your_function(grid, 4, True, -np.inf, np.inf, dep=4)
    print("Value:", value)
    print("Candidate Moves:", candidate_moves)
    if candidate_moves:
        return random.choice(list(candidate_moves))
    return random.choice(grid.valid)


#
# Heuristic functions
#

def get_heuristic(board):
    """
    Evaluates the board from Player 1's perspective using a basic heuristic.

    Returns:
      - Large positive value if Player 1 is winning
      - Large negative value if Player 2 is winning
      - Intermediate scores based on partial connect patterns
    """
    num_twos       = game.count_windows(board, 2, 1)
    num_threes     = game.count_windows(board, 3, 1)
    num_twos_opp   = game.count_windows(board, 2, 2)
    num_threes_opp = game.count_windows(board, 3, 2)

    score = (
          1e10 * board.win(1)
        + 1e6  * num_threes
        + 10   * num_twos
        - 10   * num_twos_opp
        - 1e6  * num_threes_opp
        - 1e10 * board.win(2)
    )
    return score

def get_heuristic_strong(board):
    """
    TODO (Part 3): Implement a more advanced board evaluation for agent_strong.
    Currently a placeholder that returns 0.
    """
    # 1. Immediate win/loss
    if board.win(2):
        return 1e12
    if board.win(1):
        return -1e12

    # # 2. Forced Wins: if any immediate winning moves exist
    winning_moves_p1 = [col for col in board.valid if game.check_winning_move(board, col, 2)]
    winning_moves_p2 = [col for col in board.valid if game.check_winning_move(board, col, 1)]
    if winning_moves_p1:
        return 1e10 + 1000 * len(winning_moves_p1)
    if winning_moves_p2:
        return -1e10 - 1000 * len(winning_moves_p2)

    # 4. Potential connect patterns (3-in-a-row and 2-in-a-row)
    num_threes_p1 = game.count_windows(board, 3, 2)
    num_threes_p2 = game.count_windows(board, 3, 1)
    num_twos_p1   = game.count_windows(board, 2, 2)
    num_twos_p2   = game.count_windows(board, 2, 1)
    pattern_score = (num_threes_p1 - num_threes_p2) * 1e6 + (num_twos_p1 - num_twos_p2) * 100

    # 5. Strategic Positioning: Center control
    center_column = board.column // 2
    center_count_p1 = sum(1 for r in range(board.row) if board.table[r][center_column] == 2)
    center_count_p2 = sum(1 for r in range(board.row) if board.table[r][center_column] == 1)
    center_score = 5000 * (center_count_p1 - center_count_p2)

    # 綜合評分
    score = pattern_score + center_score
    return score
    


def your_function(grid, depth, maximizingPlayer, alpha, beta, dep=4):
    """
    A stronger search function that uses get_heuristic_strong() instead of get_heuristic().
    You can employ advanced features (e.g., improved move ordering, deeper lookahead).

    Return:
      (boardValue, {setOfCandidateMoves})

    Currently a placeholder returning (0, {0}).
    """
    candidate_moves = []

    # Terminal condition: game over or reached maximum depth (depth == 0)
    if grid.terminate() or depth == 0:
        base_score = get_heuristic_strong(grid)
        # # Depth-aware adjustment:
        # # For favorable positions, a higher remaining depth (i.e. win faster) is better.
        # # For unfavorable positions, losing sooner is worse.
        # bonus = depth * 50  # 調整因子（可根據實驗調整）
        # if base_score > 0:
        #     adjusted_score = base_score + bonus
        # elif base_score < 0:
        #     adjusted_score = base_score - bonus
        # else:
        #     adjusted_score = base_score
        return base_score, []
    
    # forced win/loss check
    if depth == 4:
        # check if almost win
      winning_moves_p1 = [col for col in grid.valid if game.check_winning_move(grid, col, 1)]
      if winning_moves_p1:
          return 0, winning_moves_p1
      # check if opponent almost win
      winning_moves_p2 = [col for col in grid.valid if game.check_winning_move(grid, col, 2)]
      if winning_moves_p2:  
        return 0, winning_moves_p2
    if maximizingPlayer:
        value = -np.inf
        for col in grid.valid:
            new_grid = game.drop_piece(grid, col)
            new_value, _ = your_function(new_grid, depth - 1, False, alpha, beta, dep)
            if new_value > value:
                value = new_value
                candidate_moves = [col]
            elif new_value == value:
                candidate_moves.append(col)
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        # print("maxValue:", value)
        return value, candidate_moves
    else:
        value = np.inf
        for col in grid.valid:
            new_grid = game.drop_piece(grid, col)
            new_value, _ = your_function(new_grid, depth - 1, True, alpha, beta, dep)
            if new_value < value:
                value = new_value
                candidate_moves = [col]
            elif new_value == value:
                candidate_moves.append(col)
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff
        # print("minValue:", value)
        return value, candidate_moves
    
    