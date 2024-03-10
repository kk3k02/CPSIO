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
        self.canvas.get_tk_widget().grid(row=0, column=1)
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
        self.plot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
        self.plot.grid(True)
        self.canvas.draw()
        self.line = self.plot.lines[0]  # Zapisuje referencję do nowej linii wykresu


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('CPSIO EKG')
        self.path = ""
        self.frequency_entry = None
        self.start_time_entry = None
        self.end_time_entry = None
        self.showEKG_button = None

        # Loading EKG signal from *.txt file
        def loadFile():
            self.path = filedialog.askopenfilename(initialdir="/", title="Select EKG signal file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

        # Showing EKG signal plot
        def show_plot():
            frequency = float(self.frequency_entry.get())
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            file = File(self.path, frequency=frequency)
            time, signal_data = file.load_EKG()
            app.plot_signal.update_Plot(time, signal_data, start_time, end_time, "EKG SIGNAL", "Time [s]", "Amplitude")

        # Buttons
        loadFile_button = Button(master, text="Load File", command=loadFile)
        loadFile_button.grid(row=0, column=0)

        frequency_label = Label(master, text="Frequency [Hz]:")
        frequency_label.grid(row=1, column=0)
        self.frequency_entry = Entry(master)
        self.frequency_entry.grid(row=2, column=0)

        start_time_label = Label(master, text="Start Time [s]:")
        start_time_label.grid(row=3, column=0)
        self.start_time_entry = Entry(master)
        self.start_time_entry.grid(row=4, column=0)

        end_time_label = Label(master, text="End Time [s]:")
        end_time_label.grid(row=5, column=0)
        self.end_time_entry = Entry(master)
        self.end_time_entry.grid(row=6, column=0)

        self.plot_signal = Plot(master)

        self.showEKG_button = Button(master, text="Show EKG", command=show_plot)
        self.showEKG_button.grid(row=7, column=0)
        self.showEKG_button.config(state='disabled')

        # Sprawdzenie pól tekstowych i ustawienie stanu przycisku
        def check_entries(*args):
            if all(entry.get() for entry in (self.frequency_entry, self.start_time_entry, self.end_time_entry)):
                self.showEKG_button.config(state='normal')
            else:
                self.showEKG_button.config(state='disabled')

        for entry in (self.frequency_entry, self.start_time_entry, self.end_time_entry):
            entry.bind('<KeyRelease>', check_entries)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
