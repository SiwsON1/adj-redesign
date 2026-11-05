#!/bin/bash
# Po odnowieniu limitu Codexa (5.11 po 21:46): odpowiedzi -> blok -> walidacja -> podgląd -> zrzuty
set -e
cd "$(dirname "$0")"
codex exec --sandbox workspace-write --skip-git-repo-check "$(cat ~/.claude/skills/artykul/prompt-writer-codex.md)

--- ZADANIE SPECJALNE: nie piszesz artykułu, tylko krótki blok FAQ. Brief poniżej ma pierwszeństwo przed ogólnymi zasadami o długości i strukturze artykułu. Zapisz wynik do pliku 02_faq-tresc.md w bieżącym katalogu. Pierwsza linia pliku: '## Nagłówek: <krótki nagłówek H2 sekcji FAQ, do 60 znaków>'.

BRIEF:
$(cat 01_brief-faq-pilot.md)" > zrodla/codex-log.txt 2>&1
python3 buduj_blok.py 02_faq-tresc.md
python3 waliduj.py || echo "UWAGA: walidacja zgłosiła problemy"
python3 podglad.py
node zrzuty.mjs final
