import pygame
import os
from chessboard import *
from invalid_animation import *
from game_controller import *

# =========================================================
# CONSTANTS
# =========================================================

WIDTH = 640
SQUARE = WIDTH // 8
MODE="flip"

# =========================================================
# HELPERS
# =========================================================

def flip_coords_vertical(row, col, flip_board):
    """Flip board top-to-bottom if flip_board=True"""
    if flip_board:
        return 7 - row, col
    return row, col

def load_piece_images(folder):
    images = {}
    for file in os.listdir(folder):
        if file.endswith(".png"):
            key = file.split(".")[0]
            path = os.path.join(folder, file)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (SQUARE, SQUARE))
            images[key] = img
    return images

def piece_to_key(board, pid):
    if pid == -1:
        return None
    color = "w" if board.get_color(pid)== board.WHITE else "b"
    type_map = {
        ChessBoard.PAWN: "Pawn",
        ChessBoard.KNIGHT: "Knight",
        ChessBoard.BISHOP: "Bishop",
        ChessBoard.ROOK: "Rook",
        ChessBoard.QUEEN: "Queen",
        ChessBoard.KING: "King",
    }
    return color + "_" + type_map[board.pieceType[pid]]

# =========================================================
# DRAW FUNCTIONS
# =========================================================

def draw_board(screen, flip_board=False):
    colors = [(240, 217, 181), (181, 136, 99)]
    for row in range(8):
        for col in range(8):
            draw_row, draw_col = flip_coords_vertical(row, col, flip_board)
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (draw_col * SQUARE, draw_row * SQUARE, SQUARE, SQUARE))

def draw_pieces(screen, board, images, flip_board=False):
    for square in range(64):
        pid = board.squarePiece[square]
        if pid == -1:
            continue
        key = piece_to_key(board, pid)
        row = square // 8
        col = square % 8
        draw_row, draw_col = flip_coords_vertical(row, col, flip_board)
        screen.blit(images[key], (draw_col * SQUARE, draw_row * SQUARE))

def draw_selected_square(screen, square, flip_board=False):
    overlay = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
    overlay.fill((50, 100, 255, 120))
    row = square // 8
    col = square % 8
    row, col = flip_coords_vertical(row, col, flip_board)
    screen.blit(overlay, (col * SQUARE, row * SQUARE))

def draw_allowed_moves(screen, moves, flip_board=False):
    for square in moves:
        row = square // 8
        col = square % 8
        row, col = flip_coords_vertical(row, col, flip_board)
        center_x = col * SQUARE + SQUARE // 2
        center_y = row * SQUARE + SQUARE // 2
        pygame.draw.circle(screen, (30, 144, 255), (center_x, center_y), SQUARE // 6)

# =========================================================
# MAIN LOOP
# =========================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Chess")

    board = ChessBoard()
    images = load_piece_images("assets")

    selected_piece = None
    allowed_moves = []
    invalid_animation = None
    game = GameHandler()

    render_surface = pygame.Surface((WIDTH, WIDTH))
    flip_board = True  # vertical flip top-to-bottom

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        # ========================
        # EVENTS
        # ========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE
                row = y // SQUARE

                # adjust row for vertical flip
                if flip_board:
                    row = 7 - row

                square = row * 8 + col

                # =========================
                # SELECT PIECE
                # =========================
                if selected_piece is None:
                    pid = board.squarePiece[square]

                    if pid != -1 and board.get_color(pid) == game.side_to_move:
                        selected_piece = pid
                        allowed_moves = board.get_legal_moves(pid, game.side_to_move)
                    else:
                        invalid_animation = InvalidMoveAnimation(square)
                # =========================
                # MOVE PIECE
                # =========================
                else:
                    if board.pieceSquare[selected_piece] == square:
                        selected_piece = None
                        allowed_moves = []
                    else:
                        if square in allowed_moves:
                            board.move_piece(selected_piece, square)
                            board.get_pinned_pieces(board.BLACK if game.side_to_move== board.WHITE else board.WHITE)
                            selected_piece = None
                            allowed_moves = []
                            if(game.side_to_move== board.WHITE):
                                if board.is_checkmate(board.BLACK):
                                    print("White wins by checkmate!")
                                elif board.is_stalemate(board.BLACK):
                                    print("Stalemate!")
                            if(game.side_to_move== board.BLACK):
                                if board.is_checkmate(board.WHITE):
                                    print("Black wins by checkmate!")
                                elif board.is_stalemate(board.WHITE):
                                    print("Stalemate!")
                            game.side_to_move = board.BLACK if game.side_to_move == board.WHITE else board.WHITE
                            if(MODE=="flip"):
                                flip_board= not flip_board
                        else:
                            invalid_animation = InvalidMoveAnimation(square)
                            selected_piece = None
                            allowed_moves = []

        # ========================
        # UPDATE ANIMATION
        # ========================
        if invalid_animation:
            invalid_animation.update()
            if invalid_animation.finished:
                invalid_animation = None

        # ========================
        # DRAW EVERYTHING
        # ========================
        render_surface.fill((0, 0, 0))

        draw_board(render_surface, flip_board)
        draw_pieces(render_surface, board, images, flip_board)
        if selected_piece is not None:
            draw_selected_square(render_surface, board.pieceSquare[selected_piece], flip_board)
        draw_allowed_moves(render_surface, allowed_moves, flip_board)
        if invalid_animation:
            invalid_animation.draw(render_surface, SQUARE)

        screen.blit(render_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()