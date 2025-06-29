# inside the app imports
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import ReviewForm, CustomUserCreationForm
from reminder.models import Album, Review, Song, Artist, Genre

# other stuff
from typing import Union
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=config('SPOTIPY_CLIENT_ID'),
    client_secret=config('SPOTIPY_CLIENT_SECRET')
))


# app views
def index(request):
    albums = Album.objects.all()
    return render(request, 'reminder/test.html',
                  {
                      'show_albums': True,
                      'some_list': albums
                      }
                  )


def album_details(request, album_slug):
    try:
        selected_album = Album.objects.get(slug=album_slug)
        has_reviews = Review.objects.filter(album=selected_album).exists()
        if has_reviews:
            ratings = list(Review.objects.filter(album=selected_album).values_list('rating', flat=True))
            avg_rating = sum(ratings) / len(ratings)
            avg_rating = round(avg_rating, 1)
        else:
            avg_rating = 'Not rated'

        genres = selected_album.genres.all()

        songs = selected_album.songs.all()
        spotify_album_id = find_album_spotify_id(selected_album.title, selected_album.artist.name)
        if spotify_album_id:
            spotify_tracklist = get_an_album_tracklist(spotify_album_id)
        else:
            spotify_tracklist = None

        if spotify_tracklist:
            tracklist = spotify_tracklist
        else:
            max_tracks = selected_album.number_of_songs
            tracklist: list[Union[dict, None]] = [None] * max_tracks
            for song in songs:
                if song.track_number and 1 <= song.track_number <= max_tracks:
                    tracklist[song.track_number - 1] = {
                        'title': song.title,
                        'track_number': song.track_number,
                        'duration': format_duration(song.duration),
                        'slug': song.slug,
                        'description': song.description
                    }

        user_review = None

        if request.user.is_authenticated:
            try:
                user_review = Review.objects.get(user=request.user, album=selected_album)
            except Review.DoesNotExist:
                user_review = None

        if request.method == "GET":
            if user_review:
                review_form = ReviewForm(instance=user_review)
            else:
                review_form = ReviewForm()
            return render(request, 'reminder/album_detail.html',
                          {
                              'album': selected_album,
                              'album_found': True,
                              'genres': genres,
                              'avg_rating': avg_rating,
                              'form': review_form,
                              'tracklist': tracklist
                              }
                          )
        else:
            if user_review:
                review_form = ReviewForm(request.POST, instance=user_review)
            else:
                review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.album = selected_album
                review.user = request.user
                review.save()
                return redirect('album_details', album_slug=album_slug)

    except Exception as e:
            return render(request, 'reminder/album_detail.html',
                          {
                              'album_found': False
                              }
                          )


def song_details(request, song_slug):
    selected_song = Song.objects.get(slug=song_slug)
    return render(request, 'reminder/song_detail.html', {'song': selected_song})


def artist_details(request, artist_slug):
    selected_artist = Artist.objects.get(slug=artist_slug)
    albums = selected_artist.albums.order_by('release_date')
    return render(request, 'reminder/artist_detail.html',
                  {'artist': selected_artist, 'albums': albums})


def genre_details(request, genre_slug):
    selected_genre = Genre.objects.get(slug=genre_slug)
    return render(request, 'reminder/genre_detail.html',
                  {'genre': selected_genre})


def search(request):
    if request.method == 'POST':
        result = request.POST['searched']
        albums = Album.objects.filter(title__icontains=result)
        songs = Song.objects.filter(title__icontains=result)
        artists = Artist.objects.filter(name__icontains=result)
        return render(request, 'reminder/search_result.html',
                      {'result': result, 'albums': albums, 'songs': songs, 'artists': artists}
                      )
    else:
        result = None
        return render(request, 'reminder/search_result.html',
                      {'result': result})


# user authorization and authentication
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'reminder/registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'reminder/login.html', {"form": form})


def logout_user(request):
    logout(request)
    return redirect('login')


# additional functions
def find_album_spotify_id(album_title, artist_name):
    query = f'album:{album_title} artist:{artist_name}'
    results = sp.search(q=query, type='album', limit=1)
    items = results['albums']['items']
    if items:
        return items[0]['id']
    return None


def get_an_album_tracklist(album_id):
    if not album_id:
        return []
    results = sp.album_tracks(album_id)
    return [
        {
            'track_number': t['track_number'],
            'title': t['name'],
            'duration': format_spotify_duration(t['duration_ms']),
            'preview_url': t['preview_url']
        }
        for t in results['items']
    ]


def format_spotify_duration(ms):
    seconds = (ms // 1000) % 60
    minutes = (ms // (1000 * 60))
    return f"{minutes}:{seconds:02d}"


def format_duration(td):
    if not td:
        return ""
    total_seconds = int(td.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}:{seconds:02d}"

