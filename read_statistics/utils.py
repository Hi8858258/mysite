import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" %(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        #增加总阅读数
        readnum, created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        #计数+1
        readnum.read_num += 1
        readnum.save()

        #统计每天的阅读数
        date = timezone.now().date()
        readDetail,created = ReadDetail.objects.get_or_create(content_type = ct, object_id = obj.pk, date=date)
        readDetail.read_num +=1
        readDetail.save() 


    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()    #timezone.now()包含日期和时间，用date（）则只会显示日期
    read_nums = []
    dates = []
    for  i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime("%m-%d"))
        read_details = ReadDetail.objects.filter(content_type=content_type,date = date) #先通过ReadDetail 获取到相应的查询集
        result = read_details.aggregate(read_num_sum = Sum('read_num')) #aggregate返回的是字典结果，跟annotate在后面增加一个标注不一样
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums,dates

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date = today)
    return read_details.order_by('-read_num')[:7]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today-datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type,date = yesterday)
    return read_details.order_by('-read_num')[:7]

def get_lastweek_hot_data(content_type):
    today = timezone.now().date()
    lastweek = today-datetime.timedelta(days=7)
    read_details = ReadDetail.objects.filter \
                                         (content_type=content_type,date__lt=today,date__gte=lastweek) \
                                         .values('content_type','object_id') \
                                         .annotate(read_num_sum=Sum('read_num'))
    return read_details.order_by('-read_num_sum')[:7]