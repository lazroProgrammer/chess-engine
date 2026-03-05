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
    
    WHITE_ROOK1=8
    WHITE_ROOK2=9
    BLACK_ROOK1=24
    BLACK_ROOK2=25

    # ==============================
    # Color Constants
    # ==============================
    WHITE = 0
    BLACK = 1
    
    WQ = 0b1000
    WK = 0b0100
    BQ = 0b0010
    BK = 0b0001
    
    B1= 1
    C1= 2
    D1= 3
    F1= 5
    G1= 6
    B8= 57
    C8= 58
    D8= 59
    F8= 61
    G8= 62

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
        self.castlingRights = 0b1111  # WQ WK BQ BK
        self.enPassantSquare = None
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
        print(self.enPassantSquare)    
        self.enPassantSquare= None
        
        if( self.get_type(piece_id)== self.PAWN and abs(self.pieceSquare[piece_id] - to_square)==16):
            self.enPassantSquare= to_square
        
        if(piece_id == self.WHITE_KING):
            self.castlingRights &= 0b0011
        elif(piece_id == self.BLACK_KING):
            self.castlingRights &= 0b1100
        elif(piece_id == self.WHITE_ROOK1):
            self.castlingRights &= 0b0111
        elif(piece_id == self.WHITE_ROOK2):
            self.castlingRights &= 0b1011
        elif(piece_id == self.BLACK_ROOK1):
            self.castlingRights &= 0b1101
        elif(piece_id == self.BLACK_ROOK2):
            self.castlingRights &= 0b1110
            
        if( piece_id== self.WHITE_KING  and abs(to_square - self.pieceSquare[self.WHITE_KING]) > 1):
            if( to_square== self.G1):
                self.move_piece(self.WHITE_ROOK2, self.F1)
            if( to_square== self.C1):
                self.move_piece(self.WHITE_ROOK1, self.D1)
        if( piece_id== self.BLACK_KING  and abs(to_square - self.pieceSquare[self.BLACK_KING]) > 1 ):
            if( to_square== self.G8):
                self.move_piece(self.BLACK_ROOK2, self.F8)
            if( to_square== self.C8):
                self.move_piece(self.BLACK_ROOK1, self.D8)
        
        
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
                    if self.enPassantSquare:
                        target_piece = self.squarePiece[self.enPassantSquare]
                        enpassant_coordinates= self.get_coordinates(self.enPassantSquare)
                        if target_piece != -1 and self.pieceColor[target_piece] != color  and abs(new_col - enpassant_coordinates[1]) == 0 and abs(new_row - enpassant_coordinates[0]) == 1:
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
            
            if(piece_id == self.WHITE_KING):
                if(self.castlingRights & self.WK and self.squarePiece[self.G1]==-1 and self.squarePiece[self.F1]==-1 and not self.is_square_attacked(self.G1, self.WHITE)):
                    allowed_moves.append(self.G1)
                elif(self.castlingRights & self.WQ and self.squarePiece[self.B1]==-1 and self.squarePiece[self.C1]==-1 and self.squarePiece[self.D1]==-1 and not self.is_square_attacked(self.C1, self.WHITE)):
                    allowed_moves.append(self.C1)
                
            elif(piece_id == self.BLACK_KING):
                if(self.castlingRights & self.BK and self.squarePiece[self.G8]==-1 and self.squarePiece[self.F8]==-1 and not self.is_square_attacked(self.G8, self.BLACK)):
                    allowed_moves.append(self.G8)
                elif(self.castlingRights & self.BQ and self.squarePiece[self.B8]==-1 and self.squarePiece[self.C8]==-1 and self.squarePiece[self.D8]==-1 and not self.is_square_attacked(self.C8, self.BLACK)):
                    allowed_moves.append(self.C8)
            

            return allowed_moves

        # -------------------------
        # SLIDING PIECES
        # -------------------------
        if piece_type in offsets_increments:

            for dr, dc in offsets_increments[piece_type]:
                r, c = row + dr, col + dc

                while self.in_boundary((r, c)):
                    target = self.get_square((r, c))
                    target_piece = self.squarePiece[target]

                    # Empty square
                    if target_piece == -1:
                        allowed_moves.append(target)

                    # Occupied square
                    else:
                        # Enemy piece
                        if self.pieceColor[target_piece] != color:
                            # Skip enemy king for "attacked squares" calculation if needed
                            enemy_king_id = self.WHITE_KING if color == self.BLACK else self.BLACK_KING
                            if target_piece == enemy_king_id:
                                r += dr
                                c += dc
                                continue  # keep sliding past the enemy king

                            allowed_moves.append(target)

                        # Stop sliding in all other cases
                        break

                    # Move along the ray
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
    
    def get_legal_moves(self, piece_id, defender_color):
        pseudo_moves= self.get_pseudo_moves(piece_id)

        if piece_id==self.WHITE_KING and defender_color== self.WHITE:
            moves=[move for move in pseudo_moves if not self.is_square_attacked(move, self.WHITE)]
            return moves
        elif piece_id==self.BLACK_KING and defender_color== self.BLACK:
            moves=[move for move in pseudo_moves if not self.is_square_attacked(move, self.BLACK)]
            return moves    
        else:
            king= self.WHITE_KING if defender_color== self.WHITE else self.BLACK_KING
            king_attackers=self.get_checkers(defender_color)
            if(len(king_attackers) == 0):
                return pseudo_moves 
            elif(len(king_attackers)== 1):
                ray= self.get_blocking_squares(king_attackers[0], defender_color)
                print(ray)
                return [e for e in ray if e in pseudo_moves]
            else:
                return []
                
        
        
        
    def exists(self, piece_type, color):
        for piece_id in range(32):
            if self.pieceSquare[piece_id] == -1:
                continue

            if self.pieceType[piece_id] == piece_type and \
            self.pieceColor[piece_id] == color:
                return True

        return False
    
    
    def get_checkers(self, color):

        king_id = self.WHITE_KING if color == self.WHITE else self.BLACK_KING
        king_square = self.pieceSquare[king_id]
        row, col = self.get_coordinates(king_square)

        enemy_color = self.BLACK if color == self.WHITE else self.WHITE
        checkers = []

        # ==================================
        # Pawn checks
        # ==================================
        pawn_direction = -1 if color == self.WHITE else 1

        for dc in (-1, 1):
            r = row + pawn_direction
            c = col + dc
            if self.in_boundary((r, c)):
                sq = self.get_square((r, c))
                pid = self.squarePiece[sq]
                if pid != -1 and \
                self.pieceType[pid] == self.PAWN and \
                self.pieceColor[pid] == enemy_color:
                    checkers.append(pid)

        # ==================================
        # Knight checks
        # ==================================
        knight_offsets = [(2,1),(1,2),(-2,1),(-1,2),
                        (2,-1),(1,-2),(-2,-1),(-1,-2)]

        for dr, dc in knight_offsets:
            r = row + dr
            c = col + dc
            if self.in_boundary((r, c)):
                sq = self.get_square((r, c))
                pid = self.squarePiece[sq]
                if pid != -1 and \
                self.pieceType[pid] == self.KNIGHT and \
                self.pieceColor[pid] == enemy_color:
                    checkers.append(pid)

        # ==================================
        # Sliding checks
        # ==================================
        directions = [
            (1,0), (-1,0), (0,1), (0,-1),       # rook dirs
            (1,1), (1,-1), (-1,1), (-1,-1)      # bishop dirs
        ]

        for dr, dc in directions:
            r = row + dr
            c = col + dc

            while self.in_boundary((r, c)):
                sq = self.get_square((r, c))
                pid = self.squarePiece[sq]

                if pid == -1:
                    r += dr
                    c += dc
                    continue

                if self.pieceColor[pid] == enemy_color:
                    ptype = self.pieceType[pid]

                    is_rook_dir = (dr == 0 or dc == 0)
                    is_bishop_dir = (abs(dr) == abs(dc))

                    if (
                        (is_rook_dir and ptype in (self.ROOK, self.QUEEN)) or
                        (is_bishop_dir and ptype in (self.BISHOP, self.QUEEN))
                    ):
                        checkers.append(pid)

                break  # stop at first piece

        return checkers
    
    def get_blocking_squares(self, attacker_id, defender_color):
        """
        Returns the squares that can be used to block a check or capture the attacking piece.

        attacker_id: the piece giving the check
        defender_color: the color of the king being checked

        Returns:
            List of squares along the ray between the king and the attacker, 
            including the attacker's square. For pawns/knights, returns only the attacker's square.
        """
        king_id = self.WHITE_KING if defender_color == self.WHITE else self.BLACK_KING
        king_square = self.pieceSquare[king_id]
        attacker_square = self.pieceSquare[attacker_id]
        attacker_type = self.pieceType[attacker_id]

        # For pawns and knights, only capturing the piece can stop the check
        if attacker_type in (self.PAWN, self.KNIGHT):
            return [attacker_square]

        # For sliding pieces, compute ray
        kr, kc = self.get_coordinates(king_square)
        ar, ac = self.get_coordinates(attacker_square)

        dr = (ar - kr)
        dc = (ac - kc)

        # Normalize direction to -1, 0, or 1
        dr = (dr > 0) - (dr < 0)
        dc = (dc > 0) - (dc < 0)

        # Collect squares along the ray (excluding king, include attacker)
        r, c = kr + dr, kc + dc
        ray_squares = []
        while (r, c) != (ar, ac):
            ray_squares.append(self.get_square((r, c)))
            r += dr
            c += dc

        ray_squares.append(attacker_square)
        return ray_squares