import tkinter as tk
from interface import ClockApp

def main():
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
