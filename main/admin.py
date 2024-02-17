from django.contrib import admin
from django.contrib import admin
from .models import *

# admin.site.register(AboutMe)

@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "content", 'path_photo', "style_photo", "time_create", "time_update", "is_published"
    list_display_links = 'pk', 'title', 'content'

    ordering = 'pk', 'content', "time_create", "time_update"
    search_fields = 'pk', 'title', 'content',
    fieldsets = [
        (None, {
            'fields': ('title', 'content', 'path_photo', "style_photo"),
        }),
    ]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = "pk", "menu_item", "urls", "icon"
    list_display_links = 'pk', 'menu_item'

    ordering = 'pk', 'menu_item'
    search_fields = 'pk', 'menu_item', 'urls'
    fieldsets = [
        (None, {
            'fields': ('menu_item', 'urls'),
        }),
    ]


@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):
    list_display = "pk", "sub_menu_items", "urls"
    list_display_links = 'pk', 'sub_menu_items'

    ordering = 'pk', 'sub_menu_items'
    search_fields = 'sub_menu_items', 'urls'
    fieldsets = [
        (None, {
            'fields': ('sub_menu_items', 'urls'),
        }),
    ]


@admin.register(LogInReg)
class LogInRegAdmin(admin.ModelAdmin):
    list_display = "pk", "menu_item", "urls"
    list_display_links = 'pk', 'menu_item'

    ordering = 'pk', 'menu_item'
    search_fields = 'menu_item', 'urls'
    fieldsets = [
        (None, {
            'fields': ('menu_item', 'urls'),
        }),
    ]
