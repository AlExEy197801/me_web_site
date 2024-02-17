from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import AboutMe, Menu, LogInReg #, SubMenu


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
