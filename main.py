import tkinter as tk
from tkinter import ttk

from gui import App


def main():
    root = tk.Tk()
    try:
        estilo = ttk.Style()
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
    except Exception:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
