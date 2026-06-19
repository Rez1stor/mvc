from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('search/', views.movie_search, name='movie_search'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/new/', views.movie_create, name='movie_create'),
    path('movie/<int:pk>/edit/', views.movie_update, name='movie_update'),
    path('movie/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    
    # User auth
    path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='movie_list'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/password/', views.change_password_view, name='change_password'),
    path('settings/delete/', views.delete_account_view, name='delete_account'),
    
    # Interactions
    path('movie/<int:pk>/review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('movie/<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('movie/<int:pk>/status/', views.update_status, name='update_status'),
    path('movie/<int:pk>/rate/', views.rate_movie, name='rate_movie'),
    
    # API endpoints
    path('api/search/', views.api_search_movies, name='api_search_movies'),
    path('api/details/', views.api_get_movie_details, name='api_get_movie_details'),
]
