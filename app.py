from tkinter import *
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from readFile import File
from scipy.fft import fft, fftfreq, ifft
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
            # Activate entry fields after loading a file
            self.frequency_entry.config(state='normal')
            self.start_time_entry.config(state='normal')
            self.end_time_entry.config(state='normal')
            self.label_x_entry.config(state='normal')
            self.label_y_entry.config(state='normal')

        # Showing EKG signal plot
        def show_plot():
            frequency = float(self.frequency_entry.get())
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            lab_x = self.label_x_entry.get()
            lab_y = self.label_y_entry.get()
            file = File(self.path, frequency=frequency)
            App.time, App.signal = file.load_EKG()
            App.length = file.get_length()

            if self.fq_status.get():
                self.plot_signal.show_frequency_analysis(App.signal, frequency)
            else:
                self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, "EKG SIGNAL", lab_x, lab_y)

            self.fq_anal_c.config(state='normal')

        # Showing single sine wave plot
        def show_sin_plot():
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
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

            self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, "SIN SIGNAL", self.label_x,
                                         self.label_y)

        # Showing plot for the sum of two sine waves
        def show_2sin_plot():
            start_time = 0
            end_time = 0.5
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

            self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, "SIN SIGNAL", self.label_x,
                                         self.label_y)

        # Perform FFT on the signal
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

        # Perform IFFT on the signal
        def do_ifft():
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
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

            inverse_fft = ifft(Fft)

            plt.plot(App.time, inverse_fft.real)  # Real part of the inverse FFT
            plt.title('Signal after Inverse FFT')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.grid(True)
            plt.xlim(start_time, end_time)
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
                    self.plot_signal.fig.savefig(file_path)
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

        # FFT button
        self.fft_button = Button(master, text='FFT', command=do_fft, state='normal', bg='green')
        self.fft_button.grid(row=11, column=0, padx=10)

        # IFFT button
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

        # Frequency analysis checkbox
        self.fq_anal_c = Checkbutton(master, text='Frequency analysis', variable=self.fq_status, onvalue=True,
                                     offvalue=False, state='disabled')
        self.fq_anal_c.grid(row=4, column=2, padx=10)

        # Checking inputs and setting buttons accessibility
        def check_entries(*args):
            if all(e.get() for e in (self.frequency_entry, self.start_time_entry, self.end_time_entry)):
                self.showEKG_button.config(state='normal')
            else:
                self.showEKG_button.config(state='disabled')

        for entry in (self.frequency_entry, self.start_time_entry, self.end_time_entry):
            entry.bind('<KeyRelease>', check_entries)
