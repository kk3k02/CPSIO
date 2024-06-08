from tkinter import *
from app import App


if __name__ == '__main__':
    root = Tk()
    root.geometry("1300x650")
    root.configure(bg='white')
    app = App(root)
    root.mainloop()
