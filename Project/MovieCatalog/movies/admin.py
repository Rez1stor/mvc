from django.contrib import admin
from .models import Director, Genre, Movie, Review, Rating, Favorite, UserMovieStatus

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating', 'director')
    list_filter = ('genres', 'director')
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'movie__title', 'user__username')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'score')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user')

@admin.register(UserMovieStatus)
class UserMovieStatusAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'status')
