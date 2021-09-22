from django.contrib import admin
from . import models
from .models import TreeBlank, Blank, Menu, MostPlanted, RegionStatistics, ContactForm


@admin.register(TreeBlank)
class TreeBlankAdmin(admin.ModelAdmin):
    list_display = ['tree', 'blank', 'amount']
    list_filter = ['tree']


@admin.register(Blank)
class BlankAdmin(admin.ModelAdmin):
    list_display = ['region', 'district', 'mahalla', 'payment_type']
    list_filter = ['region', 'payment_type']
    search_fields = ['district', 'mahalla', 'social_media_url']


@admin.register(MostPlanted)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'username', 'tree_amount']
    list_filter = ['type']
    search_fields = ['name', 'username', 'account_link']


@admin.register(RegionStatistics)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['region', 'donated_trees', 'donated_people', 'planted_trees', 'on_plan_planting']


@admin.register(ContactForm)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'phone', 'email', 'text']


admin.site.register(models.LeganEntity)
admin.site.register(models.TreeType)
admin.site.register(models.Tree)
admin.site.register(models.Index)
admin.site.register(models.StaticPage)
admin.site.register(models.Footer)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'footer', 'header']
    list_filter = ['footer', 'header']
