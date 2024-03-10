import numpy as np
import matplotlib.pyplot as plt


def load_signal(file_path):
    """
    Funkcja do wczytywania sygnału EKG z pliku tekstowego.
    Założenie: Jeśli pierwsza kolumna zawiera czas, to jest używana do skalowania osi czasu.
    """

    data = np.loadtxt(file_path)

    if data.shape[1] == 2:  # Jeśli są dwie kolumny, to pierwsza to czas, a druga to sygnał EKG
        time = data[:, 0]
        signal = data[:, 1]
    else:  # Jeśli jedna kolumna, to to są wartości sygnału EKG, a czas jest indeksem
        time = np.arange(len(data))
        signal = data

    print(signal)
    return time, signal


def plot_signal(time, signal, start_time, end_time, title="Sygnał EKG", xlabel="Czas (ms)", ylabel="Amplituda",
                save_path=None):
    """
    Funkcja do wizualizacji sygnału EKG.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, signal[:, 3], label="Sygnał EKG")
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
    file_path = input("Podaj ścieżkę do pliku z sygnałem EKG: ")
    start_time = float(input("Podaj początkowy czas wyświetlanego wycinka: "))
    end_time = float(input("Podaj końcowy czas wyświetlanego wycinka: "))
    save_path = input("Podaj ścieżkę do zapisu wycinka (jeśli nie chcesz zapisać, pozostaw puste): ")

    time, signal = load_signal(file_path)
    plot_signal(time, signal, start_time, end_time, save_path=save_path)


if __name__ == "__main__":
    main()
