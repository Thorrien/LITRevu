from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(max_length=70, label="Nom d'utilisateur")
    password = forms.CharField(max_length=70, widget=forms.PasswordInput, label='Mot de passe')


class SingupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username',]
