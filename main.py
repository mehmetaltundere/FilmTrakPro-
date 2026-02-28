import tkinter as tk
from ui import FilmTrakUI

def main():
    # [EN] Main application entry point
    # [TR] Uygulama ana giriş noktası
    root = tk.Tk()
    app = FilmTrakUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
