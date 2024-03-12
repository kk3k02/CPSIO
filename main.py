import tkinter
from tkinter import *
from tkinter import filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from readFile import File
from scipy.fft import fft


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
    def __init__(self, master):
        self.master = master
        self.master.title('CPSIO EKG')
        self.frame_left = tkinter.Frame(master)
        self.frame_left.grid(row=0, column=0, pady=20, padx=(20, 0))
        self.frame_right = tkinter.Frame(master)
        self.frame_right.grid(row=0, column=2, pady=20, padx=(0, 20))
        self.frame_middle = tkinter.Frame(master)
        self.frame_middle.grid(row=0, column=1, pady=20, padx=(0, 0))
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

        # Loading EKG signal from *.txt file
        def loadFile():
            self.path = filedialog.askopenfilename(initialdir="./", title="Select EKG signal file",
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
            time, signal_data = file.load_EKG()

            if app.fq_status.get():
                app.plot_signal.show_frequency_analysis(signal_data, frequency)
            else:
                app.plot_signal.update_Plot(time, signal_data, start_time, end_time, "EKG SIGNAL", label_x, label_y)

            app.save_button.config(state='normal')  # Activate save button after showing a plot
            self.fq_anal_c.config(state='normal')

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
        loadFile_button = Button(self.frame_left, text="Load File", command=loadFile, bg='red')
        loadFile_button.grid(row=0, column=0, pady=20)

        # Frequency frame
        fq_frame = Frame(self.frame_left)
        fq_frame.grid(row=1 , column=0, pady=20, padx=10)

        # Frequency label/entry
        frequency_label = Label(fq_frame, text="Frequency [Hz]:")
        frequency_label.grid(row=0, column=0)
        self.frequency_entry = Entry(fq_frame, state='disabled')
        self.frequency_entry.grid(row=0, column=1)

        # Time frame
        time_frame = Frame(self.frame_left)
        time_frame.grid(row=2, column=0, pady=20, padx=10)

        # Start time label/entry
        start_time_label = Label(time_frame, text="Start Time [s]:")
        start_time_label.grid(row=0, column=0)
        self.start_time_entry = Entry(time_frame, state='disabled')
        self.start_time_entry.grid(row=0, column=1, pady=(0, 5))

        # End time label/entry
        end_time_label = Label(time_frame, text="End Time [s]:")
        end_time_label.grid(row=1, column=0)
        self.end_time_entry = Entry(time_frame, state='disabled')
        self.end_time_entry.grid(row=1, column=1, pady=(5, 0))

        # Save/Show buttons frame
        ss_button_frame = Frame(self.frame_left)
        ss_button_frame.grid(row=3, column=0, pady=20, padx=10)

        # Save to file button
        self.save_button = Button(ss_button_frame, text="Save to File", command=save_plot,
                                  state='disabled')
        self.save_button.grid(row=0, column=0, padx=(0, 10))

        # Plot
        self.plot_signal = Plot(self.frame_middle)

        # Show EKG button
        self.showEKG_button = Button(ss_button_frame, text="Show EKG", command=show_plot,
                                     state='disabled', bg='yellow')
        self.showEKG_button.grid(row=0, column=1, padx=(0, 10))

        # Plot labels frame
        plot_label_frame = Frame(self.frame_right)
        plot_label_frame.grid(row=0, column=0, pady=(60, 0))

        # Label/entry X
        label_x = Label(plot_label_frame, text="Label X:")
        label_x.grid(row=0, column=0)
        self.label_x_entry = Entry(plot_label_frame, state='disabled')
        self.label_x_entry.grid(row=0, column=1, pady=(0, 5))

        # Label/entry Y
        label_y = Label(plot_label_frame, text="Label Y:")
        label_y.grid(row=1, column=0,)
        self.label_y_entry = Entry(plot_label_frame, state='disabled')
        self.label_y_entry.grid(row=1, column=1, pady=(5, 0))

        # Frequency analise
        self.fq_anal_c = Checkbutton(self.frame_right, text='Frequency analise', variable=self.fq_status, onvalue=True,
                                     offvalue=False, state='disabled')
        self.fq_anal_c.grid(row=2, column=0, pady=(20, 20))

        # Type of filter label
        label_filter = Label(self.frame_right, text="Butterworth's Filter")
        label_filter.grid(row=3, column=0, pady=(5, 5), padx=15)

        # High-Pass filter frame
        hp_filter_frame = Frame(self.frame_right)
        hp_filter_frame.grid(row=4, column=0, pady=(0, 20), padx=15)

        # High-pass filter
        self.fl_high_c = Checkbutton(hp_filter_frame, text='High-Pass filter', variable=self.fl_high_status, onvalue=True, offvalue=False, state='disabled')
        self.fl_high_c.grid(row=0, column=0)
        label_high = Label(hp_filter_frame, text="Frequency Limit: ")
        label_high.grid(row=1, column=0)
        self.fl_high_entry = Entry(hp_filter_frame, state='disabled')
        self.fl_high_entry.grid(row=1, column=1, pady=5)
        label_sample_high = Label(hp_filter_frame, text="Sampling Frequency: ")
        label_sample_high.grid(row=2, column=0)
        self.sample_fq_high_entry = Entry(hp_filter_frame, state='disabled')
        self.sample_fq_high_entry.grid(row=2, column=1, pady=5)
        label_order_high = Label(hp_filter_frame, text="Order: ")
        label_order_high.grid(row=3, column=0)
        self.fl_order_high_entry = Entry(hp_filter_frame, state='disabled')
        self.fl_order_high_entry.grid(row=3, column=1, pady=5)

        # Low-pass filter frame
        lp_filter_frame = Frame(self.frame_right)
        lp_filter_frame.grid(row=5, column=0, pady=(0, 20), padx=15)

        # Low-pass filter
        self.fl_low_c = Checkbutton(lp_filter_frame, text='Low-Pass filter', variable=self.fl_low_status,
                                     onvalue=True, offvalue=False, state='disabled')
        self.fl_low_c.grid(row=0, column=0)
        label_low = Label(lp_filter_frame, text="Frequency Limit: ")
        label_low.grid(row=1, column=0)
        self.fl_low_entry = Entry(lp_filter_frame, state='disabled')
        self.fl_low_entry.grid(row=1, column=1)
        label_sample_low = Label(lp_filter_frame, text="Sampling Frequency: ")
        label_sample_low.grid(row=2, column=0)
        self.sample_fq_low_entry = Entry(lp_filter_frame, state='disabled')
        self.sample_fq_low_entry.grid(row=2, column=1, pady=5)
        label_order_low = Label(lp_filter_frame, text="Order: ")
        label_order_low.grid(row=3, column=0)
        self.fl_order_low_entry = Entry(lp_filter_frame, state='disabled')
        self.fl_order_low_entry.grid(row=3, column=1, pady=5)

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
    root.geometry("1550x650")
    root.configure(bg='white')
    app = App(root)
    root.mainloop()
