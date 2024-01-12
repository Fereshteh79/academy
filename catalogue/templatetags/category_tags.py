from django import template

from .models import Category

register = template.library()


@register.simple_tag
def get_category():
    return Category.objects.all()
