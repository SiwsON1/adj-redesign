# ADJ-27: blok FAQ na wpisach (pilot, 5.11.2026)

Pilot: wpis 310 https://www.naukajazdy.wroc.pl/blog/samochody-osobowe/czym-grozi-jazda-bez-prawa-jazdy-po-zdanym-egzaminie/
Zadanie: https://os.neteam.pl/zadania/ADJ-27

## Stan
- Blok (HTML + CSS + JSON-LD) gotowy, podgląd i zrzuty zrobione na ZAŚLEPKACH odpowiedzi.
- Odpowiedzi: Codex na limicie do 21:46 (5.11). Po odnowieniu: `./dokoncz.sh` (Codex -> buduj_blok -> waliduj -> podglad -> zrzuty `final-*`). Potem QA ręczne.
- Nic nie jest na żywej stronie. Szkicu w WP nie zakładano: podgląd szkicu wymaga logowania, więc podgląd jest lokalny (`podglad-wpis-310.html`, wstrzyknięty blok w zapisaną kopię żywego wpisu).

## KONFLIKT, decyzja przed wdrożeniem
Wpis 310 twierdzi, że bez odebranego dokumentu nie wolno jeździć. To nieaktualne od 08.2023: tymczasowe elektroniczne prawo jazdy (mObywatel) potwierdza uprawnienia od dnia zdanego egzaminu przez max 30 dni (ustawa o kierujących pojazdami art. 4 ust. 1a, art. 5b). FAQ zgodne z prawem będzie sprzeczne z treścią wpisu nad nim.
Ten sam błąd: wpis 1566 https://www.naukajazdy.wroc.pl/blog/zdane-prawo-jazdy-co-dalej/ . Wpis 2904 (prawo jazdy tymczasowe) jest zgodny z prawem.
Propozycja: najpierw poprawić H2 „Czy po zdanym egzaminie można jeździć samochodem?” i akapit końcowy we wpisie 310 (Codex, brief z faktami F1-F6), potem FAQ. We wpisie są też kwoty i „w 2025 roku” (mandat 1500 zł, 30 000 zł), do przeglądu przy tej samej poprawce.

## Pytania (GSC, 4.08-3.11.2026, poz. <= 25, URL pilota)
Pełna lista: zrodla/gsc-pilot-zapytania.tsv (836 zapytań). Grupy (suma wyświetleń zapytań w grupie):
1. Czy po zdaniu egzaminu można od razu jeździć? 161 zapytań, 14 814 wyśw. (top: „czy po zdaniu egzaminu na prawo jazdy można od razu jeździć” 2955, poz. 7,5)
2. Czy mogę jeździć bez plastikowego prawa jazdy (mObywatel, nieodebrany dokument)? 61 zapytań, 1 497 wyśw.
3. Co, jeśli w ciągu 30 dni nie odbiorę prawa jazdy? (pochodna 1 i 2, luka we wpisie)
4. Jak sprawdzić, czy prawo jazdy jest gotowe do odbioru? 19 zapytań, 87 wyśw. (+ „czy jeśli prawo jazdy jest gotowe do odbioru to mogę jeździć” 52)
5. Czy przed egzaminem mogę ćwiczyć z rodzicem/znajomym? 10 zapytań, 463 wyśw. (z osobą z PJ 202 + w trakcie kursu/przed egzaminem 261)
Pominięte: kary i mandaty (1 839 wyśw.) bo wpis to omawia, a FAQ nie może mieć kwot.
„Podobne pytania” z Google: nie pobierane (brak dostępu do SERP z tego środowiska; headless dostaje 429/consent).

## Źródła faktów (sprawdzone 5.11.2026)
- Ustawa o kierujących pojazdami, t.j. Dz.U. 2025 poz. 1226: art. 4 ust. 1a, 5b, 10c, 10d, 23. https://api.sejm.gov.pl/eli/acts/DU/2025/1226/text.pdf (tekst: zrodla/ukp.txt)
- https://info.mobywatel.gov.pl/dokumenty/mprawo-jazdy (30 dni, tylko PL, kategorie, wiek dla kat. B; tekst: zrodla/mobywatel*.txt)
- https://www.gov.pl/web/cyfryzacja/zdajesz-i-jedziesz--rozpoczynamy-wdrozenie-tymczasowego-prawa-jazdy-w-aplikacji-mobywatel (07.08.2023, policja sprawdza w systemie)
- https://www.gov.pl/web/infrastruktura/jak-uzyskac-prawo-jazdy (gotowe najpóźniej po 9 dniach roboczych od potwierdzenia opłaty, status na info-car.pl)
- Uwaga: mObywatel podaje dla kat. B „ukończenie 17 lat” (zmiana 2026), tekst jednolity ustawy z 09.2025 ma jeszcze 18. W FAQ bez liczby lat.

## Blok
- `buduj_blok.py <tresc.md>` -> `03_blok-faq.html` (blok `wp:html`: section.adj-faq, inline style, h2.wp-block-heading, details/summary, JSON-LD FAQPage).
- Styl = kopia `.adj-loc-faq` z /prawo-jazdy-wroclaw-krzyki/ (zrodla/krzyki-adj-loc.css): ramka #ececec, radius 14px, chevron #fea900, summary 16/600, odpowiedź 15px #4b5563.
- Zmiany względem dzielnic (dostępność): hover/active tekstu #a65f00 zamiast #e59800 (kontrast 4,9:1 zamiast 2,4:1), summary:focus-visible (obrys 3px), prefers-reduced-motion, style linków w odpowiedziach.
- H2 sekcji wpada do spisu treści motywu jako ostatnia pozycja. Zostawione celowo.
- Yoast nie generuje FAQPage na wpisach (graph: Article, WebPage, ImageObject, BreadcrumbList, WebSite, Organization, Person), więc brak duplikatu.
- Konto REST (editor) ma unfiltered_html: <style> i <script ld+json> przejdą przez REST. Wgrywanie wg zadania przez Chrome Marcina.
- Partie: docelowo CSS do „Dodatkowy CSS” motywu (raz), w bloku tylko HTML + JSON-LD.
- `waliduj.py`: składnia JSON-LD, zgodność pytań/odpowiedzi z treścią widoczną, em-dash/półpauza, „zł”, „WORD”, >65 słów, polskie znaki.

## Zrzuty
zrzuty/r2-* (po usunięciu banera cookie), zrzuty/r3-* (po poprawce kontrastu hover). 1440 px i 390 px, stany: zamknięte, kontekst (koniec wpisu + blok), otwarte + focus.

## Plan partii (GSC, wszystkie wpisy /blog/, zapytania-pytania poz. <= 25, 3 mies.)
04_potencjal-wpisow-gsc.tsv: 167 wpisów z pytaniami; 24 wpisy >= 5000 wyśw. pytań, 57 >= 1000, 76 >= 100.
Kolejność: partie po 5 od góry listy. Uwaga na „ile kosztuje prawo jazdy” (najwięcej wyświetleń): pytania o kwoty urzędowe, odpowiedzi tylko z odesłaniem do źródła, bez liczb.
