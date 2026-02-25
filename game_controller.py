from chessboard import *
class GameHandler:
    def __init__(self):
        self.board = ChessBoard()
        self.side_to_move = "w"
        self.game_over = False
        self.rotate_board = False

    def get_legal_moves(self, piece):
        if self.board.get_color(piece) != self.side_to_move:
            return []
        return self.board.get_legal_moves(piece)

    def try_move(self, piece, target):
        legal = self.get_legal_moves(piece)
        if target in legal:
            self.board.move_piece(piece, target)
            self.switch_turn()
            return True
        return False

    def switch_turn(self):
        self.side_to_move = "b" if self.side_to_move == "w" else "w"