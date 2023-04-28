from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, UpdateView
from django.core.cache import cache

from users.forms import CustomUserCreationForm, EmailChangeForm

from users.utils import send_email_for_verify, token_generator, get_user

User = get_user_model()


def register_view(request):
    """Представление с регистрацией пользователя"""

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            send_email_for_verify(request, user)
            login(request, user)
            return redirect('confirm_email')
    else:
        form = CustomUserCreationForm()
    return render(request, template_name='users/register.html', context={'form': form})


class SendVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        send_email_for_verify(request, user)
        return redirect('confirm_email')


class UserListLoginView(LoginView):
    template_name = 'users/login.html'


class UserListLogoutView(LogoutView):
    template_name = 'users/logout.html'


class UserList(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/main_page.html'


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'users/profile.html')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_edit.html'
    fields = ['full_name']
    success_url = 'profile'

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerifyView(View):

    def get(self, request, uidb64, token):
        user = get_user(uidb64)
        check_token = token_generator.check_token(user, token)

        if user is not None and check_token:
            user.verified = True
            user.save()
            login(request, user)
            return redirect('main_page')
        return redirect('invalid_verify')


class EmailChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = EmailChangeForm()
        return render(request, 'users/change_email.html', {'form': form})

    def post(self, request):
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            change_mail_cache_key = f'{request.user.pk} new email'
            cache.set(change_mail_cache_key, email, 60 * 60 * 24)
            send_email_for_verify(request, request.user, change_mail=True)
            return redirect('confirm_email')
        return render(request, 'users/change_email.html', {'form': form})


class EmailChange(View):
    def get(self, request, uidb64, token):
        user = get_user(uidb64)
        check_token = token_generator.check_token(user, token)
        change_mail_cache_key = f'{user.pk} new email'
        email = cache.get(change_mail_cache_key)
        if user is not None and check_token and email:
            user.email = email
            user.verified = False
            user.save()
            return redirect('main_page')
        return redirect('invalid_verify')
