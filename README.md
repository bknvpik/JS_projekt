Gra komputerowa "Space Run"
===========================
Opis zadania
-------------
* Gra ma zaimplementowaną obsługę klawiatury
* Po uruchomieniu gry pojawia się ekran startowy, na którym umieszczone są: tytuł, najlepszy wynik, oraz wskazówki dotyczące sterowania
* Gra umożliwia poruszanie się gracza (statku kosmicznego) w lewo (klawisz a) oraz w prawo (klawisz d)
* Po wystartowaniu gry, statek gracza pojawia się u dołu w środku okna z programem
* Gracz umieszczony jest w przestrzeni kosmicznej, którą imituje przesuwające się tło, nadając efekt poruszania się statku
* Gracz ma możliwość wystrzelenia pocisku (klawisz spacja), który wydostaje się z przodu statku i leci na wprost, w zależności od pozycji gracza
* Na planszy wraz z uruchomieniem gry pojawiają się losowo, obracają się i zmierzają pod różnymi kątami w stronę gracza wrogowie (meteory - 3 rożne typy, wielkości)
* Gdy gracz trafi wystrzelonym pociskiem w meteoryt, niszczy go i zdobywa punkt, licznik aktualnego wyniku gracza umieszczony jest w środkowej, górnej części okna gry
* W lewej górnej części okna gry widnieje wskaźnik aktualnego życia gracza
* Gdy gracz zostanie uderzony przez meteoryt, odebrana będzie odpowiednia ilość życia (w zależności od wielkości meteorytu, z którym się zderzy)
* Gracz umiera, gdy jego pasek zdrowia osiągnie zerową wartość, pojawia się wówczas ekran startowy, który pozwala użytkownikowi zacząć grę od nowa
* Z każdego rozwalonego przez gracza wroga może wypaść jeden z dwóch bonusów (podwójny pocisk oraz odnowienie części życia), bonusy powoli spadają w kierunku gracza
* Gdy gracz zbierze bonus podwajający jego pocisk - w górnym lewym rogu okna (tuż pod paskiem życia) pojawi się pasek wskazujący czas trwania bonusu. Gdy czas ten dobiegnie końca - pasek zniknie
* Gra zapamiętuje najwyższy wynik i wypisuje go zawsze na ekranie startowym w oknie programu
* Gdy gracz pobije rekord, po jego śmierci ukazuje się napis "NEW HIGHSCORE" oraz uzyskany wynik
* Gra posiada ścieżkę dźwiękową: zapętlony podkład muzyczny w tle, odgłosy pocisków, bonusów, niszczenia meteorytów, wybuchów

Testy
-----
* Gracz ma ograniczone pole poruszania - statek kosmiczny nie wychodzi poza krawędzie okna gry
* Jeśli pocisk zetknie się z wrogim obiektem - obiekt ten jest niszczony
* Jeśli gracz zderzy się z wrogim obiektem - odjęta będzie odpowiednia ilość punktów życia, natomiast gdy spadnie ona poniżej zera - gra się zakończy i wyświetli ekran startowy
* Jeśli wrogi obiekt zniknie z pola widzenia gracza - zostaje kasowany
* Na ekranie w danym momencie jest umieszczona konkretna liczba wrogich obiektów, jeżeli któryś z nich zostanie zniszczony lub zniknie z pola widzenia gracza - pojawi się odpowiednia ilość nowych obiektów
* Złapanie bonusu odnawiającego życie powoduje dodanie odpowiedniej ilości punktów życia - nie przekracza maksymalnej dozwolonej wartości, gdy gracz posiada pełen pasek zdrowia zbieranie kolejnych bonusów tego typu nie daje żadnego efektu
* Złapanie bonusu podwójnego lasera podczas gdy jest już aktywny resetuje czas trwania bonusu

[GitHub](http://github.com/bknvpik/JS_projekt)
----------------------------------------------
!ss(https://github.com/bknvpik/JS_projekt/img/screenshot.png)
