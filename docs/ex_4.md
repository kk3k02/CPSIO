# Zadanie 4

---

## Filtracja sygnału EKG

---

Ćwiczenie 4. Celem ćwiczenia jest praktyczne wypróbowanie działania filtrów
w celu wyeliminowania niepożądanych zakłóceń z sygnału EKG. Proszę wybrać
rodzaj filtra do eksperymentowania, np. Butterwortha lub Czebyszewa. Do filtracji
wykorzystać gotowe funkcje z biblioteki scipy.signal [7]. Biblioteka posiada również
funkcje wspomagające projektowanie filtrów, które można zastosować.

**1) Wczytaj sygnał ekg noise.txt i zauważ zakłócenia nałożone na sygnał. Wykreślić
częstotliwościową charakterystykę amplitudową sygnału.**

![ex_4_1.png](Zadanie%204%2Fex_4_1.png)


Powyższy wykres przedstawia sygnał EKG z nałożonymi zakłóceniami. Charakterystyczne 
piki sygnału reprezentują poszczególne fazy cyklu serca, takie jak załamek P, kompleks QRS i załamek T.

Sygnał powinien mieć stosunkowo gładki przebieg, z wyraźnymi, ale krótkotrwałymi pikami odpowiadającymi
aktywności elektrycznej serca. Zakłócenia w sygnale można zauważyć jako drobne oscylacje i nierówności 
w miejscach, gdzie sygnał powinien być względnie płaski.

Takie zakłócenia mogą pochodzić z różnych 
źródeł, takich jak szum elektryczny, który może być spowodowany przez zakłócenia pochodzące z innych 
urządzeń elektronicznych w pobliżu aparatury EKG, ruch pacjenta, czyli artefakty ruchowe powstające,
gdy pacjent porusza się podczas pomiaru, co powoduje zakłócenia mechaniczne, oraz szum tła, który
może pochodzić z otoczenia, na przykład z przewodów zasilających lub innych źródeł elektromagnetycznych.

Na wykresie widać szum tła jako drobne, ciągłe oscylacje na całej długości sygnału, które zakłócają
właściwy przebieg sygnału EKG. Widoczne są również duże skoki (artefakty), które nie są częścią
typowego sygnału EKG i mogą wynikać z nagłych ruchów lub zakłóceń elektromagnetycznych.

![ex_4_2.png](Zadanie%204%2Fex_4_2.png)

Powyższy wykres przedstawia analizę częstotliwościową sygnału EKG z zakłóceniami. Na osi poziomej (X) 
przedstawione są częstotliwości w Hz, a na osi pionowej (Y) amplituda.

Widać główny pik na bardzo 
niskiej częstotliwości (blisko 0 Hz), co wskazuje na dużą składową stałą lub bardzo wolno zmieniające 
się sygnały, typowe dla EKG. 

W zakresie niskich częstotliwości (od 0 Hz do około 50 Hz) widoczne są 
oscylacje, które mogą odpowiadać szumowi i zakłóceniom pochodzącym z różnych źródeł, takich jak 
szumy elektryczne czy artefakty ruchowe. 

Wyraźny pik przy około 50 Hz prawdopodobnie odpowiada 
zakłóceniom od sieci zasilającej. 

Powyżej 50 Hz amplituda sygnału jest bardzo niska, co oznacza, 
że większość energii sygnału skoncentrowana jest w niskich częstotliwościach.

---

**2) Zbadaj filtr dolnoprzepustowy o częstotliwości granicznej 60 Hz w celu redukcji
zakłóceń pochodzących z sieci zasilającej. Wyznacz parametry filtra, wykreśl
jego charakterystykę (zależność tłumienia od częstotliwości), przebieg sygnału
po filtracji oraz jego widmo. Można też wyznaczyć różnicę między sygnałem
przed i po filtracji i widmo tej różnicy.**

![ex_4_3.png](Zadanie%204%2Fex_4_3.png)

Na załączonym obrazie widoczny jest sygnał EKG po zastosowaniu filtra dolnoprzepustowego o 
następujących parametrach: częstotliwość odcięcia (cut-off) wynosi 60 Hz, częstotliwość próbkowania 
(fs) to 360 Hz, a rząd filtra (order) wynosi 6. 

Filtr dolnoprzepustowy skutecznie tłumi składowe sygnału powyżej 60 Hz, co redukuje
wysokoczęstotliwościowe zakłócenia, takie jak szumy z sieci zasilającej, i pozwala na
uzyskanie bardziej przejrzystego sygnału EKG do dalszej analizy.


![ex_4_4.png](Zadanie%204%2Fex_4_4.png)

Wykres przedstawia charakterystykę częstotliwościową filtru dolnoprzepustowego, który ma za
zadanie tłumienie zakłóceń w sygnale EKG. Oś pozioma (x) ilustruje częstotliwość w hercach (Hz). 
Oś pionowa (y) przedstawia tłumienie amplitudy w decybelach (dB),
co jest logarytmiczną miarą pokazującą, jak bardzo sygnał jest tłumiony przez filtr.

Zielona linia na wykresie pokazuje, jak filtr działa w zakresie różnych częstotliwości. Do około 
60 Hz tłumienie jest minimalne, co oznacza, że sygnały o tych częstotliwościach przechodzą przez
filtr bez większych zmian. Jest to zakres, w którym filtr pozwala na swobodne przejście sygnału. 

Przy około 60 Hz zaczyna się gwałtowny wzrost tłumienia, co oznacza, że filtr zaczyna znacząco
tłumić sygnały powyżej tej częstotliwości. Powyżej 60 Hz tłumienie szybko rośnie, osiągając
wysokie wartości, co wskazuje, że filtr skutecznie usuwa zakłócenia o wyższych częstotliwościach, 
takich jak zakłócenia z sieci zasilającej (typowo 50/60 Hz).


![ex_4_5.png](Zadanie%204%2Fex_4_5.png)

Wykres przedstawia widmo sygnału oryginalnego i widmo sygnału po filtracji, ograniczone do zakresu
częstotliwości 0-100 Hz. Na osi poziomej (x) znajdują się częstotliwości w hercach (Hz), a na osi
pionowej (y) moc spektralna w skali logarytmicznej (dB).

Niebieska linia reprezentuje widmo sygnału oryginalnego. Widać, że sygnał ma istotne składowe w
całym zakresie częstotliwości, szczególnie powyżej 60 Hz, gdzie widoczne są szczyty mocy spektralnej.
Te szczyty są wynikami zakłóceń, prawdopodobnie pochodzących z sieci zasilającej lub innych źródeł
wysokoczęstotliwościowych zakłóceń.

Czerwona linia pokazuje widmo sygnału po filtracji dolnoprzepustowej. Filtr został użyty 
z częstotliwością odcięcia 60 Hz, co oznacza, że skutecznie tłumi składowe sygnału powyżej tej 
częstotliwości. Na wykresie widać, że po filtracji moc spektralna powyżej 60 Hz jest znacznie niższa.
Składowe powyżej 60 Hz zostały znacznie stłumione, co świadczy o skuteczności filtru w 
usuwaniu zakłóceń wysokoczęstotliwościowych.

W zakresie częstotliwości do 60 Hz, zarówno w sygnale oryginalnym, jak i przefiltrowanym widoczne 
są składowe sygnału. Wartości mocy spektralnej w tym zakresie są podobne dla obu sygnałów, co 
wskazuje, że filtr dolnoprzepustowy nie zmienia istotnie składowych sygnału w tym zakresie. 
W zakresie częstotliwości powyżej 60 Hz widmo sygnału oryginalnego pokazuje znaczące składowe,
które są efektem zakłóceń. Po filtracji, te składowe są znacznie zredukowane. Moc spektralna powyżej
60 Hz w sygnale przefiltrowanym jest znacznie niższa, co potwierdza, że filtr skutecznie usuwa 
zakłócenia.

Wykres wyraźnie pokazuje, że filtr dolnoprzepustowy z częstotliwością odcięcia 60 Hz skutecznie tłumi zakłócenia powyżej tej częstotliwości. Dzięki temu, sygnał EKG po filtracji jest czystszy, co ułatwia jego analizę i interpretację. Filtr zachowuje składowe sygnału poniżej 60 Hz, co jest kluczowe dla prawidłowej analizy danych EKG.

---

**3) Zastosuj następnie, do sygnału otrzymanego w punkcie 2, filtr górnoprzepustowy
o częstotliwości granicznej 5 Hz w celu eliminacji pływania linii izoelektrycznej.
Sporządź wykresy sygnałów jak w punkcie 2.
Zauważ, że wykonując polecenia 2 i 3 dostaliśmy szeregowe połączenie filtrów odpowiednio dolno- i górnoprzepustowego, co jest równoważne zastosowaniu filtra
pasmowoprzepustowego o paśmie przepustowym [5, 60] Hz**


![ex_4_6.png](Zadanie%204%2Fex_4_6.png)

Na załączonym obrazie widoczny jest sygnał EKG po zastosowaniu filtra górnoprzepustowego o 
następujących parametrach: częstotliwość odcięcia (cut-off) wynosi 5 Hz, częstotliwość próbkowania
(fs) to 360 Hz, a rząd filtra (order) wynosi 6.

Filtr górnoprzepustowy skutecznie tłumi składowe sygnału poniżej 5 Hz, co eliminuje 
niskoczęstotliwościowe zakłócenia, takie jak pływanie linii izoelektrycznej, i pozwala 
na uzyskanie bardziej przejrzystego sygnału EKG do dalszej analizy.


![ex_4_7.png](Zadanie%204%2Fex_4_7.png)

Wykres przedstawia charakterystykę częstotliwościową filtru połączonego, składającego się z 
filtru dolnoprzepustowego (o częstotliwości odcięcia 60 Hz) oraz filtru górnoprzepustowego
(o częstotliwości odcięcia 5 Hz).

W zakresie częstotliwości poniżej 5 Hz, filtr wykazuje wysokie tłumienie, co oznacza, że 
składowe sygnału w tym zakresie są skutecznie tłumione. Jest to efekt działania filtru 
górnoprzepustowego, który eliminuje niskoczęstotliwościowe zakłócenia, takie jak pływanie
linii izoelektrycznej.

Powyżej 60 Hz również obserwujemy wysokie tłumienie, co jest wynikiem działania filtru 
dolnoprzepustowego. Ten filtr tłumi składowe sygnału powyżej tej częstotliwości, skutecznie 
usuwając zakłócenia wysokoczęstotliwościowe, takie jak szumy z sieci zasilającej.

W zakresie od 5 Hz do 60 Hz filtr przepuszcza składowe sygnału z minimalnym tłumieniem. 
Jest to pasmo, w którym sygnały przechodzą przez filtr bez większych zmian, co jest istotne 
dla analizy sygnału EKG, który zawiera ważne informacje diagnostyczne w tym zakresie częstotliwości.

![ex_4_8.png](Zadanie%204%2Fex_4_8.png)

Wykres przedstawia widmo sygnału oryginalnego (niebieska linia) oraz widmo sygnału po 
filtracji dolnoprzepustowej i górnoprzepustowej (zielona linia).

Widmo sygnału oryginalnego ukazuje składowe w całym zakresie częstotliwości od 0 do 100 Hz, 
z wyraźnymi zakłóceniami niskoczęstotliwościowymi poniżej 5 Hz oraz wysokoczęstotliwościowymi
powyżej 60 Hz, które są widoczne jako wyższe wartości mocy spektralnej. 
Po zastosowaniu filtracji, widmo sygnału po filtracji wykazuje skuteczne zredukowanie 
zakłóceń niskoczęstotliwościowych poniżej 5 Hz dzięki filtrowi górnoprzepustowemu oraz
znaczące tłumienie składowych powyżej 60 Hz, co jest efektem działania filtru dolnoprzepustowego.

Składowe sygnału w zakresie od 5 Hz do 60 Hz są zachowane, co jest kluczowe dla analizy EKG.
Wynikowy sygnał po filtracji jest oczyszczony z zakłóceń, co umożliwia uzyskanie bardziej
przejrzystych danych do analizy medycznej. Porównanie obu widm pokazuje, jak skutecznie 
filtry usunęły niepożądane zakłócenia.

Warto zauważyć, że zastosowanie filtrów dolnoprzepustowego i górnoprzepustowego w 
kolejnych etapach filtracji jest równoważne zastosowaniu filtra pasmowoprzepustowego o
paśmie przepustowym [5, 60] Hz. Taki filtr pasmowoprzepustowy przepuszcza sygnały mieszczące 
się w tym zakresie częstotliwości, skutecznie eliminując zakłócenia zarówno niskoczęstotliwościowe 
(poniżej 5 Hz), jak i wysokoczęstotliwościowe (powyżej 60 Hz). 

Dzięki temu oczyszczony sygnał EKG 
zawiera tylko te składowe, które są istotne dla diagnozy i analizy medycznej, co znacząco poprawia
jego jakość i użyteczność. Porównanie obu widm pokazuje, jak skutecznie filtry usunęły niepożądane
zakłócenia, pozostawiając tylko pożądane składowe sygnału.