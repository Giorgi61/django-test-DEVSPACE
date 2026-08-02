from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from turnstile.fields import TurnstileField


class UserRegisterForm(forms.ModelForm):
    class Meta:

        model = get_user_model()

        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

        labels = {'username': 'Username',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Email',
                  'password': 'Password'}

        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control'})}

        help_texts = {'username': '', }

    def clean_email(self):

        model = get_user_model()

        email = self.cleaned_data['email']
        if model.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email

    def set_group(self):

        group = Group.objects.get(name='standard')
        self.instance.groups.add(group)

    def save(self, commit=True):

        instance = super().save(commit=False)

        password = self.cleaned_data['password']
        instance.set_password(password)

        original_save_m2m = self.save_m2m

        def custom_save_m2m():
            original_save_m2m()
            self.set_group()

        self.save_m2m = custom_save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), disabled=True,
                             label='Email')
    turnstile = TurnstileField()


    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}), }

        labels = {'first_name': 'First Name', 'last_name': 'Last Name'}



class DisconnectOauth2Form(forms.Form):
    code = forms.CharField(label='verification code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = get_user_model()

    def clean_code(self):
        code = self.cleaned_data['code']

        if code.isdigit() and len(code) == 6:
            return code
