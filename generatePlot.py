import matplotlib.pyplot as plt
class plot:
    def __init__(self, time, signal, start_time, end_time, title, xlabel, ylabel, save_path):
        self.time = time
        self.signal = signal
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.save_path = save_path

    def generate_Plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.time, self.signal, label="Sygnał EKG")
        plt.xlim(self.start_time, self.end_time)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.legend()
        plt.grid(True)

        if self.save_path:
            plt.savefig(self.save_path)
        else:
            plt.show()
