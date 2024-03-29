from django import template
# from django.contrib.auth.models import Permission

register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() or user.groups.filter(name='مدیر').exists()