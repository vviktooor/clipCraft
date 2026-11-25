<p>
  <img src=".github/readme/banner.pl.svg" width="100%" alt="WR · clipCraft: Generator wideo z tekstu z AI">
</p>

<p><a href="README.md">English</a> · <b>Polski</b></p>

<p>
  <img alt="status: aktywny" src="https://img.shields.io/badge/status-aktywny-20C9B0?style=flat-square&labelColor=121B2B">
  <img alt="stack: Python · OpenAI · AssemblyAI" src="https://img.shields.io/badge/stack-Python%20%C2%B7%20OpenAI%20%C2%B7%20AssemblyAI-3267E9?style=flat-square&labelColor=121B2B">
  <img alt="licencja: publiczne" src="https://img.shields.io/badge/licencja-publiczne-526077?style=flat-square&labelColor=121B2B">
</p>

**Aplikacja desktopowa, która z tekstu robi film z lektorem i obrazami generowanymi przez AI.**
Obrazy z OpenAI (`dall-e-3`), synchronizacja z AssemblyAI, lektor z TikTok Voice TTS. Przykładowe filmy: [playlista YouTube](https://www.youtube.com/playlist?list=PLlVNFvFbjZ3G73D6XfwyN_exaYW9FQOk6).

[Zgłoś problem](../../issues)

<p align="center"><img alt="Podgląd: Główne okno ClipCraft" src="Screenshots/ss_01.png" width="85%"></p>

## Funkcje

- **Język lektora** dobierany do tekstu.
- **Rozdziały**: tekst dzielony według długości; jeden wygenerowany obraz na rozdział.
- **Rozmiary obrazów** dla `dall-e-3`: `1024x1024`, `1792x1024` albo `1024x1792`.

## Szybki start

Wymagania: Python 3, dostęp do internetu, klucze API OpenAI i AssemblyAI.

```bash
git clone https://github.com/vviktooor/clipCraft.git
cd clipCraft
pip3 install -r requirements.txt
cd build
python3 gui.py
```

## Użycie

W oknie ustaw: język lektora, katalog wyjściowy filmu, rozmiar obrazów, długość rozdziału (np. `100` = 100 znaków na rozdział) i oba klucze API. Klucze wpisuje się w aplikacji i nie są zapisywane do plików. Znany problem: aplikacja wypisuje je w konsoli (`gui.py`, linia 69), więc nie udostępniaj logów konsoli.

## Języki

Ten README jest po polsku i po [angielsku](README.md) (wersja domyślna). Interfejs: angielski. Polski interfejs: planowany (standard WR v4.4).

## Struktura repozytorium

| Gdzie | Co |
|---|---|
| `build/` | Kod aplikacji (start: `gui.py`) |
| `Screenshots/` | Zrzuty ekranu |
| `requirements.txt` | Zależności Pythona |

## Testy i jakość

| Kontrola | Wynik | Data |
|---|---|---|
| Testy | NOT VERIFIED (brak testów) | 2026-11-25 |

## Podziękowania

[@oscie57](https://github.com/oscie57): [TikTok Voice TTS](https://github.com/oscie57/tiktok-voice).

## Licencja

Brak pliku licencji: wszelkie prawa zastrzeżone. Zapytaj przed ponownym użyciem kodu.
Autor: WR

---

<p align="center"><sub><b>WR</b> · <a href="https://github.com/vviktooor">vviktooor</a></sub></p>
