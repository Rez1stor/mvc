from django import forms
from .models import Movie
from .omdb_api import fetch_movie_details

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'release_year', 'rating', 'description', 'poster_url', 'director', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'poster_url': forms.URLInput(attrs={'class': 'form-control'}),
            'director': forms.Select(attrs={'class': 'form-select'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-select'})
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        release_year = cleaned_data.get('release_year')
        
        if title and release_year:
            qs = Movie.objects.filter(title__iexact=title, release_year=release_year)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
                
            if qs.exists():
                raise forms.ValidationError(f"Movie '{title}' ({release_year}) already exists in the catalog!")
                
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # If description or poster is empty, try to fetch from OMDb API
        if not instance.description or not instance.poster_url:
            details = fetch_movie_details(instance.title)
            if details:
                if not instance.description and details['description']:
                    instance.description = details['description']
                if not instance.poster_url and details['poster_url']:
                    instance.poster_url = details['poster_url']
                    
        if commit:
            instance.save()
            self.save_m2m()
            
        return instance

from django.contrib.auth.models import User
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar_emoji']
        widgets = {
            'avatar_emoji': forms.HiddenInput(),
        }
