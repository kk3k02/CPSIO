import tkinter as tk
from tkinter import filedialog, BooleanVar

from scipy.signal import filtfilt

from plot import Plot
from readFile import File


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('CPSIO EKG')
        self.frame_left = tk.Frame(master)
        self.frame_left.grid(row=0, column=0, pady=20, padx=(20, 0))
        self.frame_right = tk.Frame(master)
        self.frame_right.grid(row=0, column=2, pady=20, padx=(0, 20))
        self.frame_middle = tk.Frame(master)
        self.frame_middle.grid(row=0, column=1, pady=20, padx=(0, 0))
        self.path = ""
        self.frequency_entry = None
        self.start_time_entry = None
        self.end_time_entry = None
        self.min_amp_entry = None
        self.max_amp_entry = None
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
        self.apply_button = None
        self.base_signal = None
        self.new_signal = None

        # Loading EKG signal from *.txt file
        def loadFile():
            self.path = filedialog.askopenfilename(initialdir="./", title="Select EKG signal file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
            # Activate entry fields after loading a file
            self.frequency_entry.config(state='normal')
            self.start_time_entry.config(state='normal')
            self.end_time_entry.config(state='normal')
            self.min_amp_entry.config(state='normal')
            self.max_amp_entry.config(state='normal')
            self.label_x_entry.config(state='normal')
            self.label_y_entry.config(state='normal')

        # Showing EKG signal plot
        def show_plot():
            frequency = float(self.frequency_entry.get())
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            min_amp = float(self.min_amp_entry.get())
            max_amp = float(self.max_amp_entry.get())
            lab_x = self.label_x_entry.get()
            lab_y = self.label_y_entry.get()
            file = File(self.path, frequency=frequency)
            time, signal_data = file.load_EKG()
            self.base_signal = signal_data

            if self.new_signal is None:
                self.new_signal = signal_data

            if self.fq_status.get():
                self.plot_signal.show_frequency_analysis(signal_data, frequency)
            else:
                self.plot_signal.update_Plot(time, signal_data, start_time, end_time, min_amp, max_amp, "EKG SIGNAL",
                                             lab_x, lab_y)

            # Apply high-pass filter if selected
            if self.fl_high_status.get():
                if self.fl_high_entry.get() and self.sample_fq_high_entry.get() and self.fl_order_high_entry.get():
                    cut_off = float(self.fl_high_entry.get())
                    fs = float(self.sample_fq_high_entry.get())
                    order = float(self.fl_order_high_entry.get())
                    b, a = self.plot_signal.butter_highpass(cut_off, fs, order)
                    filtered_signal = filtfilt(b, a, signal_data)
                    self.plot_signal.update_Plot(time, filtered_signal, start_time, end_time, min_amp, max_amp,
                                                 "EKG SIGNAL", lab_x, lab_y)
                    self.new_signal = filtered_signal

            # Apply low-pass filter if selected
            if self.fl_low_status.get():
                if self.fl_low_entry.get() and self.sample_fq_low_entry.get() and self.fl_order_low_entry.get():
                    cut_off = float(self.fl_low_entry.get())
                    fs = float(self.sample_fq_low_entry.get())
                    order = float(self.fl_order_low_entry.get())
                    b, a = self.plot_signal.butter_lowpass(cut_off, fs, order)
                    filtered_signal = filtfilt(b, a, self.new_signal)
                    self.plot_signal.update_Plot(time, filtered_signal, start_time, end_time, min_amp, max_amp,
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
        loadFile_button = tk.Button(self.frame_left, text="Load File", command=loadFile, bg='red')
        loadFile_button.grid(row=0, column=0, pady=20)

        # Frequency frame
        fq_frame = tk.Frame(self.frame_left)
        fq_frame.grid(row=1, column=0, pady=20, padx=10)

        # Frequency label/entry
        frequency_label = tk.Label(fq_frame, text="Frequency [Hz]:")
        frequency_label.grid(row=0, column=0)
        self.frequency_entry = tk.Entry(fq_frame, state='disabled')
        self.frequency_entry.grid(row=0, column=1)

        # Time frame
        time_frame = tk.Frame(self.frame_left)
        time_frame.grid(row=2, column=0, pady=20, padx=10)

        # Start time label/entry
        start_time_label = tk.Label(time_frame, text="Start Time [s]:")
        start_time_label.grid(row=0, column=0)
        self.start_time_entry = tk.Entry(time_frame, state='disabled')
        self.start_time_entry.grid(row=0, column=1, pady=(0, 5))

        # End time label/entry
        end_time_label = tk.Label(time_frame, text="End Time [s]:")
        end_time_label.grid(row=1, column=0)
        self.end_time_entry = tk.Entry(time_frame, state='disabled')
        self.end_time_entry.grid(row=1, column=1, pady=(5, 0))

        # Amplitude frame
        amp_frame = tk.Frame(self.frame_left)
        amp_frame.grid(row=3, column=0, pady=20, padx=10)

        # Min. amplitude label/entry
        min_amp_label = tk.Label(amp_frame, text="Min. amplitude:")
        min_amp_label.grid(row=0, column=0)
        self.min_amp_entry = tk.Entry(amp_frame, state='disabled')
        self.min_amp_entry.grid(row=0, column=1, pady=(0, 5))

        # Max. amplitude label/entry
        max_amp_label = tk.Label(amp_frame, text="Max. amplitude:")
        max_amp_label.grid(row=1, column=0)
        self.max_amp_entry = tk.Entry(amp_frame, state='disabled')
        self.max_amp_entry.grid(row=1, column=1, pady=(5, 0))

        # Save/Show buttons frame
        ss_button_frame = tk.Frame(self.frame_left)
        ss_button_frame.grid(row=4, column=0, pady=20, padx=10)

        # Save to file button
        self.save_button = tk.Button(ss_button_frame, text="Save to File", command=save_plot,
                                     state='disabled')
        self.save_button.grid(row=0, column=0, padx=(0, 10))

        # Plot
        self.plot_signal = Plot(self.frame_middle, self)

        # Show EKG button
        self.showEKG_button = tk.Button(ss_button_frame, text="Show EKG", command=show_plot,
                                        state='disabled', bg='yellow')
        self.showEKG_button.grid(row=0, column=1, padx=(0, 10))

        # Plot label frame
        plot_label_frame = tk.Frame(self.frame_right)
        plot_label_frame.grid(row=0, column=0, pady=(60, 0))

        # Label/entry X
        label_x = tk.Label(plot_label_frame, text="Label X:")
        label_x.grid(row=0, column=0)
        self.label_x_entry = tk.Entry(plot_label_frame, state='disabled')
        self.label_x_entry.grid(row=0, column=1, pady=(0, 5))

        # Label/entry Y
        label_y = tk.Label(plot_label_frame, text="Label Y:")
        label_y.grid(row=1, column=0)
        self.label_y_entry = tk.Entry(plot_label_frame, state='disabled')
        self.label_y_entry.grid(row=1, column=1, pady=(5, 0))

        # Frequency analysis checkbox
        self.fq_anal_c = tk.Checkbutton(self.frame_right, text='Frequency Analysis', variable=self.fq_status,
                                        onvalue=True, offvalue=False, state='disabled')
        self.fq_anal_c.grid(row=2, column=0, pady=(20, 20))

        # Filter type label
        label_filter = tk.Label(self.frame_right, text="Butterworth Filter")
        label_filter.grid(row=3, column=0, pady=(5, 5), padx=15)

        # High-pass filter frame
        hp_filter_frame = tk.Frame(self.frame_right)
        hp_filter_frame.grid(row=4, column=0, pady=(0, 20), padx=15)

        # High-pass filter checkbox
        self.fl_high_c = tk.Checkbutton(hp_filter_frame, text='High-Pass Filter', variable=self.fl_high_status,
                                        onvalue=True, offvalue=False, state='disabled')
        self.fl_high_c.grid(row=0, column=0)
        label_high = tk.Label(hp_filter_frame, text="Cut-off Frequency: ")
        label_high.grid(row=1, column=0)
        self.fl_high_entry = tk.Entry(hp_filter_frame, state='disabled')
        self.fl_high_entry.grid(row=1, column=1, pady=5)
        label_sample_high = tk.Label(hp_filter_frame, text="Sampling Frequency: ")
        label_sample_high.grid(row=2, column=0)
        self.sample_fq_high_entry = tk.Entry(hp_filter_frame, state='disabled')
        self.sample_fq_high_entry.grid(row=2, column=1, pady=5)
        label_order_high = tk.Label(hp_filter_frame, text="Order: ")
        label_order_high.grid(row=3, column=0)
        self.fl_order_high_entry = tk.Entry(hp_filter_frame, state='disabled')
        self.fl_order_high_entry.grid(row=3, column=1, pady=5)

        # Low-pass filter frame
        lp_filter_frame = tk.Frame(self.frame_right)
        lp_filter_frame.grid(row=5, column=0, pady=(0, 20), padx=15)

        # Low-pass filter checkbox
        self.fl_low_c = tk.Checkbutton(lp_filter_frame, text='Low-Pass Filter', variable=self.fl_low_status,
                                       onvalue=True, offvalue=False, state='disabled')
        self.fl_low_c.grid(row=0, column=0)
        label_low = tk.Label(lp_filter_frame, text="Cut-off Frequency: ")
        label_low.grid(row=1, column=0)
        self.fl_low_entry = tk.Entry(lp_filter_frame, state='disabled')
        self.fl_low_entry.grid(row=1, column=1)
        label_sample_low = tk.Label(lp_filter_frame, text="Sampling Frequency: ")
        label_sample_low.grid(row=2, column=0)
        self.sample_fq_low_entry = tk.Entry(lp_filter_frame, state='disabled')
        self.sample_fq_low_entry.grid(row=2, column=1, pady=5)
        label_order_low = tk.Label(lp_filter_frame, text="Order: ")
        label_order_low.grid(row=3, column=0)
        self.fl_order_low_entry = tk.Entry(lp_filter_frame, state='disabled')
        self.fl_order_low_entry.grid(row=3, column=1, pady=5)

        # Apply settings button
        self.apply_button = tk.Button(self.frame_right, text="Apply", state='disabled', command=show_plot)
        self.apply_button.grid(row=6, column=0, pady=20)

        # Checking entries and setting button accessibility
        def check_entries():
            if all(e.get() for e in (self.frequency_entry, self.start_time_entry, self.end_time_entry)):
                self.showEKG_button.config(state='normal')
            else:
                self.showEKG_button.config(state='disabled')

            if any(e.get() for e in (
                    self.label_x_entry, self.label_y_entry, self.fl_high_entry, self.fl_low_entry,
                    self.fl_order_high_entry,
                    self.fl_order_low_entry, self.sample_fq_low_entry, self.sample_fq_high_entry)):
                self.apply_button.config(state='normal')  # Activate apply button
            else:
                self.apply_button.config(state='disabled')  # Deactivate apply button

        for entry in (
                self.frequency_entry, self.start_time_entry, self.end_time_entry, self.label_x_entry,
                self.label_y_entry,
                self.fl_high_entry, self.fl_low_entry, self.fl_order_high_entry, self.fl_order_low_entry,
                self.sample_fq_low_entry, self.sample_fq_high_entry):
            entry.bind('<KeyRelease>', check_entries)
