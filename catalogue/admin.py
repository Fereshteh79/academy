from django.contrib import admin
from django.contrib.admin import register
from .models import Category, Brand, Product, ProductType, ProductAttribute


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_type', 'upc', 'title', 'is_active', 'category', 'brand']
    list_display_links = ['title']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['upc', 'title', 'category__name', 'brand__name']
    actions = ['active_all']
    inlines = [ProductAttributeValueInline, ProductImageInline]

    def active_all(self, request, queryset):
        pass

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    inlines = [ProductAttributeInline]


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_type']


admin.site.register(Category)
admin.site.register(Brand)
# admin.site.register(Product)
# admin.site.register(ProductType)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
