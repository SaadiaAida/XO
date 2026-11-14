# ui.py
"""واجهة اللعبة الرسومية باستخدام Tkinter"""

import tkinter as tk
from tkinter import messagebox
from styles import Colors, Fonts, BOARD_SIZE, CELL_SIZE
from game_logic import XOGame


class XOGameUI:
    """الواجهة الرئيسية للعبة"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("لعبة XO")
        self.root.configure(bg=Colors.BG_MAIN)
        self.root.resizable(False, False)
        
        self.game = XOGame()
        self.buttons = []
        self._hovered = None
        
        self._center_window()
        self._build_ui()
    
    # ---------- بناء الواجهة ----------
    
    def _center_window(self):
        """توسيط النافذة على الشاشة"""
        self.root.update_idletasks()
        w, h = 420, 640
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
    
    def _build_ui(self):
        """بناء كل عناصر الواجهة"""
        main_frame = tk.Frame(self.root, bg=Colors.BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self._build_header(main_frame)
        self._build_score_panel(main_frame)
        self._build_board(main_frame)
        self._build_status(main_frame)
        self._build_controls(main_frame)
    
    def _build_header(self, parent):
        tk.Label(
            parent, text="🎮 لعبة XO",
            font=Fonts.TITLE,
            bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY
        ).pack(pady=(0, 5))
        
        tk.Label(
            parent, text="لاعب ضد لاعب",
            font=Fonts.SUBTITLE,
            bg=Colors.BG_MAIN, fg=Colors.TEXT_SECONDARY
        ).pack(pady=(0, 15))
    
    def _build_score_panel(self, parent):
        """لوحة عرض النتائج"""
        frame = tk.Frame(parent, bg=Colors.BG_PANEL)
        frame.pack(fill="x", pady=(0, 15))
        
        # لاعب X
        x_frame = tk.Frame(frame, bg=Colors.BG_PANEL)
        x_frame.pack(side="left", expand=True, pady=10)
        tk.Label(x_frame, text="X", font=("Segoe UI", 18, "bold"),
                 bg=Colors.BG_PANEL, fg=Colors.X_COLOR).pack()
        self.x_score_label = tk.Label(
            x_frame, text="0", font=Fonts.SCORE,
            bg=Colors.BG_PANEL, fg=Colors.TEXT_PRIMARY
        )
        self.x_score_label.pack()
        
        # تعادل
        d_frame = tk.Frame(frame, bg=Colors.BG_PANEL)
        d_frame.pack(side="left", expand=True, pady=10)
        tk.Label(d_frame, text="تعادل", font=("Segoe UI", 12, "bold"),
                 bg=Colors.BG_PANEL, fg=Colors.TEXT_SECONDARY).pack()
        self.draw_score_label = tk.Label(
            d_frame, text="0", font=Fonts.SCORE,
            bg=Colors.BG_PANEL, fg=Colors.TEXT_PRIMARY
        )
        self.draw_score_label.pack()
        
        # لاعب O
        o_frame = tk.Frame(frame, bg=Colors.BG_PANEL)
        o_frame.pack(side="left", expand=True, pady=10)
        tk.Label(o_frame, text="O", font=("Segoe UI", 18, "bold"),
                 bg=Colors.BG_PANEL, fg=Colors.O_COLOR).pack()
        self.o_score_label = tk.Label(
            o_frame, text="0", font=Fonts.SCORE,
            bg=Colors.BG_PANEL, fg=Colors.TEXT_PRIMARY
        )
        self.o_score_label.pack()
    
    def _build_board(self, parent):
        """شبكة اللعب"""
        board_frame = tk.Frame(parent, bg=Colors.BG_MAIN)
        board_frame.pack(pady=10)
        
        for i in range(BOARD_SIZE * BOARD_SIZE):
            btn = tk.Button(
                board_frame,
                text="",
                font=Fonts.CELL,
                width=3, height=1,
                bg=Colors.BG_CELL,
                fg=Colors.TEXT_PRIMARY,
                activebackground=Colors.BG_CELL_HOVER,
                activeforeground=Colors.TEXT_PRIMARY,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda idx=i: self._on_cell_click(idx),
            )
            row, col = divmod(i, BOARD_SIZE)
            btn.grid(row=row, column=col, padx=4, pady=4,
                     ipadx=4, ipady=4)
            
            btn.bind("<Enter>", lambda e, b=btn, idx=i: self._on_hover(b, idx, True))
            btn.bind("<Leave>", lambda e, b=btn, idx=i: self._on_hover(b, idx, False))
            
            self.buttons.append(btn)
    
    def _build_status(self, parent):
        self.status_label = tk.Label(
            parent,
            text="دور اللاعب: X",
            font=Fonts.STATUS,
            bg=Colors.BG_MAIN, fg=Colors.X_COLOR
        )
        self.status_label.pack(pady=15)
    
    def _build_controls(self, parent):
        """أزرار التحكم"""
        frame = tk.Frame(parent, bg=Colors.BG_MAIN)
        frame.pack(pady=5)
        
        self._create_button(
            frame, "🔄 لعبة جديدة", self._new_game,
            Colors.BG_BUTTON, Colors.BG_BUTTON_HOVER
        ).pack(side="left", padx=5)
        
        self._create_button(
            frame, "🗑️ تصفير النتائج", self._reset_scores,
            Colors.BG_BUTTON_SECONDARY, Colors.BG_BUTTON_SECONDARY_HOVER
        ).pack(side="left", padx=5)
    
    def _create_button(self, parent, text, command, bg, hover_bg):
        btn = tk.Button(
            parent, text=text, command=command,
            font=Fonts.BUTTON, bg=bg, fg=Colors.TEXT_PRIMARY,
            activebackground=hover_bg, activeforeground=Colors.TEXT_PRIMARY,
            relief="flat", bd=0, padx=15, pady=8, cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn
    
    # ---------- التفاعلات ----------
    
    def _on_hover(self, button, index, entering):
        """تأثير التحويم على الخلايا"""
        if self.game.game_over or self.game.board[index]:
            return
        button.configure(bg=Colors.BG_CELL_HOVER if entering else Colors.BG_CELL)
    
    def _on_cell_click(self, index):
        """عند الضغط على خلية"""
        if not self.game.make_move(index):
            return
        
        self._render_board()
        
        if self.game.game_over:
            self._handle_game_over()
        else:
            self._update_status()
    
    # ---------- الرسم والتحديث ----------
    
    def _render_board(self):
        """تحديث عرض الخلايا"""
        for i, value in enumerate(self.game.board):
            btn = self.buttons[i]
            btn.configure(
                text=value,
                fg=Colors.X_COLOR if value == "X" else Colors.O_COLOR,
                state="disabled",
                disabledforeground=Colors.X_COLOR if value == "X" else Colors.O_COLOR,
            )
            if not value:
                btn.configure(state="normal", bg=Colors.BG_CELL)
        
        # تمييز خط الفوز
        if self.game.winning_line:
            for idx in self.game.winning_line:
                self.buttons[idx].configure(bg=Colors.WIN_HIGHLIGHT)
    
    def _update_status(self):
        player = self.game.current_player
        color = Colors.X_COLOR if player == "X" else Colors.O_COLOR
        self.status_label.configure(text=f"دور اللاعب: {player}", fg=color)
    
    def _update_scores(self):
        self.x_score_label.configure(text=str(self.game.scores["X"]))
        self.o_score_label.configure(text=str(self.game.scores["O"]))
        self.draw_score_label.configure(text=str(self.game.scores["draw"]))
    
    def _handle_game_over(self):
        self._update_scores()
        
        if self.game.winner == "draw":
            self.status_label.configure(text="🤝 تعادل!", fg=Colors.DRAW_COLOR)
        else:
            color = Colors.X_COLOR if self.game.winner == "X" else Colors.O_COLOR
            self.status_label.configure(
                text=f"🏆 فاز اللاعب {self.game.winner}!",
                fg=color
            )
        
        self.root.after(300, self._show_result_dialog)
    
    def _show_result_dialog(self):
        if self.game.winner == "draw":
            msg = "انتهت اللعبة بالتعادل!"
            title = "تعادل"
        else:
            msg = f"فاز اللاعب {self.game.winner}! 🎉"
            title = "فوز"
        
        answer = messagebox.askyesno(
            title, f"{msg}\n\nهل تريد لعب جولة أخرى؟", parent=self.root
        )
        if answer:
            self._new_game()
    
    # ---------- التحكم ----------
    
    def _new_game(self):
        """بدء لعبة جديدة مع الاحتفاظ بالنتائج"""
        self.game.reset()
        self._reset_board_visuals()
        self._update_status()
    
    def _reset_scores(self):
        """تصفير كل شيء"""
        self.game.reset_scores()
        self._new_game()
        self._update_scores()
    
    def _reset_board_visuals(self):
        for btn in self.buttons:
            btn.configure(
                text="", state="normal",
                bg=Colors.BG_CELL, fg=Colors.TEXT_PRIMARY
            )