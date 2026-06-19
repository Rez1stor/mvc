from django.db.models import Count, Q
from .models import Movie, Rating, Favorite

def get_collaborative_recommendations(user, limit=8):
    """
    Returns personalized movie recommendations for a user based on collaborative filtering.
    """
    if not user.is_authenticated:
        return []

    # 1. Get movies liked by the current user (Favorites or Rating >= 7)
    liked_favorites = Favorite.objects.filter(user=user).values_list('movie_id', flat=True)
    liked_ratings = Rating.objects.filter(user=user, score__gte=7).values_list('movie_id', flat=True)
    
    current_user_liked_movie_ids = set(liked_favorites) | set(liked_ratings)
    
    if not current_user_liked_movie_ids:
        return [] # Not enough data to personalize

    # 2. Find other users who liked at least one of these movies
    other_users_favs = Favorite.objects.exclude(user=user).filter(movie_id__in=current_user_liked_movie_ids)
    other_users_ratings = Rating.objects.exclude(user=user).filter(movie_id__in=current_user_liked_movie_ids, score__gte=7)
    
    # Calculate similarity score for each other user
    # similarity = number of common liked movies
    user_similarity = {}
    
    for fav in other_users_favs:
        user_similarity[fav.user_id] = user_similarity.get(fav.user_id, 0) + 1
        
    for rating in other_users_ratings:
        user_similarity[rating.user_id] = user_similarity.get(rating.user_id, 0) + 1

    if not user_similarity:
        return []

    # 3. Find movies liked by these similar users that the current user hasn't liked
    # (We also exclude movies the user has explicitly rated poorly or marked as not_interested, 
    # but for simplicity, we'll just exclude all movies the user has rated or favorited)
    
    all_user_interacted = set(Rating.objects.filter(user=user).values_list('movie_id', flat=True)) | set(liked_favorites)
    
    recommended_movies_scores = {}
    
    # Get all favorites from similar users
    similar_users_favs = Favorite.objects.filter(user_id__in=user_similarity.keys()).exclude(movie_id__in=all_user_interacted)
    for fav in similar_users_favs:
        movie_id = fav.movie_id
        score = user_similarity[fav.user_id]
        recommended_movies_scores[movie_id] = recommended_movies_scores.get(movie_id, 0) + score
        
    # Get all positive ratings from similar users
    similar_users_ratings = Rating.objects.filter(user_id__in=user_similarity.keys(), score__gte=7).exclude(movie_id__in=all_user_interacted)
    for rating in similar_users_ratings:
        movie_id = rating.movie_id
        score = user_similarity[rating.user_id]
        recommended_movies_scores[movie_id] = recommended_movies_scores.get(movie_id, 0) + score

    # Sort movies by score descending
    sorted_movie_ids = sorted(recommended_movies_scores, key=recommended_movies_scores.get, reverse=True)[:limit]
    
    if not sorted_movie_ids:
        return []
        
    # Fetch movie objects while preserving the sorted order
    movies = Movie.objects.filter(id__in=sorted_movie_ids)
    # Sort them in python to keep the recommendation order
    movie_dict = {m.id: m for m in movies}
    return [movie_dict[m_id] for m_id in sorted_movie_ids if m_id in movie_dict]
