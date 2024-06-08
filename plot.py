"""
Moduł `Plot` do wizualizacji sygnałów EKG i analizy częstotliwościowej.

Ten moduł zawiera klasę `Plot`, która umożliwia tworzenie, aktualizację i wyświetlanie wykresów sygnałów EKG
oraz przeprowadzanie analizy częstotliwościowej przy użyciu bibliotek Matplotlib i Scipy.

Klasy:
--------
Plot :
    Klasa odpowiedzialna za tworzenie wykresów, aktualizację danych wykresów oraz analizę częstotliwościową.

Metody:
-------
__init__(self, master):
    Inicjalizuje obiekt `Plot` oraz ustawia elementy interfejsu graficznego do wyświetlania wykresów.

    Parametry:
    ----------
    master : Tk
        Główne okno aplikacji Tkinter.

update_Plot(self, time, signal, start_time, end_time, min_amp, max_amp, title, xlabel, ylabel):
    Aktualizuje wykres sygnału EKG na podstawie dostarczonych danych.

    Parametry:
    ----------
    time : array_like
        Tablica wartości czasu.
    signal : array_like
        Tablica wartości sygnału EKG.
    start_time : float
        Czas początkowy wyświetlanego wykresu.
    end_time : float
        Czas końcowy wyświetlanego wykresu.
    min_amp : float
        Minimalna amplituda wyświetlanego wykresu.
    max_amp : float
        Maksymalna amplituda wyświetlanego wykresu.
    title : str
        Tytuł wykresu.
    xlabel : str
        Etykieta osi X.
    ylabel : str
        Etykieta osi Y.

show_frequency_analysis(self, signal, frequency):
    Wyświetla analizę częstotliwościową sygnału EKG.

    Parametry:
    ----------
    signal : array_like
        Tablica wartości sygnału EKG.
    frequency : float
        Częstotliwość próbkowania sygnału.

butter_lowpass(cut_off, fs, order):
    Statyczna metoda tworząca dolnoprzepustowy filtr Butterwortha.

    Parametry:
    ----------
    cut_off : float
        Częstotliwość odcięcia filtru.
    fs : float
        Częstotliwość próbkowania sygnału.
    order : int
        Rząd filtru.

    Zwraca:
    -------
    b : ndarray
        Współczynniki filtru (b).
    a : ndarray
        Współczynniki filtru (a).

butter_highpass(cut_off, fs, order):
    Statyczna metoda tworząca górnoprzepustowy filtr Butterwortha.

    Parametry:
    ----------
    cut_off : float
        Częstotliwość odcięcia filtru.
    fs : float
        Częstotliwość próbkowania sygnału.
    order : int
        Rząd filtru.

    Zwraca:
    -------
    b : ndarray
        Współczynniki filtru (b).
    a : ndarray
        Współczynniki filtru (a).
"""

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.fft import fft
from scipy.signal import butter


class Plot:
    def __init__(self, master):
        self.master = master
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=12)
        self.line = None

    def update_Plot(self, time, signal, start_time, end_time, min_amp, max_amp, title, xlabel, ylabel):
        if self.line:
            self.line.remove()
        self.plot.clear()
        self.plot.plot(time, signal, label="EKG Signal")
        self.plot.set_xlim(start_time, end_time)
        self.plot.set_ylim(min_amp, max_amp)
        self.plot.set_title(title)
        self.plot.set_xlabel(xlabel)
        self.plot.set_ylabel(ylabel)
        self.plot.grid(True)
        self.canvas.draw()
        self.line = self.plot.lines[0]

    def show_frequency_analysis(self, signal, frequency):
        self.plot.clear()
        N = len(signal)
        T = 1 / frequency
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
        yf = fft(signal)
        self.plot.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
        self.plot.set_title("Frequency Analysis")
        self.plot.set_xlabel("Frequency [Hz]")
        self.plot.set_ylabel("Amplitude")
        self.canvas.draw()

    @staticmethod
    def butter_lowpass(cut_off, fs, order):
        """
        Create a Butterworth low-pass filter.
        """
        nyquist = 0.5 * fs
        normal_cutoff = cut_off / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    @staticmethod
    def butter_highpass(cut_off, fs, order):
        """
        Create a Butterworth high-pass filter.
        """
        nyquist = 0.5 * fs
        normal_cutoff = cut_off / nyquist
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a
