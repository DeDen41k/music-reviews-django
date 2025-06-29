from django.contrib import admin
from .models import Album, Artist, Song, Review, Genre


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album_info', 'release_date')
    list_filter = ('title', 'release_date')
    prepopulated_fields = {'slug': ('title',)}

    def album_info(self, obj):
        return f"'{obj.title}' by {obj.artist}"

    album_info.short_description = "Album"


class SongAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Review)
admin.site.register(Genre, GenreAdmin)

