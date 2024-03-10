import numpy as np
import matplotlib.pyplot as plt


def load_signal(file_path, frequency):
    """
    Funkcja do wczytywania sygnału EKG z pliku tekstowego.
    Założenie: Jeśli pierwsza kolumna zawiera czas, to jest używana do skalowania osi czasu.
    """

    data = np.genfromtxt(file_path)
    if data.ndim == 2:  # File has 2 dimensions
        if data.shape[1] > 2:  # File has more than 1 column
            time = np.arange(len(data)) / frequency
            signal = data
        else:  # File has only 1 column
            time = data[:, 0]
            signal = data[:, 1]
    else:  # File has only 1 dimension
        time = np.arange(len(data)) / frequency
        signal = data

    return time, signal


def plot_signal(time, signal, start_time, end_time, title="Sygnał EKG", xlabel="Czas (s)", ylabel="Amplituda",
                save_path=None):
    """
    Funkcja do wizualizacji sygnału EKG.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, signal, label="Sygnał EKG")
    plt.xlim(start_time, end_time)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def main():
    file_path = input("Podaj ścieżkę do pliku z sygnałem EKG [.txt]: ")
    frequency = float(input("Podaj amplitudę syngału EKG [Hz]: "))
    start_time = float(input("Podaj początkowy czas wyświetlanego wycinka [s]: "))
    end_time = float(input("Podaj końcowy czas wyświetlanego wycinka [s]: "))
    save_path = input("Podaj ścieżkę do zapisu wycinka (jeśli nie chcesz zapisać, pozostaw puste): ")

    time, signal = load_signal(file_path, frequency)
    plot_signal(time, signal, start_time, end_time, save_path=save_path)


if __name__ == "__main__":
    main()
