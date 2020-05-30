from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class Comment(models.Model):

    #要被评论的对象，如博客，图片等
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    
    #评论内容
    text = models.TextField()
    #评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    #评论者
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")#related_name可以在user反向查询comment的时候使用user.comments.all()替代user.comment_set.all()，通常用在通过一个模型中有两个外键的情况   

    #评论回复功能
    root = models.ForeignKey('self', null = True, on_delete=models.CASCADE,related_name="root_comment")   #这个可以把comment对象看作孩子评论，对应的根评论只有1条，所以是多孩子评论对一根评论
    parent = models.ForeignKey('self',null=True, on_delete=models.CASCADE,related_name="parent_comment")
    reply_to = models.ForeignKey(User,null = True, on_delete=models.CASCADE, related_name="replies")#评论回复给谁，如果是顶级评论，就没有user。

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
    