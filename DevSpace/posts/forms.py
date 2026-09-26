from django import forms


class FilterForm(forms.Form):

    my_posts = forms.BooleanField(label='My posts', required=False)



class LoginForm(forms.Form):

    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

