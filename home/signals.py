from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import AudioFile, UploadedVideo, Scenario

@receiver(user_logged_in)
def associate_records_with_user(sender, request, user, **kwargs):
    temp_id = request.COOKIES.get('temp_id')
    if temp_id:
        
        AudioFile.objects.filter(temp_id=temp_id, user__isnull=True).update(user=user, temp_id=None)
        UploadedVideo.objects.filter(temp_id=temp_id, user__isnull=True).update(user=user, temp_id=None)
        Scenario.objects.filter(temp_id=temp_id, user__isnull=True).update(user=user, temp_id=None)
        