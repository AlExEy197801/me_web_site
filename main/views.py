from django.contrib.auth import logout, login, get_user_model
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.views import LoginView

from .models import AboutMe, Menu, LogInReg #, SubMenu
from .forms import *
from .token import account_activation_token

from requests import request

import json


class MainPage(ListView):
    model_about_me = AboutMe
    model_menu = Menu
    model_log_reg_menu = LogInReg
    context_object_name = ''
    template_name='main/main.html'

    def get_queryset(self):
        return Menu.objects.prefetch_related('tags').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        menu = list(Menu.objects.prefetch_related('tags').all())
        log_reg_menu = list(LogInReg.objects.all())
        posts = list(AboutMe.objects.all())

        context['title'] = 'Мой сайт визитка'
        context['head_1'] = 'main/head-1.html'
        context['menu'] = menu
        context['log'] = log_reg_menu
        context['posts'] = posts

        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = 'main/login.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['head_1'] = 'main/head-1.html'
        context['menu'] = list(Menu.objects.prefetch_related('tags').all())
        # context['submenu'] = list(SubMenu.objects.all())
        return context

    def form_valid(self, form):
        """
        автоматом идёт на главную страницу
        """
        to_email = form.cleaned_data.get('email')
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('main/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        # to_email = form.cleaned_data.get('email')

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        print('to_email', to_email)
        print('current_site.domain', current_site.domain)
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Вход'
        context['head_1'] = 'main/head-1.html'
        return context

def logout_user(request):
    logout(request)
    return redirect('home')
