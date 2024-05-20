from TileState import TileState


def minimax(state, depth, alpha, beta, is_maximising_player):
    if depth == 0 or state.is_game_over():
        return state.evaluate(), None

    maximizing = not is_maximising_player

    if is_maximising_player:
        max_eval = float("-inf")
        best_move = None
        for move in state.calculate_all_turn_moves(TileState.BLACK_COLOR):
            state.make_move(move)
            eval = minimax(state, depth - 1, alpha, beta, maximizing)[0]
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
        for move in state.calculate_all_turn_moves(TileState.WHITE_COLOR):
            state.make_move(move)
            eval = minimax(state, depth - 1, alpha, beta, maximizing)[0]
            state.undo_move(move)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
