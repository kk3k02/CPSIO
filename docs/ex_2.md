# Ćwiczenie 2

---

## Analiza sygnałów okresowych w dziedzinie częstotliwości

---

Celem ćwiczenia jest praktyczne wypróbowanie funkcji numpy.fft
i numpy.ifft do wyznaczania prostej i odwrotnej transformaty Fouriera [1, 3].

1. Wygeneruj ciąg próbek odpowiadający fali sinusoidalnej o częstotliwości 50 Hz
i długości 65536.



2. Wyznacz dyskretną transformatę Fouriera tego sygnału i przedstaw jego widmo
amplitudowe na wykresie w zakresie częstotliwości [0, fs/2], gdzie fs oznacza
częstotliwość próbkowania.



3. Wygeneruj ciąg próbek mieszaniny dwóch fal sinusoidalnych (tzn. ich kombinacji
liniowej) o częstotliwościach 50 i 60 Hz. Wykonaj zadanie z punktu 2 dla tego
sygnału.



4. Powtórz eksperymenty dla różnych czasów trwania sygnałów, tzn. dla różnych
częstotliwości próbkowania.



5. Wyznacz odwrotne transformaty Fouriera ciągów wyznaczonych w zadaniu 2
i porównaj z ciągami oryginalnymi.
