from django.contrib import admin

# Register your models here.
from django.contrib import admin
from  .models import LikeCount,LikeRecord

# Register your models here.
@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('content_object','liked_num')

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('content_object','user','liked_time')

