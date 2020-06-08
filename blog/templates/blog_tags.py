from django import template
from ..models import Blog
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_lastweek_hot_data

register = template.Library()

@register.simple_tag
def get_blog_title(obj):
    blog_id = obj
    return Blog.objects.get(pk = blog_id).title

@register.simple_tag
def get_hot_data_lastweek():
    blog_content_type = ContentType.objects.get_for_model(Blog)
    return get_lastweek_hot_data(blog_content_type)

@register.simple_tag
def get_blog_number_in_month(obj):
    month = obj.month
    return Blog.objects.filter(created_time__month = month).count()

