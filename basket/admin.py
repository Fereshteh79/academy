from django.contrib import admin
from .models import Basket, BasketLine


class BasketLineInline(admin.TabularInline):
    model = BasketLine


class BasketAdmin(admin.ModelAdmin):
    list_filter = ['user', 'created_time']
    inlines = (BasketLineInline,)


admin.site.register(Basket, BasketAdmin)
