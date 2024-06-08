import tkinter as tk
from app import App

# Tworzenie głównego okna aplikacji i ustawianie jego parametrów
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1300x650")  # Ustawia rozmiar okna głównego
    root.configure(bg='white')  # Ustawia kolor tła okna głównego
    app = App(root)  # Inicjalizuje aplikację i przekazuje główne okno
    root.mainloop()  # Uruchamia główną pętlę zdarzeń interfejsu użytkownika
