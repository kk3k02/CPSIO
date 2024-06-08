"""
Moduł aplikacji do analizy sygnałów EKG z interfejsem graficznym w Tkinter.

Ten moduł zawiera klasę `App`, która implementuje aplikację do wczytywania, przetwarzania
i wizualizacji sygnałów EKG. Aplikacja umożliwia użytkownikowi wczytanie sygnału z pliku,
wyświetlenie wykresu sygnału EKG, zastosowanie filtrów wysokoprzepustowych i niskoprzepustowych,
przeprowadzenie analizy FFT oraz zapisanie wykresu do pliku.

Klasy:
--------
App :
    Główna klasa aplikacji, zawierająca metody do obsługi GUI oraz przetwarzania sygnałów.

Zmienne klasowe:
----------------
time : float
    Czas sygnału EKG.
signal : ndarray
    Tablica wartości sygnału EKG.
length : int
    Długość sygnału EKG.

Metody:
-------
__init__(self, master):
    Inicjalizuje główne okno aplikacji oraz elementy interfejsu użytkownika.

    Parametry:
    ----------
    master : Tk
        Główne okno aplikacji Tkinter.

loadFile():
    Wczytuje plik z sygnałem EKG i aktywuje odpowiednie pola wejściowe.
    Nie przyjmuje żadnych parametrów ani nie zwraca wartości.

show_plot():
    Wyświetla wykres sygnału EKG na podstawie wczytanych danych oraz ustawień użytkownika.

    Parametry:
    ----------
    frequency : float
        Częstotliwość próbkowania sygnału EKG.
    start_time : float
        Czas początkowy wyświetlanego wykresu.
    end_time : float
        Czas końcowy wyświetlanego wykresu.
    min_amp : float
        Minimalna amplituda wyświetlanego wykresu.
    max_amp : float
        Maksymalna amplituda wyświetlanego wykresu.
    lab_x : str
        Etykieta osi X.
    lab_y : str
        Etykieta osi Y.

show_sin_plot():
    Generuje i wyświetla wykres sinusoidy o zadanych parametrach.

    Parametry:
    ----------
    start_time : float
        Czas początkowy wyświetlanego wykresu.
    end_time : float
        Czas końcowy wyświetlanego wykresu.
    min_amp : float
        Minimalna amplituda sygnału.
    max_amp : float
        Maksymalna amplituda sygnału.

show_2sin_plot():
    Generuje i wyświetla wykres sumy dwóch sinusoid o różnych częstotliwościach.

    Parametry:
    ----------
    start_time : float
        Czas początkowy wyświetlanego wykresu.
    end_time : float
        Czas końcowy wyświetlanego wykresu.
    min_amp : float
        Minimalna amplituda sygnału.
    max_amp : float
        Maksymalna amplituda sygnału.

do_fft():
    Przeprowadza analizę FFT na wczytanym sygnale EKG i wyświetla widmo amplitudowe.
    Nie przyjmuje żadnych parametrów ani nie zwraca wartości.

do_ifft():
    Przeprowadza odwrotną transformację FFT na wczytanym sygnale EKG i wyświetla przetworzony sygnał.

    Parametry:
    ----------
    start_time : float
        Czas początkowy wyświetlanego wykresu.
    end_time : float
        Czas końcowy wyświetlanego wykresu.

save_plot():
    Zapisuje aktualnie wyświetlany wykres do pliku w formacie PNG, JPEG lub PDF.
    Nie przyjmuje żadnych parametrów ani nie zwraca wartości.

check_entries():
    Sprawdza, czy wszystkie wymagane pola wejściowe zostały wypełnione i odpowiednio aktywuje przyciski.
    Nie przyjmuje żadnych parametrów ani nie zwraca wartości.

Zmienne instancyjne:
--------------------
master : Tk
    Główne okno aplikacji Tkinter.
path : str
    Ścieżka do pliku z sygnałem EKG.
frequency_entry : Entry
    Pole wejściowe dla częstotliwości próbkowania.
start_time_entry : Entry
    Pole wejściowe dla czasu początkowego wykresu.
end_time_entry : Entry
    Pole wejściowe dla czasu końcowego wykresu.
min_amp_entry : Entry
    Pole wejściowe dla minimalnej amplitudy wykresu.
max_amp_entry : Entry
    Pole wejściowe dla maksymalnej amplitudy wykresu.
showEKG_button : Button
    Przycisk do wyświetlania wykresu sygnału EKG.
showSin_button : Button
    Przycisk do wyświetlania wykresu sinusoidy.
show2Sin_button : Button
    Przycisk do wyświetlania wykresu sumy dwóch sinusoid.
fft_button : Button
    Przycisk do przeprowadzania analizy FFT.
ifft_button : Button
    Przycisk do przeprowadzania odwrotnej transformacji FFT.
save_button : Button
    Przycisk do zapisywania wykresu do pliku.
label_x : str
    Etykieta osi X wykresu.
label_y : str
    Etykieta osi Y wykresu.
label_x_entry : Entry
    Pole wejściowe dla etykiety osi X.
label_y_entry : Entry
    Pole wejściowe dla etykiety osi Y.
fq_status : BooleanVar
    Zmienna określająca status checkboxu analizy częstotliwościowej.
fq_anal_c : Checkbutton
    Checkbox do wyboru analizy częstotliwościowej.
fl_high_c : Checkbutton
    Checkbox do wyboru filtra wysokoprzepustowego.
fl_low_c : Checkbutton
    Checkbox do wyboru filtra niskoprzepustowego.
fl_high_status : BooleanVar
    Zmienna określająca status checkboxu filtra wysokoprzepustowego.
fl_low_status : BooleanVar
    Zmienna określająca status checkboxu filtra niskoprzepustowego.
fl_high_entry : Entry
    Pole wejściowe dla częstotliwości odcięcia filtra wysokoprzepustowego.
fl_low_entry : Entry
    Pole wejściowe dla częstotliwości odcięcia filtra niskoprzepustowego.
sample_fq_low_entry : Entry
    Pole wejściowe dla częstotliwości próbkowania sygnału dla filtra niskoprzepustowego.
sample_fq_high_entry : Entry
    Pole wejściowe dla częstotliwości próbkowania sygnału dla filtra wysokoprzepustowego.
fl_order_low_entry : Entry
    Pole wejściowe dla rzędu filtra niskoprzepustowego.
fl_order_high_entry : Entry
    Pole wejściowe dla rzędu filtra wysokoprzepustowego.
apply_button : Button
    Przycisk do zastosowania ustawień i wyświetlenia wykresu.
base_signal : ndarray
    Tablica wartości pierwotnego sygnału EKG.
new_signal : ndarray
    Tablica wartości przetworzonego sygnału EKG.
"""

import tkinter as tk
from tkinter import filedialog, BooleanVar
import numpy as np
import matplotlib.pyplot as plt
from readFile import File
from scipy.fft import fft, fftfreq, ifft
from scipy.signal import filtfilt
from plot import Plot


class App:
    time, signal, length = 0, 0, 0

    def __init__(self, master):
        self.master = master
        self.master.title('CPSIO EKG')
        self.path = ""
        self.frequency_entry = None
        self.start_time_entry = None
        self.end_time_entry = None
        self.min_amp_entry = None
        self.max_amp_entry = None
        self.showEKG_button = None
        self.showSin_button = None
        self.show2Sin_button = None
        self.fft_button = None
        self.ifft_button = None
        self.save_button = None
        self.label_x = ""
        self.label_y = ""
        self.label_x_entry = None
        self.label_y_entry = None
        self.fq_status = BooleanVar()
        self.fq_anal_c = None
        self.fl_high_c = None
        self.fl_low_c = None
        self.fl_high_status = BooleanVar()
        self.fl_low_status = BooleanVar()
        self.fl_high_entry = None
        self.fl_low_entry = None
        self.sample_fq_low_entry = None
        self.sample_fq_high_entry = None
        self.fl_order_low_entry = None
        self.fl_order_high_entry = None
        self.apply_button = None
        self.base_signal = None
        self.new_signal = None

        # Function definitions at the beginning
        def loadFile():
            self.path = filedialog.askopenfilename(initialdir="/", title="Select EKG signal file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
            # Activate entry fields after loading a file
            self.frequency_entry.config(state='normal')
            self.start_time_entry.config(state='normal')
            self.end_time_entry.config(state='normal')
            self.min_amp_entry.config(state='normal')
            self.max_amp_entry.config(state='normal')
            self.label_x_entry.config(state='normal')
            self.label_y_entry.config(state='normal')

        def show_plot():
            frequency = float(self.frequency_entry.get())
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            min_amp = float(self.min_amp_entry.get())
            max_amp = float(self.max_amp_entry.get())
            lab_x = self.label_x_entry.get()
            lab_y = self.label_y_entry.get()
            file = File(self.path, frequency=frequency)
            App.time, App.signal = file.load_EKG()
            App.length = len(App.signal)  # Directly calculate the length of the signal

            if self.fq_status.get():
                self.plot_signal.show_frequency_analysis(App.signal, frequency)
            else:
                self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, min_amp, max_amp, "EKG SIGNAL",
                                             lab_x, lab_y)

            if self.fl_high_status.get():
                if self.fl_high_entry.get() and self.sample_fq_high_entry.get() and self.fl_order_high_entry.get():
                    cut_off = float(self.fl_high_entry.get())
                    fs = float(self.sample_fq_high_entry.get())
                    order = float(self.fl_order_high_entry.get())
                    b, a = self.plot_signal.butter_highpass(cut_off, fs, order)
                    filtered_signal = filtfilt(b, a, App.signal)
                    self.plot_signal.update_Plot(App.time, filtered_signal, start_time, end_time, min_amp, max_amp,
                                                 "EKG SIGNAL", lab_x, lab_y)
                    self.new_signal = filtered_signal

            if self.fl_low_status.get():
                if self.fl_low_entry.get() and self.sample_fq_low_entry.get() and self.fl_order_low_entry.get():
                    cut_off = float(self.fl_low_entry.get())
                    fs = float(self.sample_fq_low_entry.get())
                    order = float(self.fl_order_low_entry.get())
                    b, a = self.plot_signal.butter_lowpass(cut_off, fs, order)
                    filtered_signal = filtfilt(b, a, self.new_signal)
                    self.plot_signal.update_Plot(App.time, filtered_signal, start_time, end_time, min_amp, max_amp,
                                                 "EKG SIGNAL", lab_x, lab_y)
                    self.new_signal = filtered_signal

            self.save_button.config(state='normal')  # Activate save button after showing a plot
            self.fq_anal_c.config(state='normal')  # Activate frequency analysis checkbox
            self.fl_high_c.config(state='normal')  # Activate high-pass filter checkbox
            self.fl_low_c.config(state='normal')  # Activate low-pass filter checkbox

            # Activate entry fields for filters if selected
            if self.fl_high_status.get():
                self.fl_high_entry.config(state='normal')
                self.sample_fq_high_entry.config(state='normal')
                self.fl_order_high_entry.config(state='normal')
            else:
                self.fl_high_entry.config(state='disabled')
                self.sample_fq_high_entry.config(state='disabled')
                self.fl_order_high_entry.config(state='disabled')

            if self.fl_low_status.get():
                self.fl_low_entry.config(state='normal')
                self.sample_fq_low_entry.config(state='normal')
                self.fl_order_low_entry.config(state='normal')
            else:
                self.fl_low_entry.config(state='disabled')
                self.sample_fq_low_entry.config(state='disabled')
                self.fl_order_low_entry.config(state='disabled')

        def show_sin_plot():
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            min_amp = np.min(App.signal)
            max_amp = np.max(App.signal)
            self.label_x = self.label_x_entry.get()  # Get value from the X-axis text field
            self.label_y = self.label_y_entry.get()  # Get value from the Y-axis text field

            # Parameters for the sine wave
            frequency = 50  # Hz
            App.length = 65536  # Number of samples
            duration = end_time - start_time
            sampling_interval = duration / App.length
            # Create time vector
            App.time = np.arange(0, duration, sampling_interval)
            # Generate sine wave
            App.signal = np.sin(2 * np.pi * frequency * App.time)

            self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, min_amp, max_amp, "SIN SIGNAL",
                                         self.label_x, self.label_y)

        def show_2sin_plot():
            start_time = 0
            end_time = 0.5
            min_amp = np.min(App.signal)
            max_amp = np.max(App.signal)
            self.label_x = self.label_x_entry.get()  # Get value from the X-axis text field
            self.label_y = self.label_y_entry.get()  # Get value from the Y-axis text field

            # Parameters for the sine waves
            frequency1 = 50  # Hz
            frequency2 = 60  # Hz
            App.length = 65536  # Number of samples
            duration = end_time - start_time
            sampling_interval = duration / App.length
            # Create time vector
            App.time = np.arange(0, duration, sampling_interval)
            # Generate sine wave for the first frequency
            sine_wave1 = np.sin(2 * np.pi * frequency1 * App.time)
            # Generate sine wave for the second frequency
            sine_wave2 = np.sin(2 * np.pi * frequency2 * App.time)
            # Mix the sine waves
            App.signal = sine_wave1 + sine_wave2

            self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, min_amp, max_amp, "SIN SIGNAL",
                                         self.label_x, self.label_y)

        def do_fft():
            # Calculate the discrete Fourier transform
            Fft = fft(App.signal)
            # Calculate the amplitude spectrum
            spectrum = np.abs(Fft)

            duration = 10  # duration of the signal
            sampling_interval = duration / App.length

            # Determine the frequency axis
            frequencies = fftfreq(App.length, sampling_interval)
            indices = np.where(frequencies >= 0)
            frequencies = frequencies[indices]
            spectrum = spectrum[indices]

            plt.plot(frequencies, spectrum)
            plt.title('Amplitude Spectrum')
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Amplitude')
            plt.show()

        def do_ifft():
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            # Calculate the discrete Fourier transform
            Fft = fft(App.signal)
            # Calculate the amplitude spectrum

            # Determine the frequency axis

            inverse_fft = ifft(Fft)

            plt.plot(App.time, inverse_fft.real)  # Real part of the inverse FFT
            plt.title('Signal after Inverse FFT')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.grid(True)
            plt.xlim(start_time, end_time)
            plt.show()

        def save_plot():
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("PDF files", "*.pdf")])
            if file_path:  # If file path is selected
                try:
                    # Saving selected plot in selected format
                    self.plot_signal.fig.savefig(file_path)
                    print("Plot saved successfully.")
                except Exception as e:
                    print("Error while saving plot:", e)

        # Left frame for input controls
        self.frame_left = tk.Frame(master)
        self.frame_left.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Load file button
        loadFile_button = tk.Button(self.frame_left, text="Load File", command=loadFile, bg='red')
        loadFile_button.grid(row=0, column=0, padx=5, pady=5)

        # Frequency label/entry
        frequency_label = tk.Label(self.frame_left, text="Frequency [Hz]:")
        frequency_label.grid(row=1, column=0, padx=5, pady=5)
        self.frequency_entry = tk.Entry(self.frame_left, state='normal')
        self.frequency_entry.grid(row=2, column=0, padx=5, pady=5)

        # Start time label/entry
        start_time_label = tk.Label(self.frame_left, text="Start Time [s]:")
        start_time_label.grid(row=3, column=0, padx=5, pady=5)
        self.start_time_entry = tk.Entry(self.frame_left, state='normal')
        self.start_time_entry.grid(row=4, column=0, padx=5, pady=5)

        # End time label/entry
        end_time_label = tk.Label(self.frame_left, text="End Time [s]:")
        end_time_label.grid(row=5, column=0, padx=5, pady=5)
        self.end_time_entry = tk.Entry(self.frame_left, state='normal')
        self.end_time_entry.grid(row=6, column=0, padx=5, pady=5)

        # Min amplitude label/entry
        min_amp_label = tk.Label(self.frame_left, text="Min Amplitude:")
        min_amp_label.grid(row=7, column=0, padx=5, pady=5)
        self.min_amp_entry = tk.Entry(self.frame_left, state='normal')
        self.min_amp_entry.grid(row=8, column=0, padx=5, pady=5)

        # Max amplitude label/entry
        max_amp_label = tk.Label(self.frame_left, text="Max Amplitude:")
        max_amp_label.grid(row=9, column=0, padx=5, pady=5)
        self.max_amp_entry = tk.Entry(self.frame_left, state='normal')
        self.max_amp_entry.grid(row=10, column=0, padx=5, pady=5)

        # Save to file button
        self.save_button = tk.Button(self.frame_left, text="Save to File", command=save_plot, state='normal')
        self.save_button.grid(row=11, column=0, padx=5, pady=5)

        # Show EKG button
        self.showEKG_button = tk.Button(self.frame_left, text="Show EKG", command=show_plot, state='normal',
                                        bg='yellow')
        self.showEKG_button.grid(row=12, column=0, padx=5, pady=5)

        # Middle frame for plot
        self.frame_middle = tk.Frame(master)
        self.frame_middle.grid(row=0, column=1, padx=0, pady=0, sticky='n')

        # Plot
        self.plot_signal = Plot(self.frame_middle)

        # Bottom frame for sine wave controls and FFT/IFFT
        self.frame_bottom = tk.Frame(master)
        self.frame_bottom.grid(row=1, column=1, columnspan=2, padx=0, pady=0, sticky='')

        # Show Sin button
        self.showSin_button = tk.Button(self.frame_bottom, text="Load Sin", command=show_sin_plot, state='normal',
                                        bg='red')
        self.showSin_button.grid(row=0, column=0, padx=5, pady=5)

        # Show 2Sin button
        self.show2Sin_button = tk.Button(self.frame_bottom, text="Load 2 Sin", command=show_2sin_plot, state='normal',
                                         bg='red')
        self.show2Sin_button.grid(row=0, column=1, padx=5, pady=5)

        # FFT button
        self.fft_button = tk.Button(self.frame_bottom, text='FFT', command=do_fft, state='normal', bg='green')
        self.fft_button.grid(row=0, column=2, padx=5, pady=5)

        # IFFT button
        self.ifft_button = tk.Button(self.frame_bottom, text='IFFT', command=do_ifft, state='normal', bg='green')
        self.ifft_button.grid(row=0, column=3, padx=5, pady=5)

        # Label/entry X
        label_x = tk.Label(self.frame_bottom, text="Label X:")
        label_x.grid(row=0, column=4, padx=5, pady=5)
        self.label_x_entry = tk.Entry(self.frame_bottom, state='disabled')
        self.label_x_entry.grid(row=0, column=5, padx=5, pady=5)

        # Label/entry Y
        label_y = tk.Label(self.frame_bottom, text="Label Y:")
        label_y.grid(row=0, column=6, padx=5, pady=5)
        self.label_y_entry = tk.Entry(self.frame_bottom, state='disabled')
        self.label_y_entry.grid(row=0, column=7, padx=5, pady=5)

        # Right frame for filter controls
        self.frame_right = tk.Frame(master)
        self.frame_right.grid(row=0, column=2, padx=0, pady=10, sticky='n')

        # Frequency analysis checkbox
        self.fq_anal_c = tk.Checkbutton(self.frame_right, text='Frequency analysis', variable=self.fq_status,
                                        onvalue=True, offvalue=False, state='disabled')
        self.fq_anal_c.grid(row=0, column=0, padx=5, pady=5)

        # High-pass filter checkbox
        self.fl_high_c = tk.Checkbutton(self.frame_right, text='High-Pass Filter', variable=self.fl_high_status,
                                        onvalue=True, offvalue=False, state='disabled')
        self.fl_high_c.grid(row=1, column=0, padx=5, pady=5)

        label_high = tk.Label(self.frame_right, text="Cut-off Frequency: ")
        label_high.grid(row=2, column=0)
        self.fl_high_entry = tk.Entry(self.frame_right, state='disabled')
        self.fl_high_entry.grid(row=3, column=0, pady=5)

        label_sample_high = tk.Label(self.frame_right, text="Sampling Frequency: ")
        label_sample_high.grid(row=4, column=0)
        self.sample_fq_high_entry = tk.Entry(self.frame_right, state='disabled')
        self.sample_fq_high_entry.grid(row=5, column=0, pady=5)

        label_order_high = tk.Label(self.frame_right, text="Order: ")
        label_order_high.grid(row=6, column=0)
        self.fl_order_high_entry = tk.Entry(self.frame_right, state='disabled')
        self.fl_order_high_entry.grid(row=7, column=0, pady=5)

        # Low-pass filter checkbox
        self.fl_low_c = tk.Checkbutton(self.frame_right, text='Low-Pass Filter', variable=self.fl_low_status,
                                       onvalue=True, offvalue=False, state='disabled')
        self.fl_low_c.grid(row=8, column=0, padx=5, pady=5)

        label_low = tk.Label(self.frame_right, text="Cut-off Frequency: ")
        label_low.grid(row=9, column=0)
        self.fl_low_entry = tk.Entry(self.frame_right, state='disabled')
        self.fl_low_entry.grid(row=10, column=0, pady=5)

        label_sample_low = tk.Label(self.frame_right, text="Sampling Frequency: ")
        label_sample_low.grid(row=11, column=0)
        self.sample_fq_low_entry = tk.Entry(self.frame_right, state='disabled')
        self.sample_fq_low_entry.grid(row=12, column=0, pady=5)

        label_order_low = tk.Label(self.frame_right, text="Order: ")
        label_order_low.grid(row=13, column=0)
        self.fl_order_low_entry = tk.Entry(self.frame_right, state='disabled')
        self.fl_order_low_entry.grid(row=14, column=0, pady=5)

        # Apply settings button
        self.apply_button = tk.Button(self.frame_right, text="Apply", state='disabled', command=show_plot)
        self.apply_button.grid(row=15, column=0, pady=20)

        # Checking inputs and setting buttons accessibility
        def check_entries():
            if all(e.get() for e in (self.frequency_entry, self.start_time_entry, self.end_time_entry)):
                self.showEKG_button.config(state='normal')
            else:
                self.showEKG_button.config(state='disabled')

            if any(e.get() for e in (self.label_x_entry, self.label_y_entry, self.fl_high_entry, self.fl_low_entry,
                                     self.fl_order_high_entry, self.fl_order_low_entry, self.sample_fq_low_entry,
                                     self.sample_fq_high_entry)):
                self.apply_button.config(state='normal')  # Activate apply button
            else:
                self.apply_button.config(state='disabled')  # Deactivate apply button

        for entry in (self.frequency_entry, self.start_time_entry, self.end_time_entry, self.label_x_entry,
                      self.label_y_entry, self.fl_high_entry, self.fl_low_entry, self.fl_order_high_entry,
                      self.fl_order_low_entry, self.sample_fq_low_entry, self.sample_fq_high_entry):
            entry.bind('<KeyRelease>', check_entries)
