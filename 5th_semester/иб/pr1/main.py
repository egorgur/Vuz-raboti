import tkinter as tk

from cipher import MagicSquareCipher
from gui import CipherGUI


def main():
    """Главная функция"""
    root = tk.Tk()
    app = CipherGUI(root, cipher=MagicSquareCipher())
    root.mainloop()


if __name__ == "__main__":
    main()
