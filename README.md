# Dokumentacja

## Członkowie zespołu

![image](https://github.com/user-attachments/assets/74383e67-02a8-4652-8cee-952b8bfbbbf5)

[członkowie.xlsx](https://github.com/user-attachments/files/17799235/czlonkowie.xlsx)

### Zestaw pytań

| Pytanie      | Odpowiedź                  | Uwagi|
| ------------- |:-------------------:| -----|
| Pytanie | Odpowiedź | Uwagi |
| Pytanie | Odpowiedź | Uwagi |
| Pytanie | Odpowiedź | Uwagi |
| Pytanie | Odpowiedź | Uwagi |
| Pytanie | Odpowiedź | Uwagi |
| Pytanie | Odpowiedź | Uwagi |
| Pytanie | Odpowiedź | Uwagi |

### Interfejs

### Przydatne biblioteki python

| Use case | Nazwa biblioteki                  | link do dok/tutorial yt |
| ------------- |:-------------------:| -----|
| Tworzenie GUI | tkinter | |
| x | x | x |
| x | x | x |
| x | x | x |


### Schemat przykładu użycia

```mermaid
graph TD;
    Użytkownik--klika Start-->Aplikacja;
    Aplikacja--wykrywa zoom/teams/meet-->Detekcja;
    Detekcja--sprawdza udostępnianie -->Analiza;
    Analiza--brak udostępniania ekranu-->Nagrywanie_głosu;
    Analiza--udostępnianie ekranu-->Nagrywanie_audio_i_wideo;
    Nagrywanie_głosu-->Stop;
    Nagrywanie_audio_i_wideo-->Stop;
    Stop--generuje plik-->Konwerter;
    Konwerter--tworzy transkrypcję-->Transkrypcja;
    Transkrypcja-->Użytkownik;
```
### Diagram Sekwencyjny UML

```mermaid
sequenceDiagram
    participant Użytkownik
    participant Aplikacja
    participant Moduł_Detekcji
    participant Moduł_Nagrywania
    participant Moduł_Przetwarzania
    participant Moduł_Transkrypcji

    Użytkownik->>Aplikacja: Kliknięcie "Start"
    Aplikacja->>Moduł_Detekcji: Wykryj uruchomione aplikacje
    Moduł_Detekcji-->>Aplikacja: Informacje o stanie (udostępnianie ekranu)
    
    alt Udostępnianie ekranu wykryte
        Aplikacja->>Moduł_Nagrywania: Rozpocznij nagrywanie audio i wideo
    else Brak udostępniania ekranu
        Aplikacja->>Moduł_Nagrywania: Rozpocznij nagrywanie audio
    end

    Użytkownik->>Aplikacja: Kliknięcie "Stop"
    Aplikacja->>Moduł_Nagrywania: Zakończ nagrywanie
    Moduł_Nagrywania-->>Aplikacja: Plik audio/wideo

    Aplikacja->>Moduł_Przetwarzania: Przetwarzanie pliku
    Moduł_Przetwarzania-->>Aplikacja: Plik audio

    Aplikacja->>Moduł_Transkrypcji: Utwórz transkrypcję
    Moduł_Transkrypcji-->>Aplikacja: Transkrypcja

    Aplikacja-->>Użytkownik: Wyświetlenie transkrypcji i raportu
```
### Projekt Architektury opracowanego systemu

``` mermaid
graph TD;
    
subgraph UI - Interfejs użytkownika
    U1[Panel Użytkownika]
    U2[Przycisk Start/Stop]
    U3[Wybór opcji nagrywania]
    U4[Przegląd danych]
end

subgraph Detekcja i Nagrywanie
    D1[Moduł Detekcji Aplikacji]
    D2[Moduł Analizy Stanu]
    N1[Moduł Nagrywania Audio]
    N2[Moduł Nagrywania Audio-Wideo]
end

subgraph Przetwarzanie
    P1[Walidacja Nagrania]
    P2[Moduł Konwersji Plików]
    P3[Moduł Transkrypcji]
end

subgraph Wyniki i Raportowanie
    W1[Generowanie Transkrypcji]
    W2[Generowanie Raportów]
    W3[Udostępnienie Wyniku]
end

U1 --> D1
D1 --> D2
D2 --> N1
D2 --> N2
N1 --> P1
N2 --> P1
P1 --> P2
P2 --> P3
P3 --> W1
W1 --> W2
W2 --> W3
```
### Sugerowane języki implementacji
Python

Uzasadnienie: Python jest doskonałym wyborem dla projektu nagrywania i transkrypcji dzięki swojej wszechstronności oraz bogatemu ekosystemowi bibliotek do obsługi multimediów, takich jak pyaudio, opencv, czy integracji z FFmpeg. Jako lider w dziedzinie sztucznej inteligencji, Python pozwala na łatwą integrację z zaawansowanymi API do transkrypcji, np. OpenAI Whisper czy Google Speech-to-Text, co przyspiesza wdrożenie funkcji przetwarzania dźwięku. Jego prostota i czytelność umożliwiają szybkie prototypowanie i rozwój aplikacji, a wsparcie dla systemowych bibliotek, takich jak psutil, pozwala na monitorowanie aplikacji i procesów systemowych.

