"""
Główna część aplikacji uruchamiającej GUI do analizy sygnałów EKG.

Ten moduł tworzy główne okno aplikacji Tkinter i uruchamia interfejs graficzny użytkownika,
który pozwala na wczytywanie, przetwarzanie i wizualizację sygnałów EKG za pomocą klasy `App`.

Sposób użycia:
-------------
Uruchomienie tego modułu spowoduje otwarcie okna aplikacji o rozmiarze 1300x650 pikseli,
z białym tłem, w którym będzie działać aplikacja `App`.

Kod:
----
import tkinter as tk
from app import App

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1300x650")
    root.configure(bg='white')
    app = App(root)
    root.mainloop()

Zmienne:
--------
root : Tk
    Główne okno aplikacji Tkinter.
app : App
    Instancja klasy `App` odpowiedzialna za funkcjonalność aplikacji.
"""


import tkinter as tk
from app import App

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1300x650")
    root.configure(bg='white')
    app = App(root)
    root.mainloop()
