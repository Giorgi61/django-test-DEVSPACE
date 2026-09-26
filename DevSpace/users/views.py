from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from django.views.generic.edit import CreateView, UpdateView

from mail_verifications.EmailSender import EmailSender
from mail_verifications.VerificationService import VerificationService

from .forms import DisconnectOauth2Form, ProfileForm, UserRegisterForm

# Create your views here.


class UserLogin(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login_register.html"
    success_url = reverse_lazy('posts:all_posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['input_value'] = 'Login'

        return context


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/login_register.html'
    success_url = reverse_lazy('posts:all_posts')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_social = self.request.GET.get('social_register') == 'true'

        context['is_social'] = is_social
        context['input_value'] = 'Register'
        return context


class UerProfileView(UpdateView):
    pk_url_kwarg = 'pk'
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('posts:all_posts')
    extra_context = {'title': 'Profile'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['social_auths'] = context['object'].social_auth.all()
        return context

    def form_invalid(self, form):
        print(form.errors.as_data())
        return super().form_invalid(form)

class UserPasswordChange(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Password Change'}


class UserPasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Password Change Done'}


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    # html_email_template_name = 'users/password_reset_email.html'
    email_template_name = 'users/password_reset_email.txt'
    success_url = reverse_lazy('users:password_reset_done')
    extra_context = {'title': 'Password Reset'}


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': 'Password Reset Done'}


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')


@require_POST
@login_required
def remove_oauth2_view(request):

    provider = request.POST.get('provider')
    user = request.user

    if user.social_auth.filter(provider=provider).exists():
        code = VerificationService(user).register_verification()

        email = user.email

        EmailSender.send_verification_code(email, code)

        return redirect('users:disconnect_oauth2_confirm', provider=provider)

    raise Http404

class DisconnectOauth2View(LoginRequiredMixin, FormView):
    template_name = 'users/disconnect_oauth2_verification.html'
    form_class = DisconnectOauth2Form
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        code = form.cleaned_data['code']

        user = self.request.user
        verificator = VerificationService(user)

        if verificator.verify_verification_code(code) is not None:
            provider = self.kwargs['provider']

            social = user.social_auth.filter(provider=provider).first()

            if social:
                social.delete()

            return super().form_valid(form)

        else:
            form.add_error('code', 'Invalid code')
            return self.form_invalid(form)

