from django.contrib import admin
from django.contrib import admin
from .models import *

admin.site.register(AboutMe)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = "pk", "menu_item", "urls", "icon"
    list_display_links = 'pk', 'menu_item'

    ordering = 'menu_item', 'pk'
    search_fields = 'menu_item', 'urls'
    fieldsets = [
        (None, {
            'fields': ('menu_item', 'urls'),
        }),
    ]
