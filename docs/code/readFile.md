# Wczytywanie i przetwarzanie sygnału EKG

### Wczytywanie sygnału EKG

Użyte metody i funkcje służą do wczytywania sygnału EKG z pliku tekstowego i jego przetwarzania 
w celu analizy sygnału. Podczas inicjalizacji, klasa `File` przyjmuje ścieżkę do pliku oraz częstotliwość 
próbkowania sygnału. Następnie, za pomocą odpowiednich metod, wczytuje dane z pliku, przetwarza je, 
generując tablice czasowe oraz sygnałowe, co umożliwia dalszą analizę i interpretację sygnału EKG.

## **Metody**

---

### Konstruktor klasy File

Metoda inicjalizacyjna `__init__` dla klasy File przyjmuje dwa argumenty: `path` oraz `frequency`. Wewnątrz metody wartości te są przypisywane odpowiednio do atrybutów `self.path` i `self.frequency`. Dzięki temu, gdy tworzony jest obiekt tej klasy, jego atrybuty `path` i `frequency` są ustawiane na wartości przekazane podczas inicjalizacji.

```python    
def __init__(self, path, frequency):
    self.path = path
    self.frequency = frequency
```

#### Parametry

- **path**: `str`
  Ścieżka do pliku z sygnałem EKG.
- **frequency**: `float`
  Częstotliwość próbkowania sygnału EKG.

---

### Wczytywanie sygnału EKG z pliku

Funkcja `load_EKG` wczytuje dane z pliku EKG i przetwarza je na sygnał oraz odpowiadający mu czas. Najpierw używa `np.genfromtxt` do wczytania danych z pliku, którego ścieżka jest zapisana w `self.path`. Następnie sprawdza wymiar danych. Jeśli dane są dwuwymiarowe i mają więcej niż jedną kolumnę, generuje czas jako tablicę równomiernie rozłożonych punktów i przypisuje dane do zmiennej `signal`. Jeśli dane dwuwymiarowe mają tylko jedną kolumnę, przypisuje pierwszą kolumnę do `time`, a drugą do `signal`. Jeśli dane są jednowymiarowe, generuje czas jako tablicę równomiernie rozłożonych punktów i przypisuje dane do `signal`. Na koniec funkcja zwraca dwie tablice: `time` i `signal`.

```python    
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
```

#### Zwraca

- **time**: `numpy.ndarray`
  Tablica czasów, obliczona na podstawie częstotliwości próbkowania.
  - **signal**: `numpy.ndarray`
  Tablica wartości sygnału EKG.

---

### Obsługa sygnału EKG

Funkcja otwiera okno dialogowe umożliwiające użytkownikowi wybór pliku EKG. Po wybraniu pliku, aktywuje pola wejściowe, umożliwiając wprowadzenie częstotliwości, czasu początkowego i końcowego, minimalnej i maksymalnej amplitudy oraz etykiet osi X i Y.

```python
def loadFile(self):
    self.path = filedialog.askopenfilename(initialdir="/", title="Select EKG signal file",
                                           filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    # Activate entry fields after loading a file
    self.frequency_entry.config(state='normal')
    self.start_time_entry.config(state='normal')
    self.end_time_entry.config(state='normal')
    self.min_amp_entry.config(state='normal')
    self.max_amp_entry.config(state='normal')
    self.label_x_entry.config(state='normal')
    self.label_y_entry.config(state='normal')
```

#### Etykiety

- **frequency_entry**: `tk.Entry`
  Pole wejściowe do wprowadzenia częstotliwości próbkowania sygnału EKG. Użytkownik wprowadza wartość liczbową, która określa, jak często próbki sygnału są pobierane na sekundę.

- **start_time_entry**: `tk.Entry`
  Pole wejściowe do wprowadzenia czasu początkowego. Użytkownik wprowadza wartość, która określa początek zakresu czasu do analizy sygnału EKG.

- **end_time_entry**: `tk.Entry`
  Pole wejściowe do wprowadzenia czasu końcowego. Użytkownik wprowadza wartość, która określa koniec zakresu czasu do analizy sygnału EKG.

- **min_amp_entry**: `tk.Entry`
  Pole wejściowe do wprowadzenia minimalnej amplitudy sygnału. Użytkownik wprowadza wartość, która określa dolny próg amplitudy sygnału EKG do analizy.

- **max_amp_entry**: `tk.Entry`
  Pole wejściowe do wprowadzenia maksymalnej amplitudy sygnału. Użytkownik wprowadza wartość, która określa górny próg amplitudy sygnału EKG do analizy.

- **label_x_entry**: `tk.Entry`
  Pole wejściowe do wprowadzenia etykiety osi X. Użytkownik wprowadza tekst, który będzie używany jako etykieta osi poziomej na wykresie sygnału EKG.

- **label_y_entry**: `tk.Entry`
  Pole wejściowe do wprowadzenia etykiety osi Y. Użytkownik wprowadza tekst, który będzie używany jako etykieta osi pionowej na wykresie sygnału EKG.

