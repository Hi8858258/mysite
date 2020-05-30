from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import auth
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User


# Create your views here.

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))#问题：这里面有问题需要再改

    else:#通过非post方式进入登陆页面
        login_form = LoginForm()

    context ={}
    context['login_form'] = login_form
    return render(request,'user/login.html',context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username,email,password)
            #登入用户
            user = auth.authenticate(username= username,password = password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:#通过非post方式进入登陆页面
        reg_form = RegForm()

    context ={}
    context['reg_form'] = reg_form
    return render(request,'user/register.html',context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from',reverse('home')))

def user_info(request):
    return render(request,'user/user_info.html')