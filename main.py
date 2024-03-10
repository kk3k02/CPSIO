from readFile import File
from generatePlot import plot


def main():
    file_path = input("Podaj ścieżkę do pliku z sygnałem EKG [.txt]: ")
    frequency = float(input("Podaj amplitudę syngału EKG [Hz]: "))
    start_time = float(input("Podaj początkowy czas wyświetlanego wycinka [s]: "))
    end_time = float(input("Podaj końcowy czas wyświetlanego wycinka [s]: "))
    save_path = input("Podaj ścieżkę do zapisu wycinka (jeśli nie chcesz zapisać, pozostaw puste): ")

    file = File(file_path, frequency)
    time, signal = file.load_EKG()
    plot_signal = plot(time, signal, start_time, end_time, "Sygnał EKG", "Czas [s]", "Amplituda", None)
    plot_signal.generate_Plot()


if __name__ == "__main__":
    main()
