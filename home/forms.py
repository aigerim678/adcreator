from django import forms
from .models import AudioFile
from .models import UploadedVideo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['file']


class VideoFileForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ['video']  


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Обязательное поле. Введите корректный адрес электронной почты.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user