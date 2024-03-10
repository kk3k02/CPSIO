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
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=8)
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


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('CPSIO EKG')
        self.path = ""
        self.frequency_entry = None
        self.start_time_entry = None
        self.end_time_entry = None
        self.showEKG_button = None
        self.save_button = None
        self.label_x = ""
        self.label_y = ""
        self.label_x_entry = None
        self.label_y_entry = None

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
            frequency = float(self.frequency_entry.get())
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            self.label_x = self.label_x_entry.get()  # Pobierz wartość z pola tekstowego dla osi X
            self.label_y = self.label_y_entry.get()  # Pobierz wartość z pola tekstowego dla osi Y
            file = File(self.path, frequency=frequency)
            time, signal_data = file.load_EKG()
            app.plot_signal.update_Plot(time, signal_data, start_time, end_time, "EKG SIGNAL", self.label_x, self.label_y)
            self.save_button.config(state='normal')  # Activate save button after showing a plot

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
        self.frequency_entry = Entry(master, state='disabled')
        self.frequency_entry.grid(row=2, column=0, padx=10, pady=(5, 0))

        # Start time label/entry
        start_time_label = Label(master, text="Start Time [s]:")
        start_time_label.grid(row=3, column=0, padx=10, pady=0)
        self.start_time_entry = Entry(master, state='disabled')
        self.start_time_entry.grid(row=4, column=0, padx=10, pady=(5, 0))

        # End time label/entry
        end_time_label = Label(master, text="End Time [s]:")
        end_time_label.grid(row=5, column=0, padx=10, pady=0)
        self.end_time_entry = Entry(master, state='disabled')
        self.end_time_entry.grid(row=6, column=0, padx=10, pady=(5, 0))

        # Save to file button
        self.save_button = Button(master, text="Save to File", command=save_plot,
                                  state='disabled')
        self.save_button.grid(row=7, column=0, padx=10, pady=(5, 0))

        # Plot
        self.plot_signal = Plot(master)

        # Show EKG button
        self.showEKG_button = Button(master, text="Show EKG", command=show_plot,
                                     state='disabled', bg='yellow')
        self.showEKG_button.grid(row=8, column=0, padx=10)

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
