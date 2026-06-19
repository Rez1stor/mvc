# MVC Labs 1-5

To repozytorium zawiera realizację laboratoriów 1-5, które demonstrują podstawowe zasady wzorca MVC na dwóch platformach: Django (Python) i ASP.NET Core (C#).

## Jak uruchomić aplikację w Django

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

## Jak uruchomić aplikację w .NET Core

1. Przejdź do folderu `TaskManager`:
   ```bash
   cd .NET/TaskManager
   ```
2. Uruchom aplikację:
   ```bash
   dotnet run
   ```
3. Otwórz link podany w konsoli (np. http://localhost:5000) w przeglądarce.
