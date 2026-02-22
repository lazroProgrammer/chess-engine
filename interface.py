import pygame
import os

# =========================================================
# CHESS ENGINE (Your Code - Slightly Cleaned)
# =========================================================

class ChessBoard:
    PAWN   = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK   = 3
    QUEEN  = 4
    KING   = 5

    WHITE = 0
    BLACK = 1

    def __init__(self):
        self.pieceSquare = [-1] * 32
        self.squarePiece = [-1] * 64
        self.pieceType = [None] * 32
        self.pieceColor = [None] * 32

        self.sideToMove = ChessBoard.WHITE
        self.castlingRights = 0b1111
        self.enPassantSquare = -1
        self.halfmoveClock = 0
        self.fullmoveNumber = 1

        self._initialize_pieces()
        self._initialize_start_position()

    def _initialize_pieces(self):
        for i in range(8):
            self.pieceType[i] = ChessBoard.PAWN
            self.pieceColor[i] = ChessBoard.WHITE

        self.pieceType[8] = self.pieceType[9] = ChessBoard.ROOK
        self.pieceColor[8] = self.pieceColor[9] = ChessBoard.WHITE

        self.pieceType[10] = self.pieceType[11] = ChessBoard.KNIGHT
        self.pieceColor[10] = self.pieceColor[11] = ChessBoard.WHITE

        self.pieceType[12] = self.pieceType[13] = ChessBoard.BISHOP
        self.pieceColor[12] = self.pieceColor[13] = ChessBoard.WHITE

        self.pieceType[14] = ChessBoard.QUEEN
        self.pieceColor[14] = ChessBoard.WHITE

        self.pieceType[15] = ChessBoard.KING
        self.pieceColor[15] = ChessBoard.WHITE

        for i in range(16):
            self.pieceType[i + 16] = self.pieceType[i]
            self.pieceColor[i + 16] = ChessBoard.BLACK

    def _initialize_start_position(self):
        def place(pid, sq):
            self.pieceSquare[pid] = sq
            self.squarePiece[sq] = pid

        for i in range(8):
            place(i, 8 + i)

        place(8, 0); place(10, 1); place(12, 2)
        place(14, 3); place(15, 4); place(13, 5)
        place(11, 6); place(9, 7)

        for i in range(8):
            place(i + 16, 48 + i)

        place(24, 56); place(26, 57); place(28, 58)
        place(30, 59); place(31, 60); place(29, 61)
        place(27, 62); place(25, 63)

    def move_piece(self, piece_id, to_square):
        from_square = self.pieceSquare[piece_id]
        captured = self.squarePiece[to_square]

        if captured != -1:
            self.pieceSquare[captured] = -1

        self.squarePiece[from_square] = -1
        self.squarePiece[to_square] = piece_id
        self.pieceSquare[piece_id] = to_square


# =========================================================
# UI HELPERS
# =========================================================

WIDTH = 640
SQUARE = WIDTH // 8

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

    color = "w" if board.pieceColor[pid] == ChessBoard.WHITE else "b"

    type_map = {
        ChessBoard.PAWN: "Pawn",
        ChessBoard.KNIGHT: "Knight",
        ChessBoard.BISHOP: "Bishop",
        ChessBoard.ROOK: "Rook",
        ChessBoard.QUEEN: "Queen",
        ChessBoard.KING: "King",
    }

    return color + "_" + type_map[board.pieceType[pid]]


def draw_board(screen):
    colors = [(240, 217, 181), (181, 136, 99)]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(
                screen,
                color,
                (col * SQUARE, row * SQUARE, SQUARE, SQUARE),
            )


def draw_pieces(screen, board, images):
    for square in range(64):
        pid = board.squarePiece[square]
        if pid == -1:
            continue

        key = piece_to_key(board, pid)
        row = square // 8
        col = square % 8

        screen.blit(images[key], (col * SQUARE, row * SQUARE))


class InvalidMoveAnimation:
    def __init__(self, square, duration=400):
        self.square = square
        self.duration = duration  # milliseconds
        self.start_time = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.finished = True

    def draw(self, screen, square_size):
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = elapsed / self.duration

        if progress > 1:
            progress = 1

        # Fade in then fade out (triangle wave)
        if progress <= 0.5:
            alpha = int(255 * (progress * 2))
        else:
            alpha = int(255 * (1 - (progress - 0.5) * 2))

        overlay = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, alpha))

        row = self.square // 8
        col = self.square % 8

        screen.blit(overlay, (col * square_size, row * square_size))

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
    invalid_animation = None

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
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE
                row = y // SQUARE
                square = row * 8 + col

                if selected_piece is None:
                    pid = board.squarePiece[square]
                    if pid != -1:
                        selected_piece = pid
                else:
                    if board.squarePiece[square] == -1:
                        board.move_piece(selected_piece, square)
                    else:
                        invalid_animation = InvalidMoveAnimation(square)

                    selected_piece = None

        # ========================
        # 2️⃣ Update Animation
        # ========================
        if invalid_animation:
            invalid_animation.update()
            if invalid_animation.finished:
                invalid_animation = None

        # ========================
        # 3️⃣ Draw Everything
        # ========================
        draw_board(screen)
        draw_pieces(screen, board, images)

        if invalid_animation:
            invalid_animation.draw(screen, SQUARE)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()