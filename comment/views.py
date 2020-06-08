from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
# Create your views here.

def update_comment(request):
    comment_form = CommentForm(request.POST, user = request.user)
    print(request.POST)
    data = {}
    if comment_form.is_valid():
        #检查通过，添加评论
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text =comment_form.cleaned_data['text']
        comment.content_object= comment_form.cleaned_data['content_object']
        
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()
        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)