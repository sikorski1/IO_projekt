# Przewodnik konfiguracji nagrywania dźwięku

Jak skonfigurować zależności, urządzenia wejściowe i konfiguracje pętli zwrotnej wymagane do nagrywania dźwięku systemowego za pomocą Pythona.

---

## Instalacja zależności

### MacOS:

```
brew install python-tk
brew install blackhole-2ch
```

### Windows:

1. Otwórz Wiersz Poleceń jako Administrator.
2. Zainstaluj wymagane zależności:
   ```
   uv pip install -r requirements.txt
   ```
3. Upewnij się, że masz skonfigurowany Microsoft Sound Mapper - Input (MME). Użyj wejścia `<span>2 in</span>` dla MME.

### Linux:

```
sudo apt install gnome-screenshot
```

### Wspólne dla wszystkich:

```
uv pip install -r requirements.txt
```

---

## Pobieranie urządzeń wejściowych

Aby uzyskać listę urządzeń wejściowych, użyj poniższego kodu w Pythonie:

```
import sounddevice as sd
print(sd.query_devices())
```

Aby ustawić urządzenie wejściowe audio systemu, użyj odpowiedniego ID urządzenia:

```
with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback, device=4):
```

Zamień `<span>4</span>` na odpowiednie ID urządzenia z listy.

---

## Konfiguracja pętli zwrotnych do przechwytywania dźwięku systemowego

### MacOS:

1. Zainstaluj **BlackHole**:
   * Postępuj zgodnie z instrukcjami tutaj: [https://github.com/ExistentialAudio/BlackHole]().
   * Zainstaluj za pomocą Homebrew:
     ```
     brew install blackhole-2ch
     ```
2. Skonfiguruj BlackHole:
   * Otwórz **Audio MIDI Setup**.
   * Utwórz urządzenie Multi-Output z **BlackHole 2ch** jako jednym z wyjść.
   * Ustaw to urządzenie Multi-Output jako wyjście dźwięku systemowego.

Zapoznaj się z oficjalnym przewodnikiem: [BlackHole Multi-Output Device Setup](https://github.com/ExistentialAudio/BlackHole/wiki/Multi-Output-Device).

### Windows:

* Otwórz stronę [VB-Audio Virtual Cable](https://vb-audio.com/Cable/index.htm)
* Pobierz ostatnie wydanie na Windows
* Rozpakuj pobrany folder .zip
* Otwórz z folderu plik **VBCABLE_Setup_x64.exe** lub **VBCABLE_Setup.exe**
* Zainstaluj sterownik
* Zrestartuj komputer
* W ustawieniach przejdź do sekcji **Sound**
* Ustaw **output** na **CABLE Input** oraz **input** na **CABLE Output**

### Linux:

*TODO: Dodaj konkretne instrukcje dotyczące konfiguracji pętli zwrotnej w systemie Linux.*

---

## Ważne informacje:

1. **Wersja Pythona**: Upewnij się, że używasz wersji Python `<span>3.12.7</span>`.
2. **Folder roboczy**: Zawsze uruchamiaj skrypt z folderu `<span>recorder</span>`.
3. **Uprawnienia administratora**: W systemie Windows upewnij się, że uruchamiasz skrypt z uprawnieniami administratora.
