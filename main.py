from tkinter import *
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from readFile import File
from scipy.fft import fft
from scipy.fft import fftfreq
from scipy.fft import ifft


class Plot:
    def __init__(self, master):
        self.master = master
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=12)
        self.line = None

    def update_Plot(self, time, signal, start_time, end_time, title, xlabel, ylabel):
        if self.line:
            self.line.remove()
        self.plot.clear()
        self.plot.plot(time, signal, label="EKG Signal")
        self.plot.set_xlim(start_time, end_time)
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


class App:
    time, signal, length = 0, 0, 0
    def __init__(self, master):
        self.master = master
        self.master.title('CPSIO EKG')
        self.path = ""
        self.frequency_entry = None
        self.start_time_entry = None
        self.end_time_entry = None
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

        # Loading EKG signal from *.txt file
        def loadFile():
            self.path = filedialog.askopenfilename(initialdir="/", title="Select EKG signal file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
            # Activate entry after loading a file
            self.frequency_entry.config(state='normal')
            self.start_time_entry.config(state='normal')
            self.end_time_entry.config(state='normal')
            self.label_x_entry.config(state='normal')
            self.label_y_entry.config(state='normal')

        # Showing EKG signal plot
        def show_plot():
            frequency = float(app.frequency_entry.get())
            start_time = float(app.start_time_entry.get())
            end_time = float(app.end_time_entry.get())
            label_x = app.label_x_entry.get()
            label_y = app.label_y_entry.get()
            file = File(app.path, frequency=frequency)
            App.time, App.signal = file.load_EKG()
            App.length = file.get_length()

            if app.fq_status.get():
                app.plot_signal.show_frequency_analysis(App.signal, frequency)
            else:
                app.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, "EKG SIGNAL", label_x, label_y)

            self.fq_anal_c.config(state='normal')

        def show_sin_plot():
            start_time = float(app.start_time_entry.get())
            end_time = float(app.end_time_entry.get())
            self.label_x = self.label_x_entry.get()  # Pobierz wartość z pola tekstowego dla osi X
            self.label_y = self.label_y_entry.get()  # Pobierz wartość z pola tekstowego dla osi Y
           
            # Parametry fali sinusoidalnej
            czestotliwosc = 50  # Hz
            App.length = 65536  # liczba próbek
            czas_trwania = float(app.end_time_entry.get())-float(app.start_time_entry.get())
            czas_probkowania = czas_trwania / App.length
            # Tworzenie wektora czasu
            App.time = np.arange(0, czas_trwania, czas_probkowania)        
            # Generowanie fali sinusoidalnej
            App.signal = np.sin(2 * np.pi * czestotliwosc * App.time)

            app.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, "SIN SIGNAL", self.label_x, self.label_y)

        def show_2sin_plot():
            start_time = 0
            end_time = 0.5
            self.label_x = self.label_x_entry.get()  # Pobierz wartość z pola tekstowego dla osi X
            self.label_y = self.label_y_entry.get()  # Pobierz wartość z pola tekstowego dla osi Y
           
            # Parametry fal sinusoidalnych
            czestotliwosc1 = 50  # Hz
            czestotliwosc2 = 60  # Hz
            App.length = 65536  # liczba próbek
            czas_trwania = float(app.end_time_entry.get())-float(app.start_time_entry.get())
            czas_probkowania = czas_trwania / App.length
            # Tworzenie wektora czasu
            App.time = np.arange(0, czas_trwania, czas_probkowania)
            # Generowanie fali sinusoidalnej dla pierwszej częstotliwości
            fala_sinusoidalna1 = np.sin(2 * np.pi * czestotliwosc1 * App.time)
            # Generowanie fali sinusoidalnej dla drugiej częstotliwości
            fala_sinusoidalna2 = np.sin(2 * np.pi * czestotliwosc2 * App.time)
            # Mieszanie fal sinusoidalnych
            App.signal = fala_sinusoidalna1 + fala_sinusoidalna2

            app.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, "SIN SIGNAL", self.label_x, self.label_y)


        def do_fft():
            # Obliczenie dyskretnej transformaty Fouriera
            Fft = fft(App.signal)
            # Obliczenie widma amplitudowego 
            widmo = np.abs(Fft)
            
            czas_trwania = 10#float(app.end_time_entry.get())-float(app.start_time_entry.get())
            czas_probkowania = czas_trwania / App.length
            
            # Wyznaczanie osi częstotliwości
            czestotliwosci = fftfreq(App.length,czas_probkowania)
            indeksy = np.where(czestotliwosci >= 0)
            czestotliwosci = czestotliwosci[indeksy]
            widmo = widmo[indeksy]
            
            plt.plot(czestotliwosci, widmo)
            plt.title('Widmo Amplitudowe')
            plt.xlabel('Częstotliwość [Hz]')
            plt.ylabel('Amplituda')
            plt.show()
            
            
        def do_ifft():
            start_time = float(app.start_time_entry.get())
            end_time = float(app.end_time_entry.get())
            # Obliczenie dyskretnej transformaty Fouriera
            Fft = fft(App.signal)
            # Obliczenie widma amplitudowego 
            widmo = np.abs(Fft)
            
            czas_trwania = 10#float(app.end_time_entry.get())-float(app.start_time_entry.get())
            czas_probkowania = czas_trwania / App.length
            
            # Wyznaczanie osi częstotliwości
            czestotliwosci = fftfreq(App.length,czas_probkowania)
            indeksy = np.where(czestotliwosci >= 0)
            czestotliwosci = czestotliwosci[indeksy]
            widmo = widmo[indeksy]
            
            odwrotna_fft = ifft(Fft)
            
            plt.plot(App.time, odwrotna_fft.real)  # Realna część odwrotnej FFT
            plt.title('Sygnał po odwrotnej FFT')
            plt.xlabel('Czas [s]')
            plt.ylabel('Amplituda')
            plt.grid(True)
            plt.xlim(start_time,end_time)
            plt.show()

        # Saving plot to file
        def save_plot():
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("PDF files", "*.pdf")])
            if file_path:  # If file path is selected
                try:
                    # Saving selected plot in selected format
                    app.plot_signal.fig.savefig(file_path)
                    print("Plot saved successfully.")
                except Exception as e:
                    print("Error while saving plot:", e)

        # Load file button
        loadFile_button = Button(master, text="Load File", command=loadFile, bg='red')
        loadFile_button.grid(row=0, column=0, padx=10, pady=(5, 0))

        # Frequency label/entry
        frequency_label = Label(master, text="Frequency [Hz]:")
        frequency_label.grid(row=1, column=0, padx=10, pady=(5, 0))
        self.frequency_entry = Entry(master, state='normal')
        self.frequency_entry.grid(row=2, column=0, padx=10, pady=(5, 0))

        # Start time label/entry
        start_time_label = Label(master, text="Start Time [s]:")
        start_time_label.grid(row=3, column=0, padx=10, pady=0)
        self.start_time_entry = Entry(master, state='normal')
        self.start_time_entry.grid(row=4, column=0, padx=10, pady=(5, 0))

        # End time label/entry
        end_time_label = Label(master, text="End Time [s]:")
        end_time_label.grid(row=5, column=0, padx=10, pady=0)
        self.end_time_entry = Entry(master, state='normal')
        self.end_time_entry.grid(row=6, column=0, padx=10, pady=(5, 0))

        # Save to file button
        self.save_button = Button(master, text="Save to File", command=save_plot,
                                  state='normal')
        self.save_button.grid(row=7, column=0, padx=10, pady=(5, 0))

        # Plot
        self.plot_signal = Plot(master)

        # Show EKG button
        self.showEKG_button = Button(master, text="Show EKG", command=show_plot,
                                     state='normal', bg='yellow')
        self.showEKG_button.grid(row=8, column=0, padx=10)

        # Show Sin button
        self.showSin_button = Button(master, text="Load Sin", command=show_sin_plot, 
                                     state='normal', bg='red')
        self.showSin_button.grid(row=9, column=0, padx=10)

        # Show 2Sin button
        self.show2Sin_button = Button(master, text="Load 2 Sin", command=show_2sin_plot, 
                                     state='normal', bg='red')
        self.show2Sin_button.grid(row=10, column=0, padx=10)
        
        self.fft_button = Button(master, text='FFT', command=do_fft, state='normal', bg='green')
        self.fft_button.grid(row=11, column=0, padx=10)
        
        self.ifft_button = Button(master, text='IFFT', command=do_ifft, state='normal', bg='green')
        self.ifft_button.grid(row=12, column=0, padx=10)

        # Label/entry X
        label_x = Label(master, text="Label X:")
        label_x.grid(row=0, column=2, padx=10)
        self.label_x_entry = Entry(master, state='disabled')
        self.label_x_entry.grid(row=1, column=2, padx=10)

        # Label/entry Y
        label_y = Label(master, text="Label Y:")
        label_y.grid(row=2, column=2, padx=10)
        self.label_y_entry = Entry(master, state='disabled')
        self.label_y_entry.grid(row=3, column=2, padx=10)

        # Frequency analise
        self.fq_anal_c = Checkbutton(master, text='Frequency analise', variable=self.fq_status, onvalue=True,
                                     offvalue=False, state='disabled')
        self.fq_anal_c.grid(row=4, column=2, padx=10)

        # Checking inputs and setting buttons accessibility
        def check_entries(*args):
            if all(entry.get() for entry in (self.frequency_entry, self.start_time_entry, self.end_time_entry)):
                self.showEKG_button.config(state='normal')
            else:
                self.showEKG_button.config(state='disabled')

        for entry in (self.frequency_entry, self.start_time_entry, self.end_time_entry):
            entry.bind('<KeyRelease>', check_entries)


if __name__ == '__main__':
    root = Tk()
    root.geometry("1300x650")
    root.configure(bg='white')
    app = App(root)
    root.mainloop()
