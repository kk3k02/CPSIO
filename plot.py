import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.fft import fft


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
        """
        Update the plot with the given time, signal data, and plot parameters.
        Clears the previous plot, sets new limits, and draws the updated plot.

        :param time: Time data for the x-axis
        :param signal: Signal data for the y-axis
        :param start_time: Starting time for the plot x-axis limit
        :param end_time: Ending time for the plot x-axis limit
        :param title: Title of the plot
        :param xlabel: Label for the x-axis
        :param ylabel: Label for the y-axis
        """
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
        """
        Perform and display frequency analysis of the given signal.

        :param signal: Signal data to analyze
        :param frequency: Sampling frequency of the signal
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
