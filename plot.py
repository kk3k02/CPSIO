import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.fft import fft
from scipy.signal import butter

class Plot:
    def __init__(self, master, app):
        self.app = app
        self.master = master
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=8)
        self.line = None

    def update_Plot(self, time, signal, start_time, end_time, min_amp, max_amp, title, xlabel, ylabel):
        """
        Update the plot with the given parameters.
        Clears the previous plot, sets new limits, and draws the updated plot.
        """
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
        """
        Perform and display frequency analysis of the given signal.
        """
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
