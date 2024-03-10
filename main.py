from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from readFile import File


class Plot:
    def __init__(self, master):
        self.master = master
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.line = None  # Przechowuje obiekt linii wykresu

    def update_Plot(self, time, signal, start_time, end_time, title, xlabel, ylabel):
        if self.line:
            self.line.remove()  # Usuwa poprzednią linię wykresu, jeśli istnieje
        self.plot.clear()  # Czyści poprzedni wykres
        self.plot.plot(time, signal, label="EKG Signal")
        self.plot.set_xlim(start_time, end_time)
        self.plot.set_title(title)
        self.plot.set_xlabel(xlabel)
        self.plot.set_ylabel(ylabel)
        self.plot.legend()
        self.canvas.draw()
        self.line = self.plot.lines[0]  # Zapisuje referencję do nowej linii wykresu


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('CPSIO EKG')
        self.path = ""

        # Loading EKG signal from *.txt file
        def loadFile():
            self.path = filedialog.askopenfilename(initialdir="/", title="Select EKG signal file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

        # Showing EKG signal plot
        def show_plot():
            frequency = float(frequency_entry.get())
            start_time = float(start_time_entry.get())
            end_time = float(end_time_entry.get())
            file = File(self.path, frequency=frequency)
            time, signal_data = file.load_EKG()
            app.plot_signal.update_Plot(time, signal_data, start_time, end_time, "Sygnał EKG", "Czas [s]", "Amplituda")

        # Buttons
        loadFile_button = Button(master, text="Load File", command=loadFile)
        loadFile_button.pack()

        frequency_label = Label(master, text="Frequency [Hz]:")
        frequency_label.pack()
        frequency_entry = Entry(master)
        frequency_entry.pack()

        start_time_label = Label(master, text="Start Time [s]:")
        start_time_label.pack()
        start_time_entry = Entry(master)
        start_time_entry.pack()

        end_time_label = Label(master, text="End Time [s]:")
        end_time_label.pack()
        end_time_entry = Entry(master)
        end_time_entry.pack()

        self.plot_signal = Plot(master)

        showEKG_button = Button(master, text="Show EKG", command=show_plot)
        showEKG_button.pack()


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
