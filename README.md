# Dokumentacja

## Członkowie zespołu

![image](https://github.com/user-attachments/assets/74383e67-02a8-4652-8cee-952b8bfbbbf5)

[członkowie.xlsx](https://github.com/user-attachments/files/17799235/czlonkowie.xlsx)

## Zestaw pytań

| Pytanie                                                                   | Odpowiedź                                                                                                     | Uwagi                                                                                                    |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Jak rozpocząć nagrywanie audio?**                               | Użyj funkcji `start_recording_audio()`.                                                                     | Można określić parametry `samplerate`, `channels` oraz opcjonalnie `duration`.                  |
| **Jak zatrzymać nagrywanie audio?**                                | Wywołaj funkcję `stop_recording_audio(output_file)`.                                                       | Jeśli podasz ścieżkę do `output_file`, nagranie zostanie zapisane jako plik WAV.                   |
| **Czy aplikacja obsługuje konwersję TXT do PDF?**                 | Tak, funkcja `txt_to_pdf_conversion()` w klasie `More` umożliwia konwersję plików `.txt` na `.pdf`. | Upewnij się, że plik `.txt` jest poprawny i zapisany w UTF-8.                                        |
| **Czy można wyświetlić plik PDF w aplikacji?**                   | Tak, funkcja `open_pdf()` w klasie `More` otwiera plik PDF w nowym oknie.                                  | Do wyświetlania PDF wykorzystywana jest biblioteka `tkinterPdfViewer`.                                |
| **Jak wybrać plik do konwersji lub wyświetlenia?**                | Użyj przycisków "Browse" w odpowiednich sekcjach GUI (dla TXT lub PDF).                                      | Ścieżka pliku jest aktualizowana w labelu poniżej przycisku "Browse".                                 |
| **Co się stanie, jeśli plik TXT jest pusty?**                     | Funkcja `txt_to_pdf_conversion` wygeneruje pusty plik PDF.                                                   | Warto sprawdzić zawartość pliku TXT przed rozpoczęciem konwersji.                                    |
| **Czy aplikacja obsługuje błędy podczas wybierania plików?**    | Tak, w przypadku błędów (np. brak pliku, niewłaściwy typ) aplikacja wyświetli komunikat błędu.         | Obsługa błędów wykorzystuje `messagebox.showerror`.                                                |
| **Czy aplikacja ma ograniczenia dotyczące rozmiaru plików PDF?**  | Nie widać w kodzie bezpośrednich ograniczeń dotyczących rozmiaru plików PDF.                              | Dla dużych plików wyświetlanie w `tkinterPdfViewer` może być mniej wydajne.                       |
| **Jak działa konwersja TXT do PDF?**                               | Funkcja `txt_to_pdf_conversion` odczytuje zawartość pliku TXT, dzieli tekst na linie i zapisuje do PDF.    | Każda linia jest ograniczona do 15 słów, co zapobiega wychodzeniu tekstu poza marginesy.              |
| **Jak aplikacja zapisuje wygenerowany PDF?**                        | Plik PDF jest zapisywany w tym samym katalogu co plik TXT, z tą samą nazwą i rozszerzeniem `.pdf`.        | Jeśli plik PDF już istnieje, zostanie nadpisany.                                                       |
| **Czy aplikacja obsługuje różne formaty audio?**                 | Nie, aplikacja obsługuje tylko format WAV dla nagrywania i zapisu.                                            | Możesz rozszerzyć aplikację, dodając konwersję do innych formatów, np. MP3 przy użyciu `pydub`. |
| **Jak działa GUI aplikacji?**                                      | GUI jest zbudowane za pomocą `tkinter` i rozszerzenia `ttkbootstrap`.                                     | Wszystkie operacje odbywają się w oknach głównych lub pomocniczych (`Toplevel`).                   |
| **Czy aplikacja pozwala na edycję ustawień?**                     | Tak, ustawienia są obsługiwane w module `Settings` (np. jakość obrazu).                                  | Szczegóły ustawień są przechowywane w obiekcie klasy `Settings`.                                   |
| **Czy aplikacja obsługuje wielozadaniowość?**                    | Tak, funkcje takie jak nagrywanie i transkrypcja działają w oddzielnych wątkach.                            | Wątki są obsługiwane za pomocą modułu `threading`.                                                |
| **Czy aplikacja umożliwia transkrypcję audio?**                   | Tak, kod sugeruje możliwość transkrypcji audio w module `transcription`.                                  | Funkcjonalność transkrypcji zależy od implementacji modułu `process_audio_file`.                   |
| **Czy aplikacja automatycznie generuje pdf po nagraniu spotkania?** | Tak, aplikacja automatycznie generuje plik pdf z transkrypcją i slajdami w folderze meetings.                 | Plik ten dodawany jest w specjalnym folderze `meetings` z datą oraz godziną skończenia nagrywania   |

## Interfejs

![main_gui](https://raw.githubusercontent.com/sikorski1/IO_projekt/refs/heads/docs/photos/main_gui.png)

## Wykorzystane biblioteki python

| Use case                        | Nazwa biblioteki   | Link do dokumentacji/tutorialu                                                   |
| ------------------------------- | ------------------ | -------------------------------------------------------------------------------- |
| Tworzenie GUI                   | tkinter            | [Dokumentacja tkinter](https://docs.python.org/3/library/tkinter.html)              |
| Tworzenie GUI                   | ttkbootstrap       | [Dokumentacja ttkbootstrap](https://ttkbootstrap.readthedocs.io/)                   |
| Przetwarzanie obrazów          | cv2 (OpenCV)       | [Dokumentacja OpenCV](https://docs.opencv.org/)                                     |
| Manipulacja plikami audio       | pydub              | [Dokumentacja pydub](https://pydub.com/)                                            |
| Rozpoznawanie mowy              | speech_recognition | [Dokumentacja SpeechRecognition](https://github.com/Uberi/speech_recognition)       |
| Generowanie plików PDF         | fpdf               | [Dokumentacja FPDF](https://pyfpdf.github.io/fpdf2/)                                |
| Przeglądanie PDF w GUI         | tkinterPdfViewer   | [Dokumentacja tkinterPdfViewer](https://pypi.org/project/tkinter-pdf-viewer/)       |
| Obsługa systemu plików        | os, glob           | [Dokumentacja os](https://docs.python.org/3/library/os.html)                        |
| Automatyzacja GUI               | pyautogui          | [Dokumentacja pyautogui](https://pyautogui.readthedocs.io/)                         |
| Praca z plikami JSON            | json               | [Dokumentacja JSON](https://docs.python.org/3/library/json.html)                    |
| Przetwarzanie równoległe      | threading          | [Dokumentacja threading](https://docs.python.org/3/library/threading.html)          |
| Tworzenie wątków w tle        | threading          | [Dokumentacja threading](https://docs.python.org/3/library/threading.html)          |
| Nagrywanie dźwięku            | sounddevice        | [Dokumentacja sounddevice](https://python-sounddevice.readthedocs.io/)              |
| Zapisywanie plików audio       | scipy.io.wavfile   | [Dokumentacja scipy.io.wavfile](https://docs.scipy.org/doc/scipy/reference/io.html) |
| Przetwarzanie danych audio      | numpy              | [Dokumentacja numpy](https://numpy.org/doc/)                                        |
| Tworzenie plików PDF           | FPDF               | [Dokumentacja FPDF](https://pyfpdf.github.io/fpdf2/)                                |
| Przeglądanie plików PDF w GUI | tkinterPdfViewer   | [Dokumentacja tkinterPdfViewer](https://pypi.org/project/tkinter-pdf-viewer/)       |

## Schemat przykładu użycia

```mermaid
graph TD;
    Użytkownik--klika Start-->Aplikacja;
    Aplikacja--rozpoczyna nagrywanie ekranu-->Nagrywanie_audio_i_wideo;
    Nagrywanie_audio_i_wideo--analiza czy zmienił się slajd-->zapisanie_slajdu_oraz_dźwięku_do_slajdu-->Stop
    Nagrywanie_audio_i_wideo-->Analiza_oraz_transkrypcja_zapisanych_plików_audio--transkrypcja do ostatniego zapisanego pliku audio-->Generowanie_pdf 
    Stop--zapisuje ostatni slajd z audio-->Generowanie_pdf;
    Generowanie_pdf-->Użytkownik;
```

## Diagram Sekwencyjny UML

```mermaid
sequenceDiagram
    participant Użytkownik
    participant Aplikacja
    participant Moduł_Nagrywania
    participant Moduł_Detekcji_Zmiany_Slajdu
    participant Moduł_Transkrypcji
    participant Moduł_Generowania_PDF

    Użytkownik->>Aplikacja: Kliknięcie "Start"
    Aplikacja->>Moduł_Nagrywania: Rozpocznij nagrywanie audio i wideo
    loop Podczas nagrywania
        Moduł_Nagrywania->>Moduł_Detekcji_Zmiany_Slajdu: Analiza zmiany slajdu
        Moduł_Detekcji_Zmiany_Slajdu-->>Moduł_Nagrywania: Informacja o zmianie slajdu
        Moduł_Nagrywania->>Aplikacja: Zapisanie aktualnego slajdu i dźwięku
    end
    Użytkownik->>Aplikacja: Kliknięcie "Stop"
    Aplikacja->>Moduł_Nagrywania: Zakończ nagrywanie
    Moduł_Nagrywania-->>Aplikacja: Plik audio/wideo
    Aplikacja->>Moduł_Transkrypcji: Przetwarzanie audio i transkrypcja
    Moduł_Transkrypcji-->>Aplikacja: Wynik transkrypcji
    Aplikacja->>Moduł_Generowania_PDF: Generowanie raportu PDF
    Moduł_Generowania_PDF-->>Aplikacja: Gotowy plik PDF
    Aplikacja-->>Użytkownik: Wyświetlenie raportu z transkrypcją

```

## Projekt Architektury opracowanego systemugraph TD;

```mermaid
graph TD;
  
subgraph Interfejs Użytkownika
    UI1[Panel Użytkownika]
    UI2[Przycisk Start/Stop]
    UI3[Wybór opcji nagrywania]
    UI4[Przegląd wyników i raportów]
end

subgraph Detekcja i Nagrywanie
    DN1[Moduł Detekcji Zmiany Slajdu]
    DN2[Moduł Opcji jakości i wykrywania uczestników]
    DN4[Nagrywanie Audio-Wideo]
end

subgraph Przetwarzanie
    PR1[Walidacja Plików Nagrania]
    PR2[Konwersja Plików na Odpowiedni Format]
    PR3[Transkrypcja Nagrania]
end

subgraph Wyniki i Raportowanie
    WR1[Generowanie Transkrypcji]
    WR2[Generowanie Raportów PDF]
    WR3[Udostępnienie Wyników i Raportów]
end

%% Połączenia logiczne
UI1 --> UI2
UI2 --> DN1
UI3 --> DN2
DN1 --> DN4
DN4 --> PR1
PR1 --> PR2
PR2 --> PR3
PR3 --> WR1
WR1 --> WR2
WR2 --> UI4
WR2 --> WR3
UI4 --> WR3
```

## Szczegółowy opis funkcji aplikacji

![more_gui](https://raw.githubusercontent.com/sikorski1/IO_projekt/refs/heads/docs/photos/more_gui.png)
![set_name_gui](https://raw.githubusercontent.com/sikorski1/IO_projekt/refs/heads/docs/photos/set_name_gui.png)
![settings_gui](https://raw.githubusercontent.com/sikorski1/IO_projekt/refs/heads/docs/photos/settings_gui.png)

### **1. Funkcja nagrywania**

### **Rozpoczęcie nagrywania**

* **Przycisk: "Start Recording"**
  * Rozpoczyna nagrywanie ekranu oraz dźwięku.
  * Tworzone są dwa główne wątki:
    * **Wątek nagrywania wideo:**
      * Funkcja `record_screen` zapisuje zrzuty ekranu w folderze `data`.
      * Analizuje zmiany między kolejnymi zrzutami ekranu.
      * Jeśli zmiany przekraczają określony próg, zapisuje je w folderze `whiteboard_data`.
    * **Wątek nagrywania audio:**
      * Funkcja `start_recording_audio` nagrywa dźwięk w segmentach zsynchronizowanych z istotnymi zrzutami ekranu.
      * Każdy segment audio jest przypisany do zrzutu ekranu, w którym nastąpiła zmiana.

#### **Mechanizm analizy zmian na ekranie**

* **Algorytm porównywania klatek:**
  * Każdy zrzut ekranu jest porównywany z poprzednim na podstawie różnic pikseli.
  * Jeśli różnica przekracza ustalony próg (domyślnie 60%), nowy zrzut jest uznawany za istotny i zapisywany w `whiteboard_data`.
* **Synchronizacja audio i obrazu:**
  * Zrzuty ekranu oznaczone jako istotne przerywają bieżące nagrywanie audio.
  * Nagranie dźwiękowe jest automatycznie rozpoczynane od nowa, aby odpowiadało nowemu zrzutowi.

- **Jakość Zrzutów:**
  - Użytkownik może dostosować jakość zapisywanych obrazów (np. `100%`, `90%`) w ustawieniach aplikacji.

#### **Zakończ Nagrywanie**

- **Przycisk: "Stop Recording"**

  - Zatrzymuje aktywne wątki nagrywania ekranu i dźwięku.
  - Funkcja `stop_audio_recording` kończy aktualny segment audio.

  * Wszystkie pliki są przetwarzane do utworzenia raportu PDF.

#### **Przetwarzanie Raportu**

- Po zakończeniu nagrywania aplikacja generuje raport PDF:
  - Raport zawiera wszystkie istotne zrzuty ekranu.
  - Każdemu obrazowi towarzyszy transkrypcja nagrania audio przypisanego do danego zrzutu.
- Raport jest zapisywany w katalogu `meetings` z datą i godziną rozpoczęcia nagrania.

#### **Automatyczne Czyszczenie Danych**

- Przed rozpoczęciem nowego nagrywania wszystkie pliki w folderach `data` i `whiteboard_data` są usuwane, aby uniknąć nadpisywania starych danych.

### **2. Generowanie raportu PDF**

#### **Proces generowania raportu**

* Funkcja `generate_pdf_report` tworzy raport PDF zawierający:
  * Wszystkie zrzuty ekranu z folderu `whiteboard_data`.
  * Transkrypcję audio dla każdego istotnego zrzutu ekranu.
  * Podsumowanie nagrania, jeśli zostało wygenerowane.

#### **Struktura raportu**

1. **Zrzuty ekranu:**
   * Każdy zrzut ekranu jest dodawany jako nowa strona PDF.
   * Obrazy są wstawiane w wysokiej jakości na środku strony.
2. **Transkrypcja:**
   * Tekst z plików `.txt`, które odpowiadają zrzutom ekranu, jest wstawiany poniżej obrazu.
   * Jeśli plik transkrypcji jest niedostępny, dodawany jest komunikat o błędzie.
3. **Podsumowanie:**
   * Generowane na podstawie wszystkich transkrypcji przy użyciu `summarize_text_gemini`.
   * Podsumowanie dodawane jest jako osobna strona raportu PDF.

#### **Lokalizacja zapisu raportu**

* Raport jest zapisywany w katalogu `meetings` w strukturze:

### **3. Transkrypcja**

#### **Przetwarzanie audio**

* Transkrypcja odbywa się w osobnym wątku za pomocą kolejki (`transcription_queue`).
* Dźwięk zarejestrowany w plikach `.wav` jest przetwarzany do tekstu, a wynik zapisywany w formie pliku `.txt`.

#### **Podczas nagrywania**

* Każdy istotny zrzut ekranu jest łączony z odpowiednim segmentem audio.
* Transkrypcja jest przeprowadzana równolegle i zapisywana w folderze `whiteboard_data`.

#### **Wynik transkrypcji**

* Transkrypcje są automatycznie dodawane do raportu PDF wraz z odpowiadającymi im zrzutami ekranu.

### **4. Zaawansowane opcje**

#### **Set Names**

- Otwiera okno, w którym można przypisać nazwy mówców.
- Umożliwia personalizację transkrypcji.

#### **Settings**

- Otwiera okno ustawień, gdzie użytkownik może dostosować:
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

### **5. Status nagrywania**

- **Wskaźnik statusu:**
  - Aktualizowany co **200 ms**.
  - **Czerwony punkt:** Oznacza aktywne nagrywanie.
  - **Szary punkt:** Oznacza brak nagrywania.

---

### **6. Mechanizmy zarządzania danymi**

- **Czyszczenie danych:**
  - Przy rozpoczęciu nowego nagrywania wszystkie pliki w katalogach `data` i `whiteboard_data` są automatycznie usuwane.

---


### **7. Udoskonalenia**

* **Bezpieczeństwo plików:**

  * Automatyczne usuwanie danych z poprzednich sesji.
* **Zgodność z różnymi ekranami:**

  * Zrzuty ekranu są dostosowywane do rozdzielczości 1920x1080.

## Sugerowane języki implementacji

Python

Uzasadnienie: Python jest doskonałym wyborem dla projektu nagrywania i transkrypcji dzięki swojej wszechstronności oraz bogatemu ekosystemowi bibliotek do obsługi multimediów, takich jak pyaudio, opencv, czy integracji z FFmpeg. Jako lider w dziedzinie sztucznej inteligencji, Python pozwala na łatwą integrację z zaawansowanymi API do transkrypcji, np. OpenAI Whisper czy Google Speech-to-Text, co przyspiesza wdrożenie funkcji przetwarzania dźwięku. Jego prostota i czytelność umożliwiają szybkie prototypowanie i rozwój aplikacji, a wsparcie dla systemowych bibliotek, takich jak psutil, pozwala na monitorowanie aplikacji i procesów systemowych.
