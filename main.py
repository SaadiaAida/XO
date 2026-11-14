# main.py
"""نقطة انطلاق اللعبة"""

import tkinter as tk
from ui import XOGameUI


def main():
    root = tk.Tk()
    try:
        root.iconbitmap()  # اختياري على ويندوز
    except Exception:
        pass
    app = XOGameUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()