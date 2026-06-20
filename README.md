# Wzorzec MVC w tworzeniu aplikacji internetowych

**Imię i nazwisko:** Matvii Ravlyk  
**Numer indeksu:** 64151 

To repozytorium zawiera realizację zadań laboratoryjnych (1-5) oraz projekt zaliczeniowy z przedmiotu.

## Spis treści
1. [Projekt Zaliczeniowy: Movie Catalog (Zadanie 12)](#projekt-zaliczeniowy-movie-catalog-zadanie-12)
2. [Laboratoria (Tutoriale)](#laboratoria-tutoriale)
    - [Tutorial Django (Lab 2 i 3)](#tutorial-django-lab-2-i-3)
    - [Tutorial .NET Core MVC (Lab 4 i 5)](#tutorial-net-core-mvc-lab-4-i-5)

---

## Projekt Zaliczeniowy: Movie Catalog (Zadanie 12)

Katalog filmów stworzony w Pythonie z wykorzystaniem frameworka Django. Projekt opiera się na architekturze MVC (w Django znanej jako MVT - Model-View-Template).

### Krótki opis funkcjonalności:
- Przeglądanie bazy filmów, wyszukiwanie po tytule oraz filtrowanie po gatunkach.
- Zautomatyzowane dodawanie nowych filmów — system integruje się z OMDb API i samodzielnie pobiera plakat, reżysera, rok wydania oraz opis.
- Rejestracja, logowanie i zarządzanie własnym profilem użytkownika.
- System recenzji, wystawiania ocen (1-10) i dodawania filmów do list (np. "Ulubione", "Do obejrzenia").
- Rozbudowane relacje w bazie danych (wiele modeli połączonych kluczami obcymi).

### Instrukcja uruchomienia projektu
1. Przejdź do katalogu projektu:
   ```bash
   cd Project/MovieCatalog
   ```
2. Utwórz i aktywuj środowisko wirtualne (Windows):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Zainstaluj wymagane pakiety:
   ```bash
   pip install django requests
   ```
4. Wykonaj migracje bazy danych:
   ```bash
   python manage.py migrate
   ```
5. Uruchom serwer:
   ```bash
   python manage.py runserver
   ```
*(Aplikacja zawiera już plik `db.sqlite3` z przykładowymi danymi, więc po uruchomieniu można od razu z niej korzystać).*

---

## Laboratoria (Tutoriale)

Zgodnie z wymaganiami zajęć, w repozytorium znajdują się również zrealizowane oficjalne tutoriale.

### Tutorial Django (Lab 2 i 3)
Aplikacja "Polls" napisana z wykorzystaniem Django (części 1-7 tutoriala, w tym zaimplementowane testy).
- **Ścieżka:** `Django/mysite`
- **Uruchomienie:** `python manage.py runserver` (w folderze `mysite`)
- **Testy:** `python manage.py test polls`

### Tutorial .NET Core MVC (Lab 4 i 5)
Aplikacja "MvcMovie" napisana z wykorzystaniem ASP.NET Core MVC oraz Entity Framework Core.
- **Ścieżka:** `dotNET/MvcMovie`
- **Uruchomienie:** `dotnet run` (w folderze `MvcMovie`)
