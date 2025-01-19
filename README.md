# Dokumentacja

## Członkowie zespołu

![image](https://github.com/user-attachments/assets/74383e67-02a8-4652-8cee-952b8bfbbbf5)

[członkowie.xlsx](https://github.com/user-attachments/files/17799235/czlonkowie.xlsx)

## Zestaw pytań

| Pytanie                                    | Odpowiedź                                                                                               | Uwagi                                                                                                 |
|--------------------------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **Jak rozpocząć nagrywanie audio?**        | Użyj funkcji `start_recording_audio()`.                                                                | Można określić parametry `samplerate`, `channels` oraz opcjonalnie `duration`.                       |
| **Jak zatrzymać nagrywanie audio?**        | Wywołaj funkcję `stop_recording_audio(output_file)`.                                                   | Jeśli podasz ścieżkę do `output_file`, nagranie zostanie zapisane jako plik WAV.                     |
| **Czy aplikacja obsługuje konwersję TXT do PDF?** | Tak, funkcja `txt_to_pdf_conversion()` w klasie `More` umożliwia konwersję plików `.txt` na `.pdf`.     | Upewnij się, że plik `.txt` jest poprawny i zapisany w UTF-8.                                         |
| **Czy można wyświetlić plik PDF w aplikacji?** | Tak, funkcja `open_pdf()` w klasie `More` otwiera plik PDF w nowym oknie.                              | Do wyświetlania PDF wykorzystywana jest biblioteka `tkinterPdfViewer`.                                |
| **Jak wybrać plik do konwersji lub wyświetlenia?** | Użyj przycisków "Browse" w odpowiednich sekcjach GUI (dla TXT lub PDF).                                | Ścieżka pliku jest aktualizowana w labelu poniżej przycisku "Browse".                                |
| **Co się stanie, jeśli plik TXT jest pusty?** | Funkcja `txt_to_pdf_conversion` wygeneruje pusty plik PDF.                                             | Warto sprawdzić zawartość pliku TXT przed rozpoczęciem konwersji.                                     |
| **Czy aplikacja obsługuje błędy podczas wybierania plików?** | Tak, w przypadku błędów (np. brak pliku, niewłaściwy typ) aplikacja wyświetli komunikat błędu.          | Obsługa błędów wykorzystuje `messagebox.showerror`.                                                   |
| **Czy aplikacja ma ograniczenia dotyczące rozmiaru plików PDF?** | Nie widać w kodzie bezpośrednich ograniczeń dotyczących rozmiaru plików PDF.                           | Dla dużych plików wyświetlanie w `tkinterPdfViewer` może być mniej wydajne.                           |
| **Jak działa konwersja TXT do PDF?**       | Funkcja `txt_to_pdf_conversion` odczytuje zawartość pliku TXT, dzieli tekst na linie i zapisuje do PDF. | Każda linia jest ograniczona do 15 słów, co zapobiega wychodzeniu tekstu poza marginesy.              |
| **Jak aplikacja zapisuje wygenerowany PDF?** | Plik PDF jest zapisywany w tym samym katalogu co plik TXT, z tą samą nazwą i rozszerzeniem `.pdf`.      | Jeśli plik PDF już istnieje, zostanie nadpisany.                                                     |
| **Czy aplikacja obsługuje różne formaty audio?** | Nie, aplikacja obsługuje tylko format WAV dla nagrywania i zapisu.                                     | Możesz rozszerzyć aplikację, dodając konwersję do innych formatów, np. MP3 przy użyciu `pydub`.       |
| **Jak działa GUI aplikacji?**              | GUI jest zbudowane za pomocą `tkinter` i rozszerzenia `ttkbootstrap`.                                  | Wszystkie operacje odbywają się w oknach głównych lub pomocniczych (`Toplevel`).                      |
| **Czy aplikacja pozwala na edycję ustawień?** | Tak, ustawienia są obsługiwane w module `Settings` (np. jakość obrazu, platforma do nagrywania).       | Szczegóły ustawień są przechowywane w obiekcie klasy `Settings`.                                      |
| **Czy aplikacja obsługuje wielozadaniowość?** | Tak, funkcje takie jak nagrywanie i transkrypcja działają w oddzielnych wątkach.                       | Wątki są obsługiwane za pomocą modułu `threading`.                                                    |
| **Czy aplikacja umożliwia transkrypcję audio?** | Tak, kod sugeruje możliwość transkrypcji audio w module `transcription`.                               | Funkcjonalność transkrypcji zależy od implementacji modułu `process_audio_file`.                      |


## Interfejs
![image](https://github.com/user-attachments/assets/70df35ba-8973-47bf-bdd5-0ab4766cfb33)

## Wykorzystane biblioteki python

| Use case                        | Nazwa biblioteki                  | Link do dokumentacji/tutorialu                          |
|----------------------------------|------------------------------------|---------------------------------------------------------|
| Tworzenie GUI                   | tkinter                           | [Dokumentacja tkinter](https://docs.python.org/3/library/tkinter.html) |
| Tworzenie GUI                   | ttkbootstrap                      | [Dokumentacja ttkbootstrap](https://ttkbootstrap.readthedocs.io/)       |
| Przetwarzanie obrazów           | cv2 (OpenCV)                      | [Dokumentacja OpenCV](https://docs.opencv.org/)                         |
| Manipulacja plikami audio       | pydub                             | [Dokumentacja pydub](https://pydub.com/)                                |
| Rozpoznawanie mowy              | speech_recognition                | [Dokumentacja SpeechRecognition](https://github.com/Uberi/speech_recognition) |
| Generowanie plików PDF          | fpdf                              | [Dokumentacja FPDF](https://pyfpdf.github.io/fpdf2/)                    |
| Przeglądanie PDF w GUI          | tkinterPdfViewer                  | [Dokumentacja tkinterPdfViewer](https://pypi.org/project/tkinter-pdf-viewer/) |
| Obsługa systemu plików          | os, glob                          | [Dokumentacja os](https://docs.python.org/3/library/os.html)            |
| Automatyzacja GUI               | pyautogui                         | [Dokumentacja pyautogui](https://pyautogui.readthedocs.io/)             |
| Praca z plikami JSON            | json                              | [Dokumentacja JSON](https://docs.python.org/3/library/json.html)        |
| Przetwarzanie równoległe        | threading                         | [Dokumentacja threading](https://docs.python.org/3/library/threading.html) |
| Tworzenie wątków w tle          | threading                         | [Dokumentacja threading](https://docs.python.org/3/library/threading.html) 
| Nagrywanie dźwięku              | sounddevice                       | [Dokumentacja sounddevice](https://python-sounddevice.readthedocs.io/) |
| Zapisywanie plików audio        | scipy.io.wavfile                  | [Dokumentacja scipy.io.wavfile](https://docs.scipy.org/doc/scipy/reference/io.html) |
| Przetwarzanie danych audio      | numpy                             | [Dokumentacja numpy](https://numpy.org/doc/)           |
| Tworzenie plików PDF           | FPDF                               | [Dokumentacja FPDF](https://pyfpdf.github.io/fpdf2/)                    |
| Przeglądanie plików PDF w GUI  | tkinterPdfViewer                   | [Dokumentacja tkinterPdfViewer](https://pypi.org/project/tkinter-pdf-viewer/) |


## Schemat przykładu użycia

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
## Diagram Sekwencyjny UML

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
## Projekt Architektury opracowanego systemu

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
## Szczegółowy opis funkcji aplikacji

![image](https://github.com/user-attachments/assets/b30dd9f5-0419-45c4-8f8b-e0c5a9323885)

### **1. Funkcja nagrywania**

#### **Start Recording**
- **Przycisk "Start Recording":**
  - Rozpoczyna proces nagrywania ekranu i dźwięku.
  - Tworzy osobne wątki:
    - **Wątek audio:**
      - Używa funkcji `start_recording_audio` do rejestrowania dźwięku.
    - **Wątek ekranu:**
      - Wykonuje zrzuty ekranu w określonych odstępach czasu.
      - Wykorzystuje PyAutoGUI do robienia zrzutów i OpenCV do ich przetwarzania.
      - Obrazy są zapisywane w folderze `data`.
      - Obrazy znacząco różniące się od domyślnego obrazu aplikacji są zapisywane w folderze `whiteboard_data`.

#### **Mechanizm sprawdzania podobieństwa obrazów:**
- Porównuje zrzuty ekranu z domyślnym obrazem platformy (np. Teams, Zoom, Meet).
- Jeśli różnica przekracza **15%**, obraz zostaje zapisany jako istotny dla sesji nagrywania.

#### **Ograniczenia nagrywania:**
- **Wideo:** Nagrywanie kończy się, gdy liczba zrzutów ekranu przekroczy limit dostępnego miejsca.
- **Audio:** Nagrywanie kończy się, gdy czas nagrywania przekroczy ustawiony limit.

#### **Stop Recording**
- **Przycisk "Stop Recording":**
  - Zatrzymuje nagrywanie ekranu i dźwięku.
  - **Przetwarzanie plików:**
    - Obrazy z folderu `whiteboard_data` są łączone w wideo przy użyciu FFmpeg.
    - Nagranie audio jest scalane z wideo, tworząc pełny materiał.

---

### **2. Transkrypcja**

#### **File Transcription**
- **Wybór pliku audio:**
  - Umożliwia wybór pliku `.wav` z lokalnego systemu.
  - Ścieżka do wybranego pliku jest wyświetlana w interfejsie aplikacji.

- **Wybór języka:**
  - Użytkownik może wybrać język do rozpoznawania mowy (np. `pl` dla polskiego, `en-US` dla angielskiego).
  - Wybrany język jest zapisywany i widoczny w aplikacji.

- **Przycisk "Transcript File":**
  - Rozpoczyna transkrypcję pliku audio w osobnym wątku.
  - Wykorzystuje technologię rozpoznawania mowy do przetwarzania plików `.wav`.

---

### **3. Zaawansowane opcje**

#### **Set Names**
- Otwiera okno, w którym można przypisać nazwy mówców.
- Umożliwia personalizację transkrypcji.

#### **Settings**
- Otwiera okno ustawień, gdzie użytkownik może dostosować:
  - **Platformę:** Teams, Zoom, Meet.
  - **Maksymalny rozmiar plików:** np. 0.1GB, 10GB, 5GB.
  - **Jakość nagrywania:** Procentowa jakość (100%, 90%, itd.).
  - **Rozpoznawanie mówców:** Opcja włączania/wyłączania.

#### **More**
- Otwiera dodatkowe okno z zaawansowanymi funkcjami:
  - **Konwersja plików tekstowych do PDF**:
    - **Wybór pliku `.txt`:**
      - Umożliwia użytkownikowi wybór pliku tekstowego do konwersji na PDF.
      - Ścieżka do wybranego pliku jest wyświetlana w interfejsie.
      - Jeśli plik nie zostanie wybrany, pojawia się komunikat o błędzie.
    - **Przycisk "Convert":**
      - Tworzy plik PDF z zawartości pliku tekstowego.
      - Proces:
        - Każda linia pliku tekstowego jest dzielona na segmenty po 15 słów, aby zmieścić się w jednej linii PDF.
        - PDF jest zapisywany w tej samej lokalizacji co plik `.txt`, z rozszerzeniem `.pdf`.
      - Po zakończeniu procesu wyświetlany jest komunikat o sukcesie.
      - W przypadku błędu aplikacja informuje użytkownika za pomocą komunikatu o błędzie.

  - **Otwieranie plików PDF**:
    - **Wybór pliku `.pdf`:**
      - Umożliwia użytkownikowi wybór pliku PDF do wyświetlenia.
      - Ścieżka do wybranego pliku jest wyświetlana w interfejsie.
      - Jeśli plik nie zostanie wybrany, pojawia się komunikat o błędzie.
    - **Przycisk "Open":**
      - Otwiera nowy widok w oknie aplikacji, wyświetlający zawartość wybranego pliku PDF.
      - Widok PDF:
        - Umożliwia użytkownikowi przeglądanie zawartości pliku w formacie PDF.
        - Plik jest wyświetlany w interfejsie za pomocą modułu `tkinterPdfViewer`.

---

### **4. Status nagrywania**

- **Wskaźnik statusu:**
  - Aktualizowany co **200 ms**.
  - **Czerwony punkt:** Oznacza aktywne nagrywanie.
  - **Szary punkt:** Oznacza brak nagrywania.

---

### **5. Mechanizmy zarządzania danymi**

- **Czyszczenie danych:**
  - Przy rozpoczęciu nowego nagrywania wszystkie pliki w katalogach `data` i `whiteboard_data` są automatycznie usuwane.

---

### **6. Limity przechowywania**

- **Obliczenia czasu nagrywania:**
  - Na podstawie dostępnego miejsca na dysku obliczany jest maksymalny czas nagrywania.
  - Uwzględniane parametry:
    - **Jakość wideo:** Wpływa na rozmiar zrzutów ekranu.
    - **Rozmiar plików:** Ustawienia użytkownika (np. 0.1GB, 10GB).

## Sugerowane języki implementacji
Python

Uzasadnienie: Python jest doskonałym wyborem dla projektu nagrywania i transkrypcji dzięki swojej wszechstronności oraz bogatemu ekosystemowi bibliotek do obsługi multimediów, takich jak pyaudio, opencv, czy integracji z FFmpeg. Jako lider w dziedzinie sztucznej inteligencji, Python pozwala na łatwą integrację z zaawansowanymi API do transkrypcji, np. OpenAI Whisper czy Google Speech-to-Text, co przyspiesza wdrożenie funkcji przetwarzania dźwięku. Jego prostota i czytelność umożliwiają szybkie prototypowanie i rozwój aplikacji, a wsparcie dla systemowych bibliotek, takich jak psutil, pozwala na monitorowanie aplikacji i procesów systemowych.

