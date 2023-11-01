from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'name','username', 'email', 'bio']