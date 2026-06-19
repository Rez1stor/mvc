from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Movie, Genre, Director, Review, Rating, Favorite, UserMovieStatus
from .forms import MovieForm, UserUpdateForm, UserProfileUpdateForm
from .omdb_api import search_movies, fetch_full_movie_details
from .recommendations import get_collaborative_recommendations

def movie_list(request):
    movies = Movie.objects.all().order_by('-release_year')
    genres = Genre.objects.all()
    
    # Filtering & Sorting
    query = request.GET.get('q')
    genre_id = request.GET.get('genre')
    sort = request.GET.get('sort', '-release_year')
    
    valid_sorts = ['-release_year', 'release_year', '-rating', 'rating', 'title', '-title']
    if sort not in valid_sorts:
        sort = '-release_year'
        
    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
        
    movies = movies.order_by(sort)
        
    context = {
        'movies': movies,
        'genres': genres,
        'selected_genre': int(genre_id) if genre_id and genre_id.isdigit() else None,
        'query': query or '',
        'current_sort': sort
    }
    return render(request, 'movies/movie_list.html', context)

def movie_search(request):
    """HTMX endpoint: returns only the movie cards partial for live search."""
    movies = Movie.objects.all().order_by('-release_year')
    
    query = request.GET.get('q')
    genre_id = request.GET.get('genre')
    sort = request.GET.get('sort', '-release_year')
    
    valid_sorts = ['-release_year', 'release_year', '-rating', 'rating', 'title', '-title']
    if sort not in valid_sorts:
        sort = '-release_year'
    
    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
        
    movies = movies.order_by(sort)
    
    return render(request, 'movies/partials/movie_cards.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    # Load user specific data if authenticated
    user_rating = None
    is_favorite = False
    user_status = None
    
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(movie=movie, user=request.user).first()
        is_favorite = Favorite.objects.filter(movie=movie, user=request.user).exists()
        status_obj = UserMovieStatus.objects.filter(movie=movie, user=request.user).first()
        if status_obj:
            user_status = status_obj.status
            
    reviews = movie.reviews.all().order_by('-created_at')
    user_review = reviews.filter(user=request.user).first() if request.user.is_authenticated else None
    
    # Get similar movies by genre (up to 4)
    similar_movies = Movie.objects.filter(genres__in=movie.genres.all()).exclude(id=movie.id).distinct().order_by('-rating')[:4]
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'user_review': user_review,
        'user_rating': user_rating.score if user_rating else 0,
        'is_favorite': is_favorite,
        'user_status': user_status,
        'status_choices': UserMovieStatus.STATUS_CHOICES,
        'similar_movies': similar_movies
    }
    return render(request, 'movies/movie_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'Add Movie'})

@user_passes_test(lambda u: u.is_superuser)
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'Edit Movie', 'movie': movie})

@user_passes_test(lambda u: u.is_superuser)
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})

# --- Auth & Profile ---

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'movies/register.html', {'form': form})

@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    statuses = UserMovieStatus.objects.filter(user=request.user).select_related('movie')
    reviews = Review.objects.filter(user=request.user).select_related('movie')
    return render(request, 'movies/profile.html', {
        'favorites': favorites,
        'statuses': statuses,
        'reviews': reviews,
        'status_choices': UserMovieStatus.STATUS_CHOICES
    })

@login_required
def settings_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)
        
    password_form = PasswordChangeForm(request.user)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'emojis': ['👤', '👨', '👩', '🤖', '👻', '👽', '👾', '🤡', '🦁', '🐶', '🐱', '🦊', '🐼', '🦄', '🦇', '🦉', '😎', '🤓', '🤠', '😇']
    }
    return render(request, 'movies/settings.html', context)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    return redirect('settings')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('movie_list')
    return redirect('settings')

# --- Interactions ---

@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Review.objects.update_or_create(
                movie=movie, user=request.user,
                defaults={'text': text}
            )
    return redirect('movie_detail', pk=pk)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_pk = review.movie.pk
    # User can delete their own review, admin can delete any review
    if request.user == review.user or request.user.is_superuser:
        review.delete()
    return redirect('movie_detail', pk=movie_pk)

@login_required
def toggle_favorite(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    fav, created = Favorite.objects.get_or_create(movie=movie, user=request.user)
    if not created:
        fav.delete()
        is_fav = False
    else:
        is_fav = True
    
    # Return HTML snippet for HTMX
    icon_color = "#E50914" if is_fav else "none"
    stroke_color = "#E50914" if is_fav else "currentColor"
    return HttpResponse(f'''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="{icon_color}" stroke="{stroke_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
    ''')

@login_required
def update_status(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            obj, created = UserMovieStatus.objects.update_or_create(
                movie=movie, user=request.user,
                defaults={'status': status}
            )
        else:
            UserMovieStatus.objects.filter(movie=movie, user=request.user).delete()
    return HttpResponse("Saved")

@login_required
def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        score = request.POST.get('score')
        if score and score.isdigit():
            Rating.objects.update_or_create(
                movie=movie, user=request.user,
                defaults={'score': int(score)}
            )
    return HttpResponse("Saved")

def recommendations_view(request):
    """
    Displays personalized recommendations and overall trending movies.
    """
    # 1. Trending / Popular movies (top 8 by global rating, could also use review count or recent dates)
    trending_movies = Movie.objects.all().order_by('-rating')[:8]
    
    # 2. Personalized recommendations
    personalized_movies = []
    has_enough_data = False
    
    if request.user.is_authenticated:
        personalized_movies = get_collaborative_recommendations(request.user, limit=8)
        # If personalized_movies is empty, it might mean they haven't liked enough movies yet,
        # or there are no similar users. We can flag this for the template.
        has_enough_data = Rating.objects.filter(user=request.user, score__gte=7).exists() or Favorite.objects.filter(user=request.user).exists()
        
    context = {
        'trending_movies': trending_movies,
        'personalized_movies': personalized_movies,
        'has_enough_data': has_enough_data
    }
    return render(request, 'movies/recommendations.html', context)

# --- API Endpoints for OMDb Autocomplete ---

@login_required
def api_search_movies(request):
    query = request.GET.get('q', '')
    if len(query) < 3:
        return JsonResponse({'results': []})
    
    results = search_movies(query)
    return JsonResponse({'results': results})

@login_required
def api_get_movie_details(request):
    imdb_id = request.GET.get('id', '')
    if not imdb_id:
        return JsonResponse({'error': 'No ID provided'}, status=400)
        
    details = fetch_full_movie_details(imdb_id)
    if not details:
        return JsonResponse({'error': 'Movie not found'}, status=404)
        
    # Create or get director
    director_data = None
    director_name = details.get('Director', 'Unknown')
    if director_name and director_name != 'N/A':
        director_obj, _ = Director.objects.get_or_create(name=director_name)
        director_data = {'id': director_obj.id, 'name': director_obj.name}
        
    # Create or get genres
    genres_data = []
    genres_str = details.get('Genre', '')
    if genres_str and genres_str != 'N/A':
        genre_names = [g.strip() for g in genres_str.split(',')]
        for g_name in genre_names:
            genre_obj, _ = Genre.objects.get_or_create(name=g_name)
            genres_data.append({'id': genre_obj.id, 'name': genre_obj.name})
            
    # Parse release year
    try:
        year_str = details.get('Year', '0')[:4]
        release_year = int(year_str) if year_str.isdigit() else 2000
    except:
        release_year = 2000
        
    # Parse rating
    try:
        rating_str = details.get('imdbRating', '0')
        rating = float(rating_str)
    except:
        rating = 0.0
        
    poster = details.get('Poster')
    if poster == 'N/A':
        poster = ''
        
    return JsonResponse({
        'title': details.get('Title', ''),
        'release_year': release_year,
        'rating': rating,
        'description': details.get('Plot', ''),
        'poster_url': poster,
        'director_data': director_data,
        'genres_data': genres_data
    })
