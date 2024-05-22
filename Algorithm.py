from Board import Board
from Constants import *


def minimax(
    state: Board,
    depth: int,
    alpha: float,
    beta: float,
    is_maximising_player: bool,
    forced_jumping: bool = False,
):
    if depth == 0 or state.is_game_over():
        return state.evaluate(), None

    maximizing = not is_maximising_player

    if is_maximising_player:
        max_eval = float("-inf")
        best_move = None
        for move in state.calculate_all_turn_moves(BLACK_COLOR, forced_jumping):
            state.make_move(move)
            eval = minimax(state, depth - 1, alpha, beta, maximizing, forced_jumping)[0]
            state.undo_move(move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for move in state.calculate_all_turn_moves(WHITE_COLOR, forced_jumping):
            state.make_move(move)
            eval = minimax(state, depth - 1, alpha, beta, maximizing, forced_jumping)[0]
            state.undo_move(move)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
