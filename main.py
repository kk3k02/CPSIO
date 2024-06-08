import tkinter as tk
from app import App

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1550x650")
    root.configure(bg='white')
    app = App(root)
    root.mainloop()
