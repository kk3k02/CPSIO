# Wyświetlanie i wykonywanie operacji na wykresie

Poniższy kod zawiera zestaw funkcji do przetwarzania i wizualizacji sygnałów EKG oraz 
sygnałów sinusoidalnych. Kod umożliwia  przeprowadzanie filtracji 
wysokoprzepustowej i niskoprzepustowej oraz aktualizację wykresu sygnału z odpowiednimi ustawieniami 
osi i parametrów. Dodatkowo, kod pozwala na generowanie i wyświetlanie sygnałów sinusoidalnych 
o określonych częstotliwościach, a także na tworzenie sygnałów będących sumą kilku sygnałów 
sinusoidalnych. Możliwe jest również obliczanie i wyświetlanie widma amplitudowego sygnału 
za pomocą transformaty Fouriera oraz odtwarzanie sygnału po zastosowaniu odwrotnej transformaty 
Fouriera. Kod zawiera funkcjonalność umożliwiającą zapisywanie aktualnego wykresu do pliku.
Te funkcje wspierają interaktywną analizę i manipulację sygnałami w aplikacji.

## **Metody**

---

### Konstruktor klasy Plot

Funkcja `__init__` jest konstruktorem obkietu `plot`, który reprezentuje wykres. 
Podczas inicjalizacji funkcja przyjmuje jako argument `master`, który odnosi 
się do głównego okna aplikacji Tkinter. W konstruktorze tworzony jest obiekt figury 
`fig`z określonym rozmiarem (10x6 cali) i rozdzielczością (100 DPI), dodawany jest 
pojedynczy subplot do figury za pomocą `add_subplot(111)`, następnie tworzone jest 
płótno `canvas` do rysowania  wykresu, wykorzystując `FigureCanvasTkAgg`, i 
jest ono integrowane z głównym oknem aplikacji (`master`). Następnie rysowane jest 
płótno `canvas` i jest ono umieszczane w układzie siatki Tkinter za pomocą 
metody `grid`.
Inicjalizowana jest również zmienna `line` jako `None`, która może być później użyta 
do przechowywania odniesienia do rysowanej linii na wykresie.

```python    
def __init__(self, master):
    self.master = master
    self.fig = Figure(figsize=(10, 6), dpi=100)
    self.plot = self.fig.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
    self.canvas.draw()
    self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=12)
    self.line = None
```

#### Parametry

- **master**: `tkinter`
  Główne okno aplikacji Tkinter.

---

### Wyświetlanie wykresu

Funkcja pobiera dane wejściowe od użytkownika dotyczące sygnału EKG. 
Najpierw pobiera wartości częstotliwości próbkowania, czasu początkowego i końcowego, 
minimalnej i maksymalnej amplitudy oraz etykiet osi X i Y. 
Następnie oblicza długość sygnału EKG. Jeśli zaznaczona jest opcja analizy częstotliwości, 
wykonuje odpowiednie przekształcenia. W przeciwnym razie, aktualizuje wykres sygnału.
Kod także sprawdza, czy zaznaczono opcje filtracji wysokoprzepustowej i niskoprzepustowej. 
Jeśli tak, pobiera parametry filtracji i stosuje odpowiednie filtry do sygnału, 
a następnie ponownie aktualizuje wykres z przefiltrowanym sygnałem.

```python
def show_plot():
    frequency = float(self.frequency_entry.get())
    start_time = float(self.start_time_entry.get())
    end_time = float(self.end_time_entry.get())
    min_amp = float(self.min_amp_entry.get())
    max_amp = float(self.max_amp_entry.get())
    lab_x = self.label_x_entry.get()
    lab_y = self.label_y_entry.get()
    file = File(self.path, frequency=frequency)
    App.time, App.signal = file.load_EKG()
    App.length = len(App.signal)  # Directly calculate the length of the signal

    if self.fq_status.get():
        self.plot_signal.show_frequency_analysis(App.signal, frequency)
    else:
        self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, min_amp, max_amp, "EKG SIGNAL",
                                     lab_x, lab_y)

    if self.fl_high_status.get():
        if self.fl_high_entry.get() and self.sample_fq_high_entry.get() and self.fl_order_high_entry.get():
            cut_off = float(self.fl_high_entry.get())
            fs = float(self.sample_fq_high_entry.get())
            order = float(self.fl_order_high_entry.get())
            b, a = self.plot_signal.butter_highpass(cut_off, fs, order)
            filtered_signal = filtfilt(b, a, App.signal)
            self.plot_signal.update_Plot(App.time, filtered_signal, start_time, end_time, min_amp, max_amp,
                                         "EKG SIGNAL", lab_x, lab_y)
            self.new_signal = filtered_signal

    if self.fl_low_status.get():
        if self.fl_low_entry.get() and self.sample_fq_low_entry.get() and self.fl_order_low_entry.get():
            cut_off = float(self.fl_low_entry.get())
            fs = float(self.sample_fq_low_entry.get())
            order = float(self.fl_order_low_entry.get())
            b, a = self.plot_signal.butter_lowpass(cut_off, fs, order)
            filtered_signal = filtfilt(b, a, self.new_signal)
            self.plot_signal.update_Plot(App.time, filtered_signal, start_time, end_time, min_amp, max_amp,
                                         "EKG SIGNAL", lab_x, lab_y)
            self.new_signal = filtered_signal
```
 ---

## Aktualizowanie wykresu

Funkcja `update_Plot` aktualizuje wykres sygnału EKG w obiekcie `Plot`. 
Najpierw sprawdza, czy zmienna `self.line` nie jest pusta; jeśli tak, usuwa istniejącą linię z wykresu. 
Następnie czyści bieżący wykres za pomocą metody `clear`. 

Funkcja rysuje nowy wykres, używając dostarczonych danych czasowych (`time`) i sygnałowych (`signal`),
oraz ustawia zakres osi X od `start_time` do `end_time` i zakres osi Y od `min_amp` do `max_amp`. 
Dodaje tytuł wykresu (`title`), etykiety osi X (`xlabel`) i osi Y (`ylabel`). 
Włącza również siatkę na wykresie za pomocą metody `grid`.

Po zaktualizowaniu wszystkich elementów, funkcja rysuje wykres na płótnie (`canvas.draw`) i 
zapisuje referencję do nowej linii wykresu w `self.line` dla przyszłych aktualizacji.

```python
    def update_Plot(self, time, signal, start_time, end_time, min_amp, max_amp, title, xlabel, ylabel):
        if self.line:
            self.line.remove()
        self.plot.clear()
        self.plot.plot(time, signal, label="EKG Signal")
        self.plot.set_xlim(start_time, end_time)
        self.plot.set_ylim(min_amp, max_amp)
        self.plot.set_title(title)
        self.plot.set_xlabel(xlabel)
        self.plot.set_ylabel(ylabel)
        self.plot.grid(True)
        self.canvas.draw()
        self.line = self.plot.lines[0]
```

---

## Wyświetlanie fali sinusoidalnej

Funkcja generuje i wyświetla wykres sygnału sinusoidalnego. Najpierw pobiera wartości czasu początkowego
i końcowego z pól wejściowych `start_time_entry` i `end_time_entry`. Następnie ustala minimalną i
maksymalną amplitudę sygnału na podstawie aktualnego sygnału w `signal`. Etykiety osi X i Y są 
pobierane z pól `label_x_entry` i `label_y_entry`.

Sygnał sinusoidalny jest generowany z częstotliwością 50 Hz. 
Liczba próbek sygnału wynosi 65536, a czas trwania sygnału jest obliczany jako różnica między 
czasem końcowym a początkowym. Interwał próbkowania jest obliczany jako czas trwania podzielony 
przez liczbę próbek. Na tej podstawie tworzony jest wektor czasu `time`.
Następnie generowany jest sygnał sinusoidalny `signal` przy użyciu funkcji sinusoidalnej. 
Na koniec, wykres sygnału jest aktualizowany za pomocą metody `update_Plot`, która wykorzystuje
wektor czasu, sygnał, czasy początkowy i końcowy, minimalną i maksymalną amplitudę 
oraz etykiety osi X i Y.

```python
def show_sin_plot():
    start_time = float(self.start_time_entry.get())
    end_time = float(self.end_time_entry.get())
    min_amp = np.min(App.signal)
    max_amp = np.max(App.signal)
    self.label_x = self.label_x_entry.get()  # Get value from the X-axis text field
    self.label_y = self.label_y_entry.get()  # Get value from the Y-axis text field

    # Parameters for the sine wave
    frequency = 50  # Hz
    App.length = 65536  # Number of samples
    duration = end_time - start_time
    sampling_interval = duration / App.length
    # Create time vector
    App.time = np.arange(0, duration, sampling_interval)
    # Generate sine wave
    App.signal = np.sin(2 * np.pi * frequency * App.time)

    self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, min_amp, max_amp, "SIN SIGNAL",
                                 self.label_x, self.label_y)
```

---

## Wyświetlanie sumy dwóch sygnałów sinusoidalnych

Funkcja generuje i wyświetla wykres sygnału będącego sumą dwóch sygnałów sinusoidalnych 
o różnych częstotliwościach. Czas początkowy ustawiany jest na 0 a czas końcowy na 0,5 sekundy. 
Następnie obliczana jest minimaln i maksymaln amplituda sygnału na podstawie aktualnego sygnału 
w `signal`. Etykiety osi X i Y są pobierane z pól `label_x_entry` i `label_y_entry`.

Dwa sygnały sinusoidalne są generowane z częstotliwościami odpowiednio 50 Hz i 60 Hz. 
Liczba próbek sygnału wynosi 65536, a czas trwania sygnału jest obliczany jako 
różnica między czasem końcowym a początkowym. Interwał próbkowania jest obliczany jako czas 
trwania podzielony przez liczbę próbek. Na tej podstawie tworzony jest wektor czasu `time`.

Następnie generowane są dwa sygnały sinusoidalne `sine_wave1` i `sine_wave2` dla odpowiednich 
częstotliwości. Te dwa sygnały są sumowane, tworząc końcowy sygnał `signal`.

Na koniec, wykres sumy dwóch sygnałów sinusoidalnych jest aktualizowany za pomocą metody `update_Plot`,
która wykorzystuje wektor czasu, sygnał, czasy początkowy i końcowy, minimalną i maksymalną amplitudę
oraz etykiety osi X i Y.

```python
def show_2sin_plot():
    start_time = 0
    end_time = 0.5
    min_amp = np.min(App.signal)
    max_amp = np.max(App.signal)
    self.label_x = self.label_x_entry.get()  # Get value from the X-axis text field
    self.label_y = self.label_y_entry.get()  # Get value from the Y-axis text field

    # Parameters for the sine waves
    frequency1 = 50  # Hz
    frequency2 = 60  # Hz
    App.length = 65536  # Number of samples
    duration = end_time - start_time
    sampling_interval = duration / App.length
    # Create time vector
    App.time = np.arange(0, duration, sampling_interval)
    # Generate sine wave for the first frequency
    sine_wave1 = np.sin(2 * np.pi * frequency1 * App.time)
    # Generate sine wave for the second frequency
    sine_wave2 = np.sin(2 * np.pi * frequency2 * App.time)
    # Mix the sine waves
    App.signal = sine_wave1 + sine_wave2

    self.plot_signal.update_Plot(App.time, App.signal, start_time, end_time, min_amp, max_amp, "SIN SIGNAL",
                                 self.label_x, self.label_y)
```

---

## Transformata Fouriera

Funkcja oblicza i wyświetla widmo amplitudowe sygnału za pomocą transformaty Fouriera.
Najpierw oblicza dyskretną transformatę Fouriera (FFT) sygnału `signal`, a następnie oblicza 
widmo amplitudowe, biorąc wartości bezwzględne `FFT`.

Czas trwania sygnału jest ustawiony na 10 sekund, a interwał próbkowania obliczany jako czas 
trwania podzielony przez długość sygnału `length`.

Kolejno, określana jest oś częstotliwości za pomocą funkcji `fftfreq`, która zwraca próbki częstotliwości 
dla `FFT`. Wyznaczane są częstotliwości, które są większe lub równe zeru, oraz odpowiadające im 
wartości widma amplitudowego.

Na koniec, tworzony jest wykres widma amplitudowego z częstotliwościami na osi X i 
amplitudą na osi Y, dodaje tytuł wykresu oraz etykiety osi, a następnie wyświetlany jest wykres za
pomocą `plt.show()`.

```python
def do_fft():
    # Calculate the discrete Fourier transform
    Fft = fft(App.signal)
    # Calculate the amplitude spectrum
    spectrum = np.abs(Fft)

    duration = 10  # duration of the signal
    sampling_interval = duration / App.length

    # Determine the frequency axis
    frequencies = fftfreq(App.length, sampling_interval)
    indices = np.where(frequencies >= 0)
    frequencies = frequencies[indices]
    spectrum = spectrum[indices]

    plt.plot(frequencies, spectrum)
    plt.title('Amplitude Spectrum')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.show()
```

---

## Odwrotna transformata Fouriera

Funkcja `do_ifft` oblicza i wyświetla sygnał po zastosowaniu odwrotnej transformaty Fouriera (IFFT). 
Najpierw pobierane są wartości czasu początkowego i końcowego z pól wejściowych `start_time_entry` 
i `end_time_entry`. Następnie obliczana jest dyskretna transformata Fouriera (FFT) sygnału `signal`
i wykonywana jest odwrotna transformata Fouriera (IFFT) do uzyskanego `FFT`, aby odzyskać 
oryginalny sygnał w dziedzinie czasu.

Na koniec, tworzony jest wykres rzeczywistej części sygnału po `IFFT` w odniesieniu do wektora 
czasu `time`, dodawane są tytuł wykresu oraz etykiety osi, włączana jest siatka i ustawiany jest
zakres osi X na wartości od `start_time` do `end_time`. Wykres jest wyświetlany za pomocą funkcji 
`plt.show()`.

```python
def do_ifft():
    start_time = float(self.start_time_entry.get())
    end_time = float(self.end_time_entry.get())
    # Calculate the discrete Fourier transform
    Fft = fft(App.signal)
    # Calculate the amplitude spectrum

    # Determine the frequency axis
    inverse_fft = ifft(Fft)

    plt.plot(App.time, inverse_fft.real)  # Real part of the inverse FFT
    plt.title('Signal after Inverse FFT')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.xlim(start_time, end_time)
    plt.show()
```

---

## Filtr dolnoprzepustowy

Metoda statyczna `butter_lowpass` tworzy dolnoprzepustowy filtr Butterwortha. 
Przyjmuje trzy parametry: `cut_off` (częstotliwość odcięcia), `fs` (częstotliwość próbkowania) 
oraz `order` (rząd filtra). Najpierw oblicza częstotliwość Nyquista jako połowę częstotliwości 
próbkowania `fs`. Następnie normalizuje częstotliwość odcięcia `cut_off` dzieląc ją przez 
częstotliwość Nyquista, co jest wymagane przez funkcję `butter` z pakietu SciPy. 
Na końcu funkcja `butter` generuje współczynniki filtra `b` i `a`, które są zwracane jako wynik.

```python
@staticmethod
    def butter_lowpass(cut_off, fs, order):
        nyquist = 0.5 * fs
        normal_cutoff = cut_off / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a
```

#### Parametry

- **cut_off**: `float`
  Częstotliwość odcięcia filtra w Hz.
- **fs**: `float`
  Częstotliwość próbkowania sygnału w Hz.
- **order**: `int`
  Rząd filtra Butterwortha.

---

## Filtr górnoprzepustowy

Metoda statyczna `butter_highpass` tworzy górnoprzepustowy filtr Butterwortha. 
Przyjmuje trzy parametry: `cut_off` (częstotliwość odcięcia), `fs` (częstotliwość próbkowania) 
oraz `order` (rząd filtra). Najpierw oblicza częstotliwość Nyquista jako połowę częstotliwości 
próbkowania `fs`. Następnie normalizuje częstotliwość odcięcia `cut_off` dzieląc ją 
przez częstotliwość Nyquista, co jest wymagane przez funkcję `butter` z pakietu SciPy. 
Na końcu funkcja `butter` generuje współczynniki filtra `b` i `a` dla filtra górnoprzepustowego, 
które są zwracane jako wynik.

```python
    @staticmethod
    def butter_highpass(cut_off, fs, order):
        """
        Create a Butterworth high-pass filter.
        """
        nyquist = 0.5 * fs
        normal_cutoff = cut_off / nyquist
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a
```

#### Parametry

- **cut_off**: `float`
  Częstotliwość odcięcia filtra w Hz.
- **fs**: `float`
  Częstotliwość próbkowania sygnału w Hz.
- **order**: `int`
  Rząd filtra Butterwortha.

---

## Zapisywanie wykresu do pliku

Funkcja `save_plot` umożliwia zapisanie aktualnego wykresu do pliku w wybranym formacie graficznym. 
Najpierw otwierane jest okno dialogowe, które pozwala użytkownikowi wybrać ścieżkę do pliku oraz 
format zapisu (PNG, JPEG lub PDF). Wybrany format jest określany przez rozszerzenie pliku.

Jeśli użytkownik wybierze ścieżkę do pliku, funkcja próbuje zapisać bieżący wykres za pomocą metody 
`savefig` obiektu `plot_signal.fig` w wybranej lokalizacji. W przypadku pomyślnego zapisu, 
wypisywana jest informacja o sukcesie. Jeśli wystąpi błąd podczas zapisywania, 
błąd jest przechwytywany i wyświetlana jest wiadomość o błędzie.

```python
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
```