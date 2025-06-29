from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.register_user, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
    path('albums/<slug:album_slug>', views.album_details, name='album_details'),
    path('songs/<slug:song_slug>', views.song_details, name='song_details'),
    path('artists/<slug:artist_slug>', views.artist_details, name='artist_details'),
    path('genres/<slug:genre_slug>', views.genre_details, name='genre_details'),

]

