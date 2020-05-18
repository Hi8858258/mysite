from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('',views.blog_list,name = 'blog_list'),
    path('blog_detail/<int:blog_pk>/',views.blog_detail, name='blog_detail'),
    path('blogs_with_type/<int:blog_type_pk>/',views.blogs_with_type,name='blogs_with_type'),
    path('date/<int:year>/<int:month>/',views.blogs_with_date,name='blogs_with_date'),
] 