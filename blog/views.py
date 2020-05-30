from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import Blog,BlogType#,ReadNum
from django.db.models import Count
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from read_statistics.utils import read_statistics_once_read

# Create your views here.

blog_number_per_page = 10

def get_blog_list_common_data(blogs_all_list,request):
    paginator = Paginator(blogs_all_list,blog_number_per_page)
    page_num = request.GET.get('page',1)    #获取页码参数，默认值设为1。 这个参数是通过url/？page=1 的get方式传递的，和下方的pk不一样
    page_of_blogs = paginator.get_page(page_num)     #这个方法可以去识别传递的参数是否为数字的字符串，如果不是会默认当作 1来处理
    page_range = [i for i in range(int(page_num)-2,int(page_num)+3) if i>0 and i<= paginator.num_pages]
    
    #获取特定分类的博客数量(这种方法会损耗服务器性能，在数据特别多的时候不能用，应该使用annotate注释功能)
    # blog_types = BlogType.objects.all()
    # for blog_type in blog_types:
    #     blog_type.blog_type_count = Blog.objects.filter(blog_type = blog_type).count()    #blog_type是实例化的对象，所以可以直接把分类数量作为属性传给它

    context = {} 
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs          #页码浏览器
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog'))    #这里有个问题，前端直接使用blog_type.blog_count，是因为实例属性会找父类的属性
    context['blog_dates'] = Blog.objects.dates('created_time','day',order = "DESC")
    return context



def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_data(blog_all_list,request)
    return render(request,'blog/blog_list.html',context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog,pk = blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)

    context = {}
    previous_blog = Blog.objects.filter(pk__lt = blog_pk ).last()
    next_blog = Blog.objects.filter(pk__gt = blog_pk).first()
    context['blog'] = blog
    context['previous_blog'] = previous_blog
    context['next_blog'] =next_blog
    context['user'] = request.user    #获取用户信息
    response = render(request, 'blog/blog_detail.html',context)   #相应
    response.set_cookie(read_cookie_key,'true',max_age=60)    #max_age,expires取一个用
    return response

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk = blog_type_pk)
    blog_all_list_with_type = Blog.objects.filter(blog_type = blog_type)
    context = get_blog_list_common_data(blog_all_list_with_type,request)
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blog_all_list_with_date = Blog.objects.filter(created_time__year = year,created_time__month = month)
    context = get_blog_list_common_data(blog_all_list_with_date,request)
    context['blogs_with_date'] = '%s年%s月' %(year,month)
    context['blog_dates'] = Blog.objects.dates('created_time','day',order = "DESC")
    return render(request,'blog/blogs_with_date.html',context)  
