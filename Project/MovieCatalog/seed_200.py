import os
import django
import sys
import requests

# Setup Django
sys.path.append(r'c:\Users\Ban\source\repos\mvc\mvc\Project\MovieCatalog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie, Director, Genre

# 200 Movies
MORE_MOVIES = [
    "The Silence of the Lambs", "Saving Private Ryan", "The Green Mile", "Spirited Away", "Interstellar", "Parasite", 
    "Leon", "The Usual Suspects", "The Lion King", "The Pianist", "Terminator 2: Judgment Day", "Back to the Future", 
    "Modern Times", "Psycho", "Gladiator", "City Lights", "Whiplash", "The Intouchables", "The Prestige", "The Departed", 
    "Memento", "Apocalypse Now", "Raiders of the Lost Ark", "Django Unchained", "WALL·E", "The Lives of Others", 
    "Sunset Blvd.", "Paths of Glory", "The Shining", "The Great Dictator", "Avengers: Infinity War", "Witness for the Prosecution", 
    "Aliens", "American Beauty", "Spider-Man: Into the Spider-Verse", "Dr. Strangelove", "The Dark Knight Rises", "Oldboy", "Joker", 
    "Amadeus", "Toy Story", "Braveheart", "Coco", "Das Boot", "Avengers: Endgame", "Princess Mononoke", "Once Upon a Time in America", 
    "Good Will Hunting", "Your Name.", "3 Idiots", "Singin' in the Rain", "Requiem for a Dream", "Toy Story 3", 
    "Star Wars: Episode VI - Return of the Jedi", "2001: A Space Odyssey", "Eternal Sunshine of the Spotless Mind", "Reservoir Dogs", 
    "High and Low", "Capernaum", "The Hunt", "Come and See", "Children of Heaven", "Amélie", "A Clockwork Orange", 
    "Double Indemnity", "Snatch", "Full Metal Jacket", "Scarface", "Hamilton", "Incendies", "To Kill a Mockingbird", 
    "The Sting", "Up", "Heat", "L.A. Confidential", "Taxi Driver", "Metropolis", "A Separation", "Die Hard", "Batman Begins", 
    "Indiana Jones and the Last Crusade", "Like Stars on Earth", "1917", "Downfall", "Howl's Moving Castle", "Pan's Labyrinth", 
    "The Secret in Their Eyes", "Green Book", "Spider-Man: No Way Home", "Ran", "The Truman Show", "Casino", "My Neighbor Totoro", 
    "The Elephant Man", "V for Vendetta", "The Big Lebowski", "The Wolf of Wall Street", "The Sixth Sense", "Shutter Island", 
    "No Country for Old Men", "Jurassic Park", "Finding Nemo", "The Thing", "Kill Bill: Vol. 1", "Blade Runner", "Fargo", 
    "Catch Me If You Can", "Mad Max: Fury Road", "Gran Torino", "Ford v Ferrari", "Million Dollar Baby", "A Beautiful Mind", 
    "Gone Girl", "Prisoners", "Zodiac", "Hacksaw Ridge", "Room", "Before Sunrise", "Before Sunset", "Rush", 
    "The Grand Budapest Hotel", "The Revenant", "Logan", "Spotlight", "Inside Out", "The Martian", "Gravity", "Dunkirk", 
    "Black Swan", "The Social Network", "Nightcrawler", "Drive", "Her", "Birdman", "Arrival", "La La Land", "Boyhood", 
    "Moonlight", "Jojo Rabbit", "Knives Out", "Everything Everywhere All at Once", "Top Gun: Maverick", "Oppenheimer", "Dune", 
    "Avatar", "The Avengers", "Iron Man", "Guardians of the Galaxy", "Deadpool", "Black Panther", "Wonder Woman", 
    "Thor: Ragnarok", "Spider-Man: Homecoming"
]

OMDB_API_KEY = "thewdb"

print("Fetching 150 movies from OMDb...")
added = 0
for title in MORE_MOVIES:
    if Movie.objects.filter(title=title).exists():
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
                director_name = data.get('Director', 'Unknown').split(',')[0]
                director, _ = Director.objects.get_or_create(name=director_name)
                
                genre_names = [g.strip() for g in data.get('Genre', '').split(',')]
                genres = []
                for g_name in genre_names:
                    if g_name and g_name != 'N/A':
                        genre, _ = Genre.objects.get_or_create(name=g_name)
                        genres.append(genre)
                
                try:
                    rating = float(data.get('imdbRating', 0))
                except ValueError:
                    rating = 0.0
                    
                try:
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
    except Exception as e:
        pass

print(f"Seeding complete. Added {added} movies. Total movies in DB: {Movie.objects.count()}")
