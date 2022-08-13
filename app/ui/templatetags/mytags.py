from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, date
from django.conf import settings
import re
from django import template

numeric_test = re.compile("^\d+$")
register = template.Library()




@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural

@register.filter
def get_value(obj, k):
    return getattr(obj, k)

@register.filter
def fillbox(text, length):
    if text is None:
        text  = ""
    return mark_safe("<span class='blank-fill char%s'>%s</span>" % (length, text))

@register.filter
def fillarea(text):
    if text is None:
        text  = ""
    return mark_safe("<div class='blank-fill char100p text-left'>%s</div>" % ( text))

@register.filter
def age_cal(d):
    today = date.today()
    if d:
        return today.year - d.year - ((today.month, today.day) < (d.month, d.day))
    else:
        return 0

@register.filter
def checkbox(i, j):
    if i == j:
        return mark_safe("<i class='fas  fa-xs fa-check-square'></i>")
    else:
        return mark_safe("<i class='far fa-xs fa-square'></i>")

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def mrange(val,minm=5):
    return range(minm)

@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

@register.simple_tag
def getform(form, arg):
    """Gets an attribute of an object dynamically from a string name"""
    return form.fields[arg]
