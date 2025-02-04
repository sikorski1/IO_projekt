# Testowanie

## Dlaczego Wybraliśmy Testy Manualne?

Zdecydowaliśmy się na manualne testowanie naszej aplikacji z dwóch głównych powodów:

### 1. Brak Doświadczenia w Testach Jednostkowych (Python)

* **Krzywa Uczenia:** Testy jednostkowe w Pythonie (np. z użyciem `unittest` czy `pytest`) wymagają pewnego poziomu wiedzy i doświadczenia. Nasz zespół, składający się ze studentów, nie posiada jeszcze wystarczającego doświadczenia w tym obszarze, aby efektywnie implementować testy jednostkowe na dużą skalę.
* **Ryzyko Błędów:** Nieprawidłowo napisane testy jednostkowe mogą wprowadzać fałszywe poczucie bezpieczeństwa, nie wykrywając rzeczywistych problemów w aplikacji. Woleliśmy uniknąć tej sytuacji, koncentrując się na testach, które jesteśmy w stanie sprawnie przeprowadzić.

### 2. Ograniczona Liczba Osób

* **Zasoby Czasowe:** Napisanie pełnego zestawu testów jednostkowych dla naszej aplikacji wymagałoby znaczących nakładów czasu. W naszym 3-osobowym zespole, musielibyśmy odciągnąć zasoby od innych ważnych zadań, takich jak projektowanie, implementacja i debugowanie.
* **Priorytety:** W obecnej fazie projektu, naszym priorytetem jest przede wszystkim dopracowanie funkcjonalności aplikacji i zapewnienie jej podstawowej użyteczności. Testy jednostkowe, choć ważne na dłuższą metę, nie są w tym momencie naszym głównym celem.

## Co Zyskujemy Dzięki Testom Manualnym?

Manualne testy, mimo tych ograniczeń, wciąż pozwalają nam na:

* **Wykrywanie Błędów z Perspektywy Użytkownika:** Testując aplikację ręcznie, możemy naśladować działania użytkownika i wyłapać problemy z interfejsem, intuicyjnością i UX/UI, które mogą umknąć innym rodzajom testów.
* **Elastyczność i Kreatywność:** Możemy testować różne scenariusze i kombinacje akcji, wychodząc poza ramy predefiniowanych testów.
* **Szybka Informacja Zwrotna:** Manualne testy dostarczają natychmiastowej informacji zwrotnej o tym, czy aplikacja działa zgodnie z oczekiwaniami, umożliwiając szybkie wprowadzanie poprawek.
* **Zaangażowanie Zespołu:** Dają każdemu z nas możliwość głębszego zrozumienia produktu i jego potencjalnych problemów.

# Video

Zdecydowaliśmy się nagrać video testujące funkcjonalności naszej aplikacji.

### Link do video z testami manualnymi oraz komentarzem:

https://youtu.be/UWin1OANvwI


## Raport z testów oprogramowania

### Opis
Niniejszy plik zawiera informacje dotyczące raportu z testów oprogramowania, w tym wykryte błędy oraz przetestowane funkcjonalności.

### 1. Wykryte błędy
W poniższej tabeli opisano wszystkie odkryte błędy wraz z informacją o ich usunięciu.

| Nr | Opis wykrytego błędu | Opis usunięcia błędu |
|----|--------------------|--------------------|
| 1  | Po kliknięciu „Convert” plik PDF zapisywany jest w błędnym katalogu. | Poprawione. Ścieżka zapisu została skorygowana w kodzie aplikacji. |
| 2  | Możliwość zaznaczenia plików o nieobsługiwanym formacie. | Poprawione. Dodano filtrowanie plików do obsługiwanych formatów. |
| 3  | Niepoprawne wyświetlanie nazw użytkowników w raportach. | Poprawione. Dodano mechanizm ręcznego przypisywania nazw użytkownikom. |
| 4  | Nie działa poprawnie zmiana języka zapisu notatek. | Poprawione. Naprawiono mechanizm wyboru języka. |
| 5  | Brak odpowiedniego komunikatu przy braku wybranego pliku do konwersji. | Poprawione. Dodano komunikaty błędów przy braku pliku PDF/TXT. |
| 6  | Błędne działanie funkcji nagrywania spotkań. | Poprawione. Naprawiono mechanizm rejestrowania audio i wideo. |
| 7  | Niepoprawne działanie progu podobieństwa slajdów. | Poprawione. Mechanizm porównywania obrazów został usprawniony. |
| 8  | Aplikacja nie zamyka się poprawnie po zakończeniu nagrywania. | Poprawione. Dodano poprawną obsługę zamykania aplikacji. |

### 2. Przetestowane funkcjonalności
W poniższej tabeli opisano wszystkie przetestowane funkcjonalności oraz uwagi dotyczące ich działania.

| Nr | Funkcjonalność | Uwagi |
|----|---------------|--------------------|
| 1  | Konwersja pliku TXT do PDF | Działa poprawnie. Plik PDF zapisywany w odpowiednim katalogu. |
| 2  | Otwieranie wygenerowanego pliku PDF | Plik otwierany w osobnym oknie. |
| 3  | Ręczne przypisywanie nazw użytkownikom | Zmiany zapisują się poprawnie. |
| 4  | Zmiana języka transkrypcji i notatek | Działa poprawnie, język zmienia się zgodnie z wyborem użytkownika. |
| 5  | Nagrywanie spotkań i generowanie raportów | Działa poprawnie, zapisując transkrypcję oraz podział na speakerów. |
| 6  | Obsługa błędów (np. brak wybranego pliku) | Działa poprawnie, wyświetlane są odpowiednie komunikaty. |
| 7  | Automatyczne wykrywanie slajdów podczas nagrywania | Działa poprawnie, nowe slajdy są wykrywane na podstawie progu podobieństwa. |
| 8  | Obsługa różnych formatów plików wejściowych | Obsługiwane są jedynie zgodne formaty plików, poprawna walidacja. |
| 9  | Poprawne zamykanie aplikacji po zakończeniu nagrywania | Zamyka się bez błędów. |
