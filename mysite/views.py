from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, \
                                  get_today_hot_data,get_yesterday_hot_data, \
                                  get_lastweek_hot_data
from blog.models import Blog
from django.core.cache import cache

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums,dates = get_seven_days_read_data(blog_content_type)

    #获取缓存的数据
    hot_data_lastweek = cache.get('hot_data_lastweek')
    if hot_data_lastweek is None:
        hot_data_lastweek = get_yesterday_hot_data(blog_content_type)
        cache.set('hot_data_lastweek', hot_data_lastweek, 3600)
    else:
        print('Use caches')

    context ={}
    context['read_nums'] = read_nums
    context['dates'] =dates
    context['hot_data_today'] = get_today_hot_data(blog_content_type)
    context['hot_data_yesterday'] = get_yesterday_hot_data(blog_content_type)
    context['hot_data_lastweek'] = get_lastweek_hot_data(blog_content_type)
    return render(request,'home.html',context)