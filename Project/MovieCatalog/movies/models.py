from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_emoji = models.CharField(max_length=10, default='👤')

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

class Director(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    biography = models.TextField(blank=True, null=True, verbose_name="Biography")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date")

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    release_year = models.IntegerField(verbose_name="Release Year")
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        verbose_name="Rating"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    poster_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Poster URL")
    
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies', verbose_name="Director", null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name="Genres", blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Review")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.movie.title}"

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title} {self.score}/10"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} favorites {self.movie.title}"

class UserMovieStatus(models.Model):
    STATUS_CHOICES = [
        ('watched', 'Watched'),
        ('want_to_watch', 'Want to watch'),
        ('watching', 'Watching'),
        ('not_interested', 'Not interested'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.status}"
