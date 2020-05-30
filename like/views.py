from django.shortcuts import render
from .models import LikeCount,LikeRecord
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

def errorResponse(code,message):
    data = {}
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


# Create your views here.
def successResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)



def like_change(request):
    #获取前端数据
    user = request.user
    if not user.is_authenticated:
        return errorResponse(400,'请先登入')

    try:
        content_type = request.GET.get('content_type')
        content_type = ContentType.objects.get(model = content_type)
        model_class = content_type.model_class()
        object_id = request.GET.get('object_id')
        model_obj = model_class.objects.get(pk = object_id)
    except ObjectDoesNotExist:
        return errorResponse(401,'对象不存在')
    #处理数据
    if request.GET.get('is_like') == 'true':
        #要点赞
        like_count,created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)

        if created: 
            #没有点赞过，要进行点赞
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return successResponse(like_count.liked_num)
        else:
            #已经点赞，不能点赞
            return errorResponse(402,'重复点赞')
    else:
        #取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            #有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            #对点赞总数减一
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return successResponse(like_count.liked_num)
            else:
                #数据有问题
                return errorResponse(404,'数据错误')
        else:
            #没有点赞过，不能取消
            return errorResponse(403,'未点赞过，不能取消')
