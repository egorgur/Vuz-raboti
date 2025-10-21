import tkinter as tk

from cipher import MagicSquareCipher
from gui_gtk import CipherGUI


def main():
    """Главная функция"""
    # root = tk.Tk()
    app = CipherGUI(cipher=MagicSquareCipher())
    app.run()
    # root.mainloop()


if __name__ == "__main__":
    main()
