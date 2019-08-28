from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper

class RegisterForm(UserCreationForm):
    helper = FormHelper()
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        