from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class FilterForm(forms.Form):

    my_posts = forms.BooleanField(label='My posts', required=False)



class LoginForm(forms.Form):

    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

