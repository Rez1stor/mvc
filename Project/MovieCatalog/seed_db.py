import os
import django
import sys
import requests

# Setup Django
sys.path.append(r'c:\Users\Ban\source\repos\mvc\mvc\Project\MovieCatalog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from movies.models import Movie, Director, Genre

# 1. Create Superuser
username = 'пароль'
password = 'адмін'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, 'admin@example.com', password)
    print(f"Created admin user: {username}")
else:
    print(f"Admin user {username} already exists.")

# 2. Seed 50 Movies
TOP_MOVIES = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight", "12 Angry Men", 
    "Schindler's List", "The Lord of the Rings: The Return of the King", "Pulp Fiction", 
    "The Lord of the Rings: The Fellowship of the Ring", "The Good, the Bad and the Ugly", 
    "Forrest Gump", "Fight Club", "Inception", "The Lord of the Rings: The Two Towers", 
    "Star Wars: Episode V - The Empire Strikes Back", "The Matrix", "Goodfellas", 
    "One Flew Over the Cuckoo's Nest", "Se7en", "Seven Samurai", "It's a Wonderful Life", 
    "The Silence of the Lambs", "City of God", "Saving Private Ryan", "Life Is Beautiful", 
    "The Green Mile", "Interstellar", "Star Wars: Episode IV - A New Hope", 
    "Terminator 2: Judgment Day", "Back to the Future", "Spirited Away", "Psycho", 
    "The Pianist", "Leon: The Professional", "Parasite", "The Lion King", "Gladiator", 
    "American History X", "The Departed", "The Usual Suspects", "The Prestige", 
    "Whiplash", "Casablanca", "The Intouchables", "Modern Times", "Cinema Paradiso", 
    "Once Upon a Time in the West", "Rear Window", "Alien", "City Lights", "Apocalypse Now"
]

OMDB_API_KEY = "thewdb"

print("Fetching movies from OMDb...")
added = 0
for title in TOP_MOVIES:
    if Movie.objects.filter(title=title).exists():
        print(f"Skipping {title}, already exists.")
        continue
        
    try:
        response = requests.get("http://www.omdbapi.com/", params={
            'apikey': OMDB_API_KEY,
            't': title,
            'plot': 'full'
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                # Get or create Director
                director_name = data.get('Director', 'Unknown').split(',')[0] # just take the first director
                director, _ = Director.objects.get_or_create(name=director_name)
                
                # Get or create Genres
                genre_names = [g.strip() for g in data.get('Genre', '').split(',')]
                genres = []
                for g_name in genre_names:
                    if g_name and g_name != 'N/A':
                        genre, _ = Genre.objects.get_or_create(name=g_name)
                        genres.append(genre)
                
                # Parse rating and year
                try:
                    rating = float(data.get('imdbRating', 0))
                except ValueError:
                    rating = 0.0
                    
                try:
                    # Sometimes year is like "1999–"
                    year_str = data.get('Year', '2000')[:4]
                    year = int(year_str)
                except ValueError:
                    year = 2000
                    
                poster = data.get('Poster')
                if poster == "N/A": poster = None
                
                movie = Movie.objects.create(
                    title=data.get('Title', title),
                    release_year=year,
                    rating=rating,
                    description=data.get('Plot', ''),
                    poster_url=poster,
                    director=director
                )
                
                movie.genres.set(genres)
                print(f"Added: {movie.title}")
                added += 1
            else:
                print(f"OMDb Error for {title}: {data.get('Error')}")
    except Exception as e:
        print(f"Error fetching {title}: {e}")

print(f"Seeding complete. Added {added} movies.")
