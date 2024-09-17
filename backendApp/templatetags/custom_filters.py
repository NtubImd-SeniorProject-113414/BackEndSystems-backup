from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_groups')
def has_groups(user, group_names):
    if not user.is_authenticated:
        return False
    groups = user.groups.values_list('name', flat=True)
    return any(group in groups for group in group_names)

@register.filter
def to_range(start, end):
    return range(start, end)

@register.filter
def emotion_color(score):
    if score >= 4:
        return 'success'  # 綠色
    elif score >= 2:
        return 'warning'  # 橙色
    return 'danger'  # 紅色