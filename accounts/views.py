from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import login, authenticate
from django.contrib import messages

from accounts.forms import LoginForm, RegisterForm
from accounts.mixin import RequestFormAttachMixin
# Create your views here.


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password2')
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            messages.success(
                request,
                "Account Created Successfully. please login.")
            return redirect(reverse('login'))
        else:
            context = {'form': form}
            return render(request, 'accounts/register.html', context)


class LoginView(RequestFormAttachMixin, FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_url = next_ or next_post or None

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            is_safe_url = url_has_allowed_host_and_scheme(
                redirect_url, settings.ALLOWED_HOSTS)
            if is_safe_url:
                return redirect(redirect_url)
            else:
                return redirect(reverse('index'))
        return super().form_invalid(form)
