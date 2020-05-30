from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('user_info/',views.user_info,name='user_info'),
    path('login_for_modal/',views.login_for_modal,name='login_for_modal'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)