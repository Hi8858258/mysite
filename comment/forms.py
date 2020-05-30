from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment

class CommentForm(forms.Form):
    #content_type 和object_id 是从 blog   view.py里面获取到的
    content_type = forms.CharField(widget=forms.HiddenInput)   
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget = CKEditorWidget(config_name='comment_ckeditor'),error_messages={'required':'评论内容不得为空'})
    reply_comment_id = forms.IntegerField(widget = forms.HiddenInput(attrs={'id':'reply_comment_id'}))
    
    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            #用init取实例化类的时候，如果要初始化父类（即使用super）的话，新传入的参数（user）需要从参数列表中再取出来，不然不能调用父类的方法会报错
            self.user = kwargs.pop('user')
        super(CommentForm,self).__init__(*args,**kwargs)

    def clean(self):
        #验证部分
        # ----1-----判断用户是否登入
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')

        #-----2-----评论对象验证，如果评论的时候，正好删除了博客，就无法评论了
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model= content_type).model_class()
            model_obj = model_class.objects.get(pk = object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id<0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk = reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id