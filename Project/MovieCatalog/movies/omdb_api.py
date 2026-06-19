import requests
import os

# Typically the API key is hidden in .env file, but for educational purposes we use 
# a free test key. If it stops working, you need to register 
# your own at omdbapi.com
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'thewdb')
BASE_URL = "http://www.omdbapi.com/"

def fetch_movie_details(title):
    """
    Calls OMDb API by movie title.
    Returns a dictionary with description and poster URL.
    """
    try:
        response = requests.get(BASE_URL, params={
            'apikey': OMDB_API_KEY,
            't': title,
            'plot': 'full'
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                poster = data.get('Poster')
                # If poster is missing in API, it returns "N/A"
                if poster == "N/A":
                    poster = None
                
                return {
                    'description': data.get('Plot'),
                    'poster_url': poster
                }
    except Exception as e:
        print(f"Error requesting OMDb API: {e}")
    
    return None

def search_movies(query):
    """
    Calls OMDb API by search query (s).
    Returns a list of results.
    """
    try:
        response = requests.get(BASE_URL, params={
            'apikey': OMDB_API_KEY,
            's': query,
            'type': 'movie'
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data.get('Search', [])
    except Exception as e:
        print(f"Error requesting OMDb API (search): {e}")
        
    return []

def fetch_full_movie_details(imdb_id):
    """
    Calls OMDb API by imdbID (i).
    Returns all necessary details about the movie.
    """
    try:
        response = requests.get(BASE_URL, params={
            'apikey': OMDB_API_KEY,
            'i': imdb_id,
            'plot': 'full'
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data
    except Exception as e:
        print(f"Error requesting OMDb API (details): {e}")
        
    return None
