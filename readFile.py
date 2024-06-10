import numpy as np


class File:
    def __init__(self, path, frequency):
        self.path = path
        self.frequency = frequency

    def load_EKG(self):

        data = np.genfromtxt(self.path)
        if data.ndim == 2:  # File has 2 dimensions
            if data.shape[1] > 2:  # File has more than 1 column
                time = np.arange(len(data)) / self.frequency
                signal = data
            else:  # File has only 1 column
                time = data[:, 0]
                signal = data[:, 1]
        else:  # File has only 1 dimension
            time = np.arange(len(data)) / self.frequency
            signal = data

        return time, signal
