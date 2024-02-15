from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import AboutMe #, Menu, SubMenu


class MainPage(ListView):
    model = AboutMe
    context_object_name = ''
    template_name='main/main.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой сайт визитка'

        return context
