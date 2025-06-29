from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.
class Artist(models.Model):
        name = models.CharField(max_length=100, unique=True)
        bio = models.TextField(blank=True, null=True)
        slug = models.SlugField(unique=True)

        def __str__(self):
                return f'{self.name}'


class Album(models.Model):
        title = models.CharField(max_length=100)
        artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
        release_date = models.DateField()
        description = models.TextField()
        genres = models.ManyToManyField('Genre', related_name='albums')
        length = models.DurationField()
        number_of_songs = models.IntegerField()
        cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
        slug = models.SlugField(unique=True)

        def __str__(self):
            return f"'{self.title}' by {self.artist}"


class Song(models.Model):
        album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', null=True, blank=True)
        title = models.CharField(max_length=100)
        description = models.TextField(blank=True, null=True)
        duration = models.DurationField()
        artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
        track_number = models.PositiveIntegerField(help_text="Track`s placement in the album", null=True, blank=True)
        slug = models.SlugField(unique=True)

        class Meta:
                ordering = ['track_number']
                constraints = [
                        models.UniqueConstraint(fields=['album', 'track_number'], name='unique_track_per_album')
                ]

        def __str__(self):
                return f"'{self.title}' by {self.artist}" + f" (from '{self.album.title})'" if self.album else f" (Single)"


class Genre(models.Model):
        name = models.CharField(max_length=50, unique=True)
        description = models.TextField(blank=True, null=True)
        slug = models.SlugField(unique=True)

        def __str__(self):
                return f'{self.name}'


class Review(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
        album = models.ForeignKey(
                'Album',
                on_delete=models.CASCADE,
                related_name='reviews'
        )
        rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
        comment = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
                constraints = [
                        models.UniqueConstraint(fields=['user', 'album'], name='unique_user_album_review')
                ]

        def __str__(self):
                return f"{self.user.username} review on {self.album}"


