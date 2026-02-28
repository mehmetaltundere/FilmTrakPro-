import tkinter as tk
from ui import FilmTrakUI

def main():
    root = tk.Tk()
    app = FilmTrakUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
