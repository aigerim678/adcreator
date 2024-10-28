from django.db import models
from django.contrib.auth.models import User

class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    temp_id = models.CharField(max_length=36, null=True, blank=True) 

    def __str__(self):
        return f"Audio File {self.id}"


from django.db import models

class UploadedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.FileField(upload_to='videos/')  
    uploaded_at = models.DateTimeField(auto_now_add=True) 
    temp_id = models.CharField(max_length=36, null=True, blank=True)  

    def __str__(self):
        return f"Video File {self.id}"



from django.db import models

class Scenario(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    temp_id = models.CharField(max_length=36, null=True, blank=True) 

    def __str__(self):
        return self.text[:50] 