from django.db import models
from django.urls import reverse


class AboutMe(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    style_photo = models.CharField(max_length=255)
    path_photo = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_publushed = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'text': self.pk})

    class Meta:
        verbose_name = 'Обо мне'
        verbose_name_plural = 'Обо мне'
        ordering = ['time_create']


class Menu(models.Model):
    menu_item = models.CharField(max_length=255)
    urls = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class SubMenu(models.Model):
    sub_menu_items = models.CharField(max_length=255)
    urls = models.CharField(max_length=255)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='tags')
    
    class Meta:
        verbose_name = 'Подменю'
        verbose_name_plural = 'Подменю'
