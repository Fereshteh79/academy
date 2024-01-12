from django.contrib import admin
from django.contrib.admin import register
from .models import PartnerStock


@register(PartnerStock)
class PartnerStockAdmin(admin.ModelAdmin):
    pass


@register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass
