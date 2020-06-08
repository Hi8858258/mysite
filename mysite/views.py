from django.shortcuts import render                             
from blog.models import Blog,BlogType
#from django.core.cache import cache
from django.db.models import Count
from django.core.paginator import Paginator

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
    context['blog_dates'] = Blog.objects.dates('created_time','month',order = "DESC")
    return context

def home(request):
    # read_nums,dates = get_seven_days_read_data(blog_content_type)

    # #获取缓存的数据
    # hot_data_lastweek = cache.get('hot_data_lastweek')
    # if hot_data_lastweek is None:
    #     hot_data_lastweek = get_yesterday_hot_data(blog_content_type)
    #     cache.set('hot_data_lastweek', hot_data_lastweek, 3600)
    # else:
    #     print('Use caches')

    # context ={}
    # context['read_nums'] = read_nums
    # context['dates'] =dates
    # context['hot_data_today'] = get_today_hot_data(blog_content_type)
    # context['hot_data_yesterday'] = get_yesterday_hot_data(blog_content_type)
    # return render(request,'home.html',context)
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_data(blog_all_list,request)
    context['title'] = '最新文章'
    return render(request,'blog/blog_newest.html',context)

def about(request):
    return render(request,'about.html')