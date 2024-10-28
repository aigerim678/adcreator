from django.contrib import admin
from .models import AudioFile, UploadedVideo, Scenario

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','uploaded_at', 'temp_id')
    search_fields = ('user__username', 'session_key')

@admin.register(UploadedVideo)
class UploadedVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','uploaded_at', 'temp_id')
    search_fields = ('user__username', 'session_key')

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'temp_id')
    search_fields = ('user__username', 'session_key', 'text')
