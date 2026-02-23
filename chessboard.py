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
        pawns=[i for i in range(8)]
        pawns.extend([i for i in range(16,24)]),
        pieces=[
                pawns,
                [8,9,24,25],
                [10,11,26,27],
                [12,13,28,29],
                [14,30],
                [15,31]]
        if(piece_num==-1):
            return None
        elif(piece_num in pieces[0]):
            return ChessBoard.PAWN
        elif(piece_num in pieces[1]):
            return ChessBoard.ROOK
        elif(piece_num in pieces[2]):
            return ChessBoard.KNIGHT
        elif(piece_num in pieces[3]):
            return ChessBoard.BISHOP
        elif(piece_num in pieces[4]):
            return ChessBoard.QUEEN
        elif(piece_num in pieces[5]):
            return ChessBoard.KING
    
    def get_color(self, piece_num):
        # TODO: add promotion stuff here if you change number or change piece_num cast for that game
        if(piece_num<0):
            return ""
        if(piece_num < 16):
            return "w"
        elif(piece_num <32):
            return "b"
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
    def get_legal_moves(self, piece):
        allowed_moves=[]
        square=self.pieceSquare[piece]
        if(self.get_type(piece)== ChessBoard.PAWN ):
            if(self.get_color(piece)=="w"):
                if(square+7 <64 and self.get_color(self.squarePiece[square+7])== "b"):
                    allowed_moves.append(square + 7)
                if(square + 9 < 64 and self.get_color(self.squarePiece[square+9])== "b"):
                    allowed_moves.append(square + 9)
                if(square + 8 < 64 and  self.squarePiece[square + 8] == -1):
                    allowed_moves.append(square + 8) 
                    if(self.is_pawn_in_start(piece) and square + 16 < 64  and self.squarePiece[square + 16] == -1):
                        allowed_moves.append(square + 16)
            elif(self.get_color(piece)=="b"):    
                if(square - 7 >= 0 and self.get_color(self.squarePiece[square-7])== "w"):
                    print
                    allowed_moves.append(square - 7)
                if(square - 9 >= 0 and self.get_color(self.squarePiece[square-9])== "w"):
                    allowed_moves.append(square - 9)
                if(square - 8 >= 0 and self.squarePiece[square - 8] == -1):
                    allowed_moves.append(square - 8) 
                    if(square - 16 >= 0 and self.is_pawn_in_start(piece) and self.squarePiece[square - 16] == -1):
                        allowed_moves.append(square - 16)
        elif(self.get_type(piece)== ChessBoard.ROOK):
            allowed_moves.extend([i for i in range(square // 8 * 8, min((square//8 + 1 ) * 8 ,64))])
            allowed_moves.extend([i for i in range(square % 8, 64, 8 )])
        elif(self.get_type(piece)== ChessBoard.KNIGHT):
            moves_delta=[(1,6), (1,10), (2,17), (2,15)]

            for (a,i) in moves_delta:
                if( square - i >= 0 and self.squarePiece[square -i] == -1 and square // 8 - a == (square - i)//8):
                    allowed_moves.append(square - i)
                if( square + i < 64 and self.squarePiece[square +i] == -1 and square // 8 + a == (square + i)//8):
                    allowed_moves.append(square + i)
        # elif(self.get_type(piece)== ChessBoard.BISHOP):
        # elif(self.get_type(piece)== ChessBoard.QUEEN):
        # elif(self.get_type(piece)== ChessBoard.KING):
        return allowed_moves
                

                

