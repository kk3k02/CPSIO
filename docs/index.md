# Cyfrowe przetwarzanie sygnałów i obrazów

## Laboratorium: Przetwarzanie i analiza sygnału EKG

### Wstęp
W ramach tego laboratorium, zostały wykonane zadania związane z przetwarzaniem i analizą sygnałów EKG za pomocą języków programowania Python i Matlab. Celem było zdobycie umiejętności wczytywania, przetwarzania, analizowania oraz filtrowania sygnałów EKG.

### Plan ćwiczeń laboratoryjnych
1. **Platforma testowa**
2. **Testowe sygnały EKG**
3. **Analiza okresowych sygnałów w dziedzinie częstotliwości**
4. **Filtracja sygnału EKG**

### Szczegóły zadań

#### Ćwiczenie 1: Platforma testowa
Napisz skrypt w Pythonie/Matlabie umożliwiający wczytywanie i wizualizację badanych sygnałów. Program powinien umożliwiać obserwowanie wniosków sygnału dla zadanego przedziału czasowego, skalowanie osi wartości i ich opis oraz zapis dowolnego wycinka sygnału do pliku o podanej nazwie.

**Pliki sygnałów EKG:**
- `ekg1.txt` - 12 kolumn odpowiadających odpowiedziom, f<sub>s</sub> = 1000 Hz
- `ekg10.txt` - 1 kolumna, f<sub>s</sub> = 360 Hz
- `ekg_noise.txt` - 1 kolumna: czas, 2 kolumna: wartości amplitud EKG, f<sub>s</sub> = 360 Hz

#### Ćwiczenie 2: Analiza okresowych sygnałów w dziedzinie częstotliwości
Celem ćwiczenia jest praktyczne wypróbowanie funkcji `numpy.fft` do wyznaczania prostej i odwrotnej transformacji Fouriera.

**Zadania:**
1. Wygeneruj plik odpowiadający fali sinusoidalnej o częstotliwości 50 Hz i długości 65536.
2. Wyznacz dyskretną transformację Fouriera tego sygnału i przedstaw jego widmo amplitudowe.
3. Powtórz eksperymenty dla różnych czasów trwania sygnałów.
4. Wyznacz odwrotną transformację Fouriera ciągów wyznaczonych w zadaniu 3.

#### Ćwiczenie 3: Analiza sygnału EKG w dziedzinie częstotliwości
Celem ćwiczenia jest obserwacja widma sygnału EKG.

**Zadania:**
1. Wczytaj sygnał `ekg10.txt` i oceń go wizualnie na wykresie.
2. Wyznacz jego dyskretną transformację Fouriera.
3. Wyznacz odwrotną dyskretną transformację Fouriera ciągu wyznaczonego w punkcie 2 i porównaj otrzymany ciąg próbek z pierwotnym sygnałem `ekg10`.

#### Ćwiczenie 4: Filtracja sygnału EKG
Celem ćwiczenia jest praktyczne wypróbowanie działania filtrów w celu wyeliminowania niepożądanych zakłóceń z sygnału EKG.

**Zadania:**
1. Wczytaj sygnały `ekg_noise.txt` i zanalizuj zakłócenia na sygnale.
2. Zbadaj filtr dolnoprzepustowy na sygnale EKG.
3. Zastosuj filtr górnoprzepustowy na zakłóconym sygnale.
4. Sporządź wykresy sygnału przed i po filtracji.

### Bibliografia
1. Dokumentacja `numpy.fft`: [link](https://docs.scipy.org/doc/numpy/reference/routines.fft.html)
2. Dokumentacja `Matplotlib`: [link](https://matplotlib.org/)
3. `Scipy.signal` dokumentacja: [link](https://docs.scipy.org/doc/scipy/reference/signal.html)
4. `Python` Tutorial: [link](https://docs.python.org/3/tutorial/)
