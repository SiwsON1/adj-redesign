# ADJ-35: frazy z pozycji 4-10, analiza i briefy (05.11.2026)

Zadanie NETIM OS: https://os.neteam.pl/zadania/ADJ-35 . Strona: https://akademiadlaprzemyslu.pl/
Stan: analiza i briefy gotowe. Treść pisze Codex (dostępny od 21:46), Claude robi QA. Zasady wspólne: `briefy/_zasady-wspolne.md`.

Dane: GSC (06.10-02.11.2026, porównanie z 22.09-19.10.2026), SERP Google.pl pobrany 05.11.2026 w Chrome Marcina (może być lokalizowany na Wrocław), treść stron i kursów pobrana curl 05.11.2026. Surowe dane w `dane/` (gsc.json, gsc-strony-zapytania.json, serp-2026-11-05.json, nagłówki konkurencji konk-*.txt, fakty kursów kursy-fakty-*.txt, teksty naszych stron dane/strony/). Wszystkie 62 adresy akademiadlaprzemyslu.pl użyte w briefach: HTTP 200 (05.11.2026).

## Priorytet (realny popyt z GSC × szansa na top 3)

| # | Fraza (Senuto wol., poz.) | URL | GSC poz. (28 dni) i wyśw. frazy | ADJ-34 | Najważniejsze braki | Priorytet |
|---|---|---|---|---|---|---|
| 1 | polaryzacja (8 100, 7) | https://akademiadlaprzemyslu.pl/blog/przemysl/polaryzacja-co-to-jest-i-jakie-ma-znaczenie-w-technice-i-przemysle/ | 6,3 (było 7,4); 4 839 wyśw.; cała strona 12 799 wyśw., 10 klików | nie | definicja słowa na górze, rodzaje polaryzacji światła, biegunowość w elektronice (dioda, kondensator), dielektryk i elektrody, okulary, inne znaczenia (polityka), FAQ | P1 |
| 2 | tokarz (6 600, 4) | https://akademiadlaprzemyslu.pl/blog/przemysl/praca-jako-tokarz-konwencjonalny-obowiazki-wymagania-i-perspektywy/ | 7,6 (było 7,4); 2 229 wyśw. | nie | ogólna definicja tokarza, tokarz konwencjonalny a CNC, jak zostać tokarzem (szkoła, kurs, certyfikat), BHP, zawody pokrewne | P1 |
| 3 | robotyka (2 900, 4) | https://akademiadlaprzemyslu.pl/blog/robotyka/czym-jest-robotyka/ | 7,1 (było 7,3); 2 133 wyśw. | nie | z czego składa się robot, dziedziny robotyki, skąd termin, robotyka a automatyka, jak zacząć naukę (GSC „nauka robotyki przemysłowej” poz. 36) | P1 |
| 4 | ile zarabia elektryk (2 900, 4) | https://akademiadlaprzemyslu.pl/blog/ile-zarabia-elektrotechnik/ | 11,1 (było 16,6); 22 wyśw. | nie | strona jest o elektrotechniku, nie o elektryku; PILNE: kwota „technik 3 430 zł mediana 2025” niższa niż płaca minimalna 2025, żadna kwota bez źródła; brak SEP a zarobki, etat/działalność | P1 korekta kwot, fraza P3 (decyzja: sekcja vs osobny wpis) |
| 5 | sterowniki PLC (3 600, 5) | https://akademiadlaprzemyslu.pl/blog/plc/czym-dokladnie-jest-plc/ | 21,8 (było 24,7); 283 wyśw. („plc” 867 wyśw., poz. 6,7). Senuto poz. 5 to wpis o programowaniu (49 wyśw., poz. 3,2) | programowanie PLC rozbudowane 29.10, ta strona nie | rodzaje sterowników, producenci, wyjścia przekaźnikowe/tranzystorowe, języki IEC 61131-3, dobór sterownika, FAQ | P2 |
| 6 | SCADA (3 600, 9) | https://akademiadlaprzemyslu.pl/blog/przemysl/scada-co-to-jest-i-jak-dziala-w-praktyce/ | 8,5 (było 9,9); 1 591 wyśw. | TAK 28.10 | przykłady systemów (WinCC, AVEVA, Ignition, Asix), SCADA-MES-ERP i OPC UA, bezpieczeństwo, 1-2 pytania FAQ | P2, od ok. 18.11 |
| 7 | izolatory (2 900, 7) | https://akademiadlaprzemyslu.pl/blog/przemysl/izolatory-elektryczne-kompleksowy-przewodnik-techniczny/ | 8,4 (było 8,1); 393 wyśw.; „izolatory elektryczne” 302, poz. 6,1 | nie | top 3 to producenci i sklepy; dla zapytań „co to”: izolator a przewodnik z przykładami, izolator a dielektryk, kiedy izolator przestaje izolować, FAQ | P3 |
| 8 | TIA Portal (1 900, 6) | https://akademiadlaprzemyslu.pl/slowniczek-przemyslowy/tia-portal-co-to/ | 8,7 (było 9,1); 800 wyśw. | TAK 28.10 | języki LAD/FBD/SCL/GRAPH, bloki OB/FC/FB/DB, PLCSIM, FAQ o cenie licencji bez kwoty | P3, od ok. 18.11 |
| 9 | obrabiarka CNC (1 900, 8) | https://akademiadlaprzemyslu.pl/blog/przemysl/czym-jest-obrabiarka-cnc-i-jak-nauczyc-sie-jej-obslugi/ | 8,4 (było 8,2); 533 wyśw. | wpis nie; klaster CNC tak (maszyny, programowanie) | top 3 to sklepy; budowa obrabiarki, konwencjonalna a CNC, praca krok po kroku, bezpieczeństwo i obsługa | P3 |
| 10 | lidary (60 500, 4) | https://akademiadlaprzemyslu.pl/slowniczek-przemyslowy/lidary/ | 4,1 (było 3,0); 51 wyśw. | nie | wolumen Senuto błędny (51 wyśw. przy poz. 4); jak działa (ToF), rodzaje, lidar vs kamera i radar, lidary w zakładzie | P4 |

Kolejność zleceń dla Codexa: polaryzacja → tokarz → robotyka → korekta kwot elektrotechnik → sterowniki PLC → (od 18.11) SCADA, TIA Portal → izolatory → obrabiarka CNC → lidary.

## Ustalenia poza briefami (do decyzji Marcina)
1. Senuto zawyża lub myli dane: „lidary” 60 500 (GSC 51 wyśw./28 dni), „ile zarabia elektryk” poz. 4 (GSC 11), „sterowniki plc” poz. 5 (to inny URL niż ten, który zbiera większość wyświetleń).
2. Błąd faktów na żywo: https://akademiadlaprzemyslu.pl/blog/ile-zarabia-elektrotechnik/ podaje kwoty bez źródeł, w tym medianę technika poniżej płacy minimalnej. Do korekty najszybciej.
3. „ile zarabia elektryk”: wariant A (sekcja w istniejącym wpisie) albo B (osobny wpis o zarobkach elektryka). Rekomendacja: B, bo to inna encja niż elektrotechnik i lepiej pasuje do kursów SEP.
4. Polaryzacja: 12,8 tys. wyświetleń i 10 klików. Poza rozbudową treści warto przejrzeć title i meta description (osobna zmiana, akcept Marcina).
5. Rozjazdy na stronach kursów: TIA Portal poziom 1 (tekst „21 godzin”, ikona „6h”), operator tokarek konwencjonalnych (ikony 8h + 16h, harmonogram 2 dni 8:00-16:00). W briefach zakaz podawania tych godzin do potwierdzenia.
6. Widżet „Kursy, które mogą Cię zainteresować” pod wpisami pokazuje kursy niezwiązane z tematem (np. lakiernik samochodowy pod izolatorami, D2 pod obrabiarką CNC).
7. Zakaz cen kursów w tekstach (jak w ADJ-34): w briefach tylko linki do kursów.

## Po Codexie (QA Claude)
Linki: liczba, pełne adresy, HTTP 200, anchory w kontekście. Akapity ponad 65 słów. Dystansowanie od klienta. Nadmiar „może” i „bywa”. Polskie znaki. Zero półpauz. Zgodność z briefem i sekcją „Czego NIE dopisywać”. Kwoty tylko ze źródłem i datą. Potem zapis w NETIM OS (ADJ-35) per strona.
