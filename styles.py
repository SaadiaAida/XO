# styles.py
"""ملف يحتوي على الألوان والخطوط المستخدمة في اللعبة"""

class Colors:
    # الخلفية الأساسية
    BG_MAIN = "#1e1e2e"
    BG_PANEL = "#2a2a3e"
    BG_CELL = "#313145"
    BG_CELL_HOVER = "#3d3d5c"
    BG_BUTTON = "#7c3aed"
    BG_BUTTON_HOVER = "#9333ea"
    BG_BUTTON_SECONDARY = "#3f3f5c"
    BG_BUTTON_SECONDARY_HOVER = "#52527a"
    
    # النصوص
    TEXT_PRIMARY = "#f8f8f2"
    TEXT_SECONDARY = "#a1a1c0"
    
    # رموز اللاعبين
    X_COLOR = "#ff5555"    # أحمر
    O_COLOR = "#50fa7b"    # أخضر
    
    # حالات اللعبة
    WIN_HIGHLIGHT = "#ffd700"
    DRAW_COLOR = "#ffb86c"
    
    # الحدود
    BORDER = "#44475a"


class Fonts:
    TITLE = ("Segoe UI", 24, "bold")
    SUBTITLE = ("Segoe UI", 12)
    CELL = ("Segoe UI", 40, "bold")
    BUTTON = ("Segoe UI", 12, "bold")
    STATUS = ("Segoe UI", 14, "bold")
    SCORE = ("Segoe UI", 14, "bold")


# أبعاد اللعبة
BOARD_SIZE = 3
CELL_SIZE = 110