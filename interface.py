import pygame
import os
from chessboard import *
from invalid_animation import *
from game_controller import *

# =========================================================
# DRAW HELPERS
# =========================================================

def draw_selected_square(screen, square, flip_board=False):
    overlay = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
    overlay.fill((50, 100, 255, 120))  # blue transparent

    row = square // 8
    col = square % 8

    if flip_board:
        row = 7 - row
        col = 7 - col

    screen.blit(overlay, (col * SQUARE, row * SQUARE))


def draw_allowed_moves(screen, moves, flip_board=False):
    for square in moves:
        row = square // 8
        col = square % 8

        if flip_board:
            row = 7 - row
            col = 7 - col

        center_x = col * SQUARE + SQUARE // 2
        center_y = row * SQUARE + SQUARE // 2

        pygame.draw.circle(
            screen,
            (30, 144, 255),  # blue
            (center_x, center_y),
            SQUARE // 6,
        )


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

    color = board.get_color(pid)
    type_map = {
        ChessBoard.PAWN: "Pawn",
        ChessBoard.KNIGHT: "Knight",
        ChessBoard.BISHOP: "Bishop",
        ChessBoard.ROOK: "Rook",
        ChessBoard.QUEEN: "Queen",
        ChessBoard.KING: "King",
    }

    return color + "_" + type_map[board.pieceType[pid]]


def draw_board(screen, flip_board=False):
    colors = [(240, 217, 181), (181, 136, 99)]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]

            draw_row = 7 - row if flip_board else row
            draw_col = 7 - col if flip_board else col

            pygame.draw.rect(
                screen,
                color,
                (draw_col * SQUARE, draw_row * SQUARE, SQUARE, SQUARE),
            )


def draw_pieces(screen, board, images, flip_board=False):
    for square in range(64):
        pid = board.squarePiece[square]
        if pid == -1:
            continue

        key = piece_to_key(board, pid)
        row = square // 8
        col = square % 8

        if flip_board:
            row = 7 - row
            col = 7 - col

        screen.blit(images[key], (col * SQUARE, row * SQUARE))


# =========================================================
# MAIN LOOP
# =========================================================

WIDTH = 640
SQUARE = WIDTH // 8

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Chess")

    board = ChessBoard()
    images = load_piece_images("assets")

    selected_piece = None
    invalid_animation = None
    allowed_moves = []
    game = GameHandler()

    render_surface = pygame.Surface((WIDTH, WIDTH))  # intermediate surface
    flip_board = True  # toggle this to flip board visually

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # 60 FPS

        # ========================
        # 1️⃣ Handle Events
        # ========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(selected_piece)
                print(allowed_moves)
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE
                row = y // SQUARE
                square = row * 8 + col

                # =========================
                # Nothing selected → SELECT
                # =========================
                if selected_piece is None:
                    if board.get_color(board.squarePiece[square]) == game.side_to_move:
                        selected_piece = board.squarePiece[square]
                        allowed_moves = board.get_legal_moves(selected_piece)
                    else:
                        invalid_animation = InvalidMoveAnimation(square)

                # =========================
                # Piece already selected → TRY MOVE
                # =========================
                else:
                    if board.pieceSquare[selected_piece] == square:
                        selected_piece = None
                        allowed_moves = []
                    else:
                        if square in allowed_moves:
                            board.move_piece(selected_piece, square)
                            selected_piece = None
                            allowed_moves = []
                            flip_board=not flip_board
                            game.side_to_move = "b" if game.side_to_move == "w" else "w"
                        else:
                            invalid_animation = InvalidMoveAnimation(square)
                            selected_piece = None
                            allowed_moves = []

        # ========================
        # Update Animation
        # ========================
        if invalid_animation:
            invalid_animation.update()
            if invalid_animation.finished:
                invalid_animation = None

        # ========================
        # Draw Everything
        # ========================
        render_surface.fill((0, 0, 0))  # clear surface

        draw_board(render_surface, flip_board)
        draw_pieces(render_surface, board, images, flip_board)
        if selected_piece is not None:
            draw_selected_square(render_surface, board.pieceSquare[selected_piece], flip_board)
        draw_allowed_moves(render_surface, allowed_moves, flip_board)
        if invalid_animation:
            invalid_animation.draw(render_surface, SQUARE)

        # Blit render surface to screen
        screen.blit(render_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()