# Repozytorium - Wzorzec MVC w tworzeniu aplikacji internetowych

To repozytorium zawiera realizację laboratoriów (Django i .NET) oraz **Projekt Zaliczeniowy** z przedmiotu.

---

# Projekt Zaliczeniowy

## Tytuł i nazwa wybranego projektu
**Tytuł zadania:** Zadanie 12 – Katalog kolekcji filmów  
**Nazwa projektu:** Movie Catalog

## Spis treści
1. [Tytuł i nazwa wybranego projektu](#tytuł-i-nazwa-wybranego-projektu)
2. [Lista i krótki opis zaimplementowanych funkcjonalności](#lista-i-krótki-opis-zaimplementowanych-funkcjonalności)
3. [Instrukcje obsługi](#instrukcje-obsługi)
4. [Architektura MVC w projekcie](#architektura-mvc-w-projekcie)
5. [Realizacja wymagań na wyższą ocenę (powyżej 3.0)](#realizacja-wymagań-na-wyższą-ocenę-powyżej-30)
6. [Kod źródłowy aplikacji](#kod-źródłowy-aplikacji)
7. [Plik z przykładowymi danymi wejściowymi](#plik-z-przykładowymi-danymi-wejściowymi)

## Lista i krótki opis zaimplementowanych funkcjonalności
- **Przeglądanie listy filmów:** Wyświetlanie całego katalogu dostępnych w bazie filmów.
- **Szczegóły filmu:** Wyświetlanie pełnych informacji, w tym plakatu, opisu, reżysera, gatunków oraz dodanych recenzji.
- **Dodawanie i edycja (Formularze):** Możliwość ręcznego i zautomatyzowanego dodawania nowych filmów oraz edycji ich detali.
- **Konta użytkowników i system autoryzacji:** Rejestracja, logowanie i zarządzanie profilem (np. zmiana awatara, hasła).
- **Ocenianie i recenzje:** Użytkownicy mogą pisać recenzje oraz wystawiać oceny w skali 1-10.
- **Listy użytkownika (Statusy):** Śledzenie statusu oglądania dla każdego filmu (np. "Obejrzane", "Do obejrzenia", "Ulubione").
- **Wyszukiwanie i filtrowanie:** Błyskawiczne wyszukiwanie filmów po tytule oraz filtrowanie zasobów po powiązanych gatunkach.
- **Automatyczne pobieranie danych API:** System podpowiedzi tytułów z zewnętrznego OMDb API, który pozwala przy tworzeniu filmu jednym kliknięciem pobrać wszystkie metadane.

## Instrukcje obsługi
### Jak uruchomić aplikację, jakie paczki należy zainstalować i w jaki sposób
Aplikacja została napisana w języku Python przy użyciu frameworka Django. 

1. Przejdź do głównego folderu projektu (`Project/MovieCatalog`):
   ```bash
   cd Project/MovieCatalog
   ```
2. Stwórz i aktywuj środowisko wirtualne:
   - **Windows:** `python -m venv venv` a następnie `.\venv\Scripts\activate`
   - **Linux/Mac:** `python3 -m venv venv` a następnie `source venv/bin/activate`
3. Zainstaluj wymagane paczki za pomocą wbudowanego instalatora `pip`:
   ```bash
   pip install django requests
   ```
   *(Paczka `django` to główny framework MVC, a biblioteka `requests` jest potrzebna do komunikacji HTTP z API OMDb).*
4. Wykonaj migracje struktury bazy danych:
   ```bash
   python manage.py migrate
   ```
5. Uruchom serwer deweloperski:
   ```bash
   python manage.py runserver
   ```
6. Gotowa aplikacja będzie w pełni dostępna w przeglądarce pod adresem: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Architektura MVC w projekcie
Projekt ściśle realizuje założenia wzorca architektonicznego MVC (w Django funkcjonującego pod nazwą MVT - Model-View-Template) ze szczególnym uwzględnieniem wymagań dla *Zadania 12*:
- **Model:** Reprezentowany m.in. przez główną klasę `Movie` (posiadającą wymagane pola: tytuł, reżyser, ocena) zdefiniowaną w pliku `models.py`.
- **Kontroler (View w Django):** Odpowiadają za to funkcje i klasy widoków w `views.py`. Obsługują one żądania HTTP, wyciągają i przygotowują dane w Modelach i przekazują gotowy kontekst do szablonów HTML.
- **Widok (Template w Django):** Szablony znajdujące się w plikach `.html` (np. lista widoków w `index.html` czy formularz dodawania/edycji w `movie_form.html`), które generują estetyczny interfejs dla końcowego użytkownika na bazie przekazanych danych.

## Realizacja wymagań na wyższą ocenę (powyżej 3.0)
Aby uzyskać ocenę wyższą niż 3.0, zgodnie z instrukcją należało wykonać co najmniej dwie modyfikacje. W niniejszym projekcie zrealizowano ich znacznie więcej:
1. **Dodanie dwóch dodatkowych modeli oraz relacji pomiędzy nimi:** Zaimplementowano dodatkowe, zaawansowane modele takie jak `Director`, `Genre`, `Review`, `Rating`, `Favorite` oraz `UserMovieStatus` wraz z relacjami kluczy obcych (One-to-Many oraz Many-to-Many) pomiędzy nimi a modelem głównym `Movie`.
2. **Dodanie ostylowanej tabeli lub widoku pojedynczego obiektu w sposób schludny wizualnie:** Stworzono bardzo nowoczesny interfejs wizualny w stylu "Glassmorphism" używając zaawansowanych arkuszy CSS i mikro-animacji, a także w pełni ostylowany widok szczegółów filmu.
3. **Zastosowanie zewnętrznego API:** Aplikacja dynamicznie integruje się z **OMDb API**. Przy ręcznym dodawaniu filmu serwer odpytuje zewnętrzne API i potrafi całkowicie automatycznie pobrać plakat, reżysera, rok wydania, gatunki i poprawny opis.
4. **Dodanie funkcji filtrowania i wyszukiwania:** Katalog filmów udostępnia wyszukiwarkę tytułów oraz elastyczne filtrowanie wyników według wszystkich zdefiniowanych gatunków.
5. **Zaimplementowanie logiki sesji użytkownika i prostego systemu logowania:** Dodano pełen system zarządzania kontami oparty na bezpiecznych sesjach. Krytyczne funkcje takie jak dodawanie filmów, recenzowanie i modyfikacja własnych list zapisanych filmów są chronione i dostępne wyłącznie po poprawnej autoryzacji.
6. **Dodanie walidacji po stronie serwera oraz klienta:** Zaimplementowano walidację formularzy poprzez wymagane atrybuty w HTML5 na froncie oraz restrykcyjną weryfikację na backendzie (np. blokowanie duplikatów przy tworzeniu nowych filmów o identycznym tytule i roku).

## Kod źródłowy aplikacji
Cały kod źródłowy aplikacji znajduje się w głównym katalogu tego repozytorium GitHub, a ściślej w ścieżce `Project/MovieCatalog/`. Główna aplikacja definiująca zachowanie wzorca MVC spoczywa w podkatalogu `movies/` (pliki `models.py`, `views.py`, folder `templates`).

## Plik z przykładowymi danymi wejściowymi
Repozytorium zawiera w sobie wygenerowany już plik bazy danych `db.sqlite3`, który posiada setki prawidłowych rekordów pobranych z API, dzięki czemu można od razu rozpocząć testowanie aplikacji.
Ponadto aplikacja posiada skrypt **`seed_200.py`**, który pełni rolę generatora danych (dane wejściowe) potrafiącego w kilkanaście sekund napełnić zupełnie pustą bazę danych wysokiej jakości próbnymi filmami od zera.

---

# Laboratoria 1-5
Poniżej znajdują się instrukcje uruchomieniowe do zadań z wcześniejszych laboratoriów zawartych w tym repozytorium.

## Jak uruchomić aplikację w Django (Lab)
1. Przejdź do folderu `Django`:
   ```bash
   cd Django
   ```
2. Aktywuj środowisko wirtualne:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Uruchom serwer:
   ```bash
   python manage.py runserver
   ```
4. Otwórz http://127.0.0.1:8000/ w przeglądarce.

## Jak uruchomić aplikację w .NET Core (Lab)
1. Przejdź do folderu `TaskManager`:
   ```bash
   cd .NET/TaskManager
   ```
2. Uruchom aplikację:
   ```bash
   dotnet run
   ```
3. Otwórz link podany w konsoli (np. http://localhost:5000) w przeglądarce.
