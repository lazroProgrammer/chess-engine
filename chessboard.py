class ChessBoard:
    # ==============================
    # Piece Type Constants
    # ==============================
    PAWN   = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK   = 3
    QUEEN  = 4
    KING   = 5
    
    WHITE_KING=15
    BLACK_KING=31

    # ==============================
    # Color Constants
    # ==============================
    WHITE = 0
    BLACK = 1

    # ==============================
    # Constructor
    # ==============================
    def __init__(self):
        # piece -> square (0..63, or -1 if captured)
        self.pieceSquare = [-1] * 32

        # square -> piece (0..31, or -1 if empty)
        self.squarePiece = [-1] * 64

        # piece -> type (PAWN, KNIGHT, ...)
        self.pieceType = [None] * 32

        # piece -> color (WHITE / BLACK)
        self.pieceColor = [None] * 32

        # Game state
        self.sideToMove = ChessBoard.WHITE
        self.castlingRights = 0b1111  # WK WQ BK BQ
        self.enPassantSquare = -1
        self.halfmoveClock = 0
        self.fullmoveNumber = 1

        self._initialize_pieces()
        self._initialize_start_position()

    # ==============================
    # Piece Enumeration
    # ==============================
    def _initialize_pieces(self):
        """
        Piece IDs:
        0–15  = White pieces
        16–31 = Black pieces

        Order:
        0–7   White pawns
        8–9   White rooks
        10–11 White knights
        12–13 White bishops
        14    White queen
        15    White king

        Same pattern for black (+16)
        """

        # White pawns
        for i in range(8):
            self.pieceType[i] = ChessBoard.PAWN
            self.pieceColor[i] = ChessBoard.WHITE

        # White rooks
        self.pieceType[8] = self.pieceType[9] = ChessBoard.ROOK
        self.pieceColor[8] = self.pieceColor[9] = ChessBoard.WHITE

        # White knights
        self.pieceType[10] = self.pieceType[11] = ChessBoard.KNIGHT
        self.pieceColor[10] = self.pieceColor[11] = ChessBoard.WHITE

        # White bishops
        self.pieceType[12] = self.pieceType[13] = ChessBoard.BISHOP
        self.pieceColor[12] = self.pieceColor[13] = ChessBoard.WHITE

        # White queen
        self.pieceType[14] = ChessBoard.QUEEN
        self.pieceColor[14] = ChessBoard.WHITE

        # White king
        self.pieceType[15] = ChessBoard.KING
        self.pieceColor[15] = ChessBoard.WHITE

        # Black pieces (mirror white)
        for i in range(16):
            self.pieceType[i + 16] = self.pieceType[i]
            self.pieceColor[i + 16] = ChessBoard.BLACK

    # ==============================
    # Initial Position Setup
    # ==============================
    def _initialize_start_position(self):
        # Clear board
        for sq in range(64):
            self.squarePiece[sq] = -1

        # Helper
        def place(piece_id, square):
            self.pieceSquare[piece_id] = square
            self.squarePiece[square] = piece_id

        # White pawns (rank 2 → squares 8..15)
        for i in range(8):
            place(i, 8 + i)

        # White major pieces (rank 1)
        place(8, 0)   # rook
        place(10, 1)  # knight
        place(12, 2)  # bishop
        place(14, 3)  # queen
        place(15, 4)  # king
        place(13, 5)  # bishop
        place(11, 6)  # knight
        place(9, 7)   # rook

        # Black pawns (rank 7 → squares 48..55)
        for i in range(8):
            place(i + 16, 48 + i)

        # Black major pieces (rank 8)
        place(24, 56)  # rook
        place(26, 57)  # knight
        place(28, 58)  # bishop
        place(30, 59)  # queen
        place(31, 60)  # king
        place(29, 61)  # bishop
        place(27, 62)  # knight
        place(25, 63)  # rook

    # ==============================
    # Utility Methods
    # ==============================
    def get_piece_on_square(self, square):
        return self.squarePiece[square]

    def get_square_of_piece(self, piece_id):
        return self.pieceSquare[piece_id]

    def get_coordinates(self, square: int):
        return (square//8, square % 8)
        
    def get_square(self, coordinates: tuple):
        return coordinates[0] * 8 + coordinates[1]
    def in_boundary(self, pair):
        if(pair[0]<8 and pair[1]<8 and pair[0]>-1 and pair[1]>-1):
            return True
        return False
        
    
    def move_piece(self, piece_id, to_square):
        from_square = self.pieceSquare[piece_id]
        captured_piece = self.squarePiece[to_square]

        # Remove captured piece
        if captured_piece != -1:
            self.pieceSquare[captured_piece] = -1

        # Move piece
        self.squarePiece[from_square] = -1
        self.squarePiece[to_square] = piece_id
        self.pieceSquare[piece_id] = to_square

        return captured_piece
    
        # ==============================
    # Position Statistics
    # ==============================
    def compute_stats(self):
        """
        Returns a dictionary containing useful position statistics.
        """

        stats = {
            "material": {
                ChessBoard.WHITE: 0,
                ChessBoard.BLACK: 0,
            },
            "piece_counts": {
                ChessBoard.WHITE: {t: 0 for t in range(6)},
                ChessBoard.BLACK: {t: 0 for t in range(6)},
            },
            "total_pieces": 0,
            "side_to_move": self.sideToMove,
            "castling_rights": self.castlingRights,
            "en_passant_square": self.enPassantSquare,
            "halfmove_clock": self.halfmoveClock,
            "fullmove_number": self.fullmoveNumber,
        }

        # Standard material values
        piece_values = {
            ChessBoard.PAWN: 100,
            ChessBoard.KNIGHT: 320,
            ChessBoard.BISHOP: 330,
            ChessBoard.ROOK: 500,
            ChessBoard.QUEEN: 900,
            ChessBoard.KING: 0,
        }

        for piece_id in range(32):
            square = self.pieceSquare[piece_id]
            if square == -1:
                continue

            color = self.pieceColor[piece_id]
            ptype = self.pieceType[piece_id]

            stats["piece_counts"][color][ptype] += 1
            stats["material"][color] += piece_values[ptype]
            stats["total_pieces"] += 1

        stats["material_balance"] = (
            stats["material"][ChessBoard.WHITE]
            - stats["material"][ChessBoard.BLACK]
        )

        return stats
    def get_type(self, piece_num):
        if(piece_num==-1):
            return None
        else:
            return self.pieceType[piece_num]
    
    def get_color(self, piece_num):
        if(piece_num < 0):
            return None
        else:
            return self.pieceColor[piece_num]
        
    def is_pawn_in_start(self, piece_id):
        if(self.get_type(piece_id) != ChessBoard.PAWN):
            raise RuntimeError("pawn_in_start() is only for pawns")
        square= self.pieceSquare[piece_id]
        if self.pieceColor[piece_id] == ChessBoard.WHITE and 8 <= square <= 15:
            return True

        # Black pawns start on rank 7 (squares 48..55)
        if self.pieceColor[piece_id] == ChessBoard.BLACK and 48 <= square <= 55:
            return True
        return False

        
    def cast_pieces(self,piece_num):
        if(self.get_type(piece_num) ==-1):
            return "X"
        elif(self.get_type(piece_num) == ChessBoard.PAWN):
            return "P"
        elif(self.get_type(piece_num) == ChessBoard.ROOK):
            return "R"
        elif(self.get_type(piece_num) == ChessBoard.KNIGHT):
            return "N"
        elif(self.get_type(piece_num) == ChessBoard.BISHOP):
            return "B"
        elif(self.get_type(piece_num) == ChessBoard.QUEEN):
            return "Q"
        elif(self.get_type(piece_num) == ChessBoard.KING):
            return "K"
    def showBoard(self):
        cpt= 0
        line=""
        for i in self.squarePiece:
            cpt+=1
            line+=f"{self.cast_pieces(i)} "
            if(cpt % 8 == 0):
                print(f"{line}")
                line=""
    def get_pseudo_moves(self, piece_id):
        allowed_moves = []

        square = self.pieceSquare[piece_id]
        if square == -1:
            return allowed_moves

        piece_type = self.pieceType[piece_id]
        color = self.pieceColor[piece_id]

        row, col = self.get_coordinates(square)

        offsets = {
            self.PAWN:   [(-1, -1), (-1, 1)],  # capture offsets (white perspective)
            self.KNIGHT: [(2,1),(1,2),(-2,1),(-1,2),(2,-1),(1,-2),(-2,-1),(-1,-2)],
            self.KING:   [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        }

        offsets_increments = {
            self.BISHOP: [(1,1),(-1,1),(1,-1),(-1,-1)],
            self.ROOK:   [(1,0),(0,1),(-1,0),(0,-1)],
            self.QUEEN:  [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        }

        # -------------------------
        # PAWN
        # -------------------------
        if piece_type == self.PAWN:

            direction = 1 if color == self.WHITE else -1

            # Forward move
            forward_row = row + direction
            if 0 <= forward_row < 8:
                forward_square = self.get_square((forward_row, col))
                if self.squarePiece[forward_square] == -1:
                    allowed_moves.append(forward_square)

                    # Double move
                    if self.is_pawn_in_start(piece_id):
                        double_row = row + 2 * direction
                        double_square = self.get_square((double_row, col))
                        if self.squarePiece[double_square] == -1:
                            allowed_moves.append(double_square)

            # Captures
            direction = 1 if color == self.WHITE else -1

            for dc in (-1, 1):
                new_row = row + direction
                new_col = col + dc

                if self.in_boundary((new_row,new_col)):
                    target = self.get_square((new_row, new_col))
                    target_piece = self.squarePiece[target]

                    if target_piece != -1 and self.pieceColor[target_piece] != color:
                        allowed_moves.append(target)

            return allowed_moves

        # -------------------------
        # KNIGHT / KING
        # -------------------------
        if piece_type in offsets:

            for dr, dc in offsets[piece_type]:
                new_row = row + dr
                new_col = col + dc

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.get_square((new_row, new_col))
                    target_piece = self.squarePiece[target]

                    if target_piece == -1 or self.pieceColor[target_piece] != color:
                        allowed_moves.append(target)

            return allowed_moves

        # -------------------------
        # SLIDING PIECES
        # -------------------------
        if piece_type in offsets_increments:

            for dr, dc in offsets_increments[piece_type]:
                r = row + dr
                c = col + dc

                while 0 <= r < 8 and 0 <= c < 8:
                    target = self.get_square((r, c))
                    target_piece = self.squarePiece[target]

                    if target_piece == -1:
                        allowed_moves.append(target)
                    else:
                        if self.pieceColor[target_piece] != color:
                            allowed_moves.append(target)
                        break

                    r += dr
                    c += dc

            return allowed_moves

        return allowed_moves            

    def get_rook_moves(self, piece):
            color = self.get_color(piece)
            square= self.pieceSquare[piece]
            allowed_moves=[]

            # -----------------
            # LEFT (file -1)
            # -----------------
            cpt = square - 1
            while cpt >= 0 and cpt // 8 == square // 8:
                if self.squarePiece[cpt] == -1:
                    allowed_moves.append(cpt)
                else:
                    if self.get_color(self.squarePiece[cpt]) != color:
                        allowed_moves.append(cpt)
                    break
                cpt -= 1

            # -----------------
            # RIGHT (file +1)
            # -----------------
            cpt = square + 1
            while cpt < 64 and cpt // 8 == square // 8:
                if self.squarePiece[cpt] == -1:
                    allowed_moves.append(cpt)
                else:
                    if self.get_color(self.squarePiece[cpt]) != color:
                        allowed_moves.append(cpt)
                    break
                cpt += 1

            # -----------------
            # UP (rank +1)
            # -----------------
            cpt = square + 8
            while cpt < 64:
                if self.squarePiece[cpt] == -1:
                    allowed_moves.append(cpt)
                else:
                    if self.get_color(self.squarePiece[cpt]) != color:
                        allowed_moves.append(cpt)
                    break
                cpt += 8

            # -----------------
            # DOWN (rank -1)
            # -----------------
            cpt = square - 8
            while cpt >= 0:
                if self.squarePiece[cpt] == -1:
                    allowed_moves.append(cpt)
                else:
                    if self.get_color(self.squarePiece[cpt]) != color:
                        allowed_moves.append(cpt)
                    break
                cpt -= 8
            return allowed_moves
        
                
    def get_bishop_moves(self, piece_id):
        allowed_moves = []

        square = self.pieceSquare[piece_id]
        row = square // 8
        col = square % 8
        color = self.pieceColor[piece_id]

        # 4 diagonal directions
        directions = [
            (1, 1),    # down-right
            (1, -1),   # down-left
            (-1, 1),   # up-right
            (-1, -1)   # up-left
        ]

        for dr, dc in directions:
            r = row + dr
            c = col + dc

            # ray trace until blocked
            while 0 <= r < 8 and 0 <= c < 8:
                target = r * 8 + c
                target_piece = self.squarePiece[target]

                if target_piece == -1:
                    allowed_moves.append(target)
                else:
                    # capture if enemy
                    if self.pieceColor[target_piece] != color:
                        allowed_moves.append(target)
                    break  # stop ray after hitting piece

                r += dr
                c += dc

        return allowed_moves
    ## TODO: fix these after doing the groundwork
    def in_check(self, color):
        king= self.WHITE_KING if color==self.WHITE else self.BLACK_KING
        return self.is_square_attacked(self.pieceSquare[king], color)
    def checkmate(self, turn):
        king= self.WHITE_KING if turn== self.WHITE else self.BLACK_KING
        if self.in_check() and self.get_pseudo_moves(king) == [] and True:
            ## TODO!: missing the getting piece to block forced Check
            return True
        else:
            #TODO: the restricted set of moves that can be played
            return False
            
        
    def is_square_attacked(self, square, color):
        pair= self.get_coordinates(square)
        offsets={self.PAWN:[(-1,-1), (-1,1)],
        self.KNIGHT:[(2,1),(1,2),(-2,1),(-1,2),(2,-1),(1,-2),(-2,-1),(-1,-2)],
        self.KING:  [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        }
        offsets_increments={
        self.BISHOP:[(1,1),(-1,1),(1,-1),(-1,-1)],
        self.ROOK:[(1,0),(0,1),(-1,0),(0,-1)],
        self.QUEEN:  [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)]
        }
        
        opposite_color= self.WHITE if color==self.BLACK else self.BLACK
        for piece_type in offsets.keys():
            for offset in offsets[piece_type]:
                updated_coordinates=(pair[0]+offset[0], pair[1]+offset[1])
                if(self.in_boundary(updated_coordinates)):
                    danger_square= self.get_square(updated_coordinates)
                    potentiel_piece=self.squarePiece[danger_square]
                    if(self.get_type(potentiel_piece)== piece_type and self.pieceColor[potentiel_piece]  == opposite_color):
                        return True
        for piece_type in offsets_increments.keys():
            if(self.exists(piece_type, opposite_color)):
                for piece in self.get_pieces(piece_type, opposite_color):
                    if(square in self.get_pseudo_moves(piece)):
                        return True
        return False   
              
    def get_pieces(self, piece_type=None, color=None, only_alive=True):
        """
        Returns a list of piece_ids filtered by:
        - piece_type (PAWN, KNIGHT, etc.)
        - color (WHITE / BLACK)
        - only_alive (exclude captured pieces)
        """

        result = []

        for piece_id in range(32):

            if only_alive and self.pieceSquare[piece_id] == -1:
                continue

            if piece_type is not None:
                if self.pieceType[piece_id] != piece_type:
                    continue

            if color is not None:
                if self.pieceColor[piece_id] != color:
                    continue

            result.append(piece_id)

        return result   
    
    def get_legal_moves(self, piece_id):
        pseudo_moves= self.get_pseudo_moves(piece_id)

        if piece_id==self.WHITE_KING:
            moves=[move for move in pseudo_moves if not self.is_square_attacked(move, self.WHITE)]
            return moves
        elif piece_id==self.BLACK_KING:
            moves=[move for move in pseudo_moves if not self.is_square_attacked(move, self.BLACK)]
            return moves    
        else:
            return pseudo_moves 
        
        
        
    def exists(self, piece_type, color):
        for piece_id in range(32):
            if self.pieceSquare[piece_id] == -1:
                continue

            if self.pieceType[piece_id] == piece_type and \
            self.pieceColor[piece_id] == color:
                return True

        return False