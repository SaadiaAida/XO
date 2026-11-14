# game_logic.py
"""منطق لعبة XO مستقل عن الواجهة"""

from styles import BOARD_SIZE


class XOGame:
    """كلاس يدير حالة اللعبة والمنطق"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """إعادة تعيين اللعبة"""
        self.board = [""] * (BOARD_SIZE * BOARD_SIZE)
        self.current_player = "X"
        self.winner = None
        self.winning_line = None
        self.game_over = False
        self.move_count = 0
        self.scores = getattr(self, "scores", {"X": 0, "O": 0, "draw": 0})
    
    def reset_scores(self):
        """إعادة تعيين النتائج"""
        self.scores = {"X": 0, "O": 0, "draw": 0}
    
    def is_valid_move(self, index):
        """التحقق من صحة الحركة"""
        return (
            not self.game_over
            and 0 <= index < len(self.board)
            and self.board[index] == ""
        )
    
    def make_move(self, index):
        """تنفيذ حركة وإرجاع True إذا نجحت"""
        if not self.is_valid_move(index):
            return False
        
        self.board[index] = self.current_player
        self.move_count += 1
        
        if self._check_winner():
            return True
        
        if self.move_count == len(self.board):
            self.game_over = True
            self.winner = "draw"
            self.scores["draw"] += 1
            return True
        
        self.current_player = "O" if self.current_player == "X" else "X"
        return True
    
    def _check_winner(self):
        """التحقق من وجود فائز"""
        lines = self._winning_lines()
        
        for line in lines:
            a, b, c = line
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                self.winner = self.board[a]
                self.winning_line = line
                self.game_over = True
                self.scores[self.winner] += 1
                return True
        
        return False
    
    @staticmethod
    def _winning_lines():
        """جميع الخطوط الفائزة الممكنة"""
        n = BOARD_SIZE
        lines = []
        
        # صفوف
        for row in range(n):
            lines.append(tuple(row * n + col for col in range(n)))
        
        # أعمدة
        for col in range(n):
            lines.append(tuple(row * n + col for row in range(n)))
        
        # قطر رئيسي
        lines.append(tuple(i * n + i for i in range(n)))
        
        # قطر ثانوي
        lines.append(tuple(i * n + (n - 1 - i) for i in range(n)))
        
        return lines