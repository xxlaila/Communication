# -*- coding: utf-8 -*-
"""
@File    : register.py
@Time    : 2021/9/7 7:57 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.http import HttpResponse,JsonResponse
from django.views import View
from utils.hashcode import hash_code
import json
from ..forms.register import RegisterForm
from django.shortcuts import (
    render, redirect
)
from utils.email_send import send_register_email
from ..models.users import *

class RegisterView(View):
    def get(self, request, ):
        register_form = RegisterForm()
        return render(request, 'users/register.html',  {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            realname = register_form.cleaned_data['realname']
            sex = register_form.cleaned_data['sex']
            email = register_form.cleaned_data['email']
            mobile = register_form.cleaned_data['mobile']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:
                msg = "两次输入的密码不同！"
                return render(request, 'users/register.html', {'message': msg})
            same_user = Users.objects.filter(username=username)
            if same_user:
                msg = '用户已经存在，请重新输入用户名！'
                return render(request, 'users/register.html', {'message': msg})
            same_mobile_user = Users.objects.filter(mobile=mobile)
            if same_mobile_user:
                msg = '该电话号码已被注册，请换一个号码！'
                return render(request, 'users/register.html', {'message': msg})
            same_email_user = Users.objects.filter(email=email)
            if same_email_user:
                msg = '该邮箱地址已被注册，请使用别的邮箱！'
                return render(request, 'users/register.html', {'message': msg})

            new_user = Users.objects.create()
            new_user.username = username
            new_user.realname = realname
            new_user.sex = sex
            new_user.email = email
            new_user.mobile = mobile
            new_user.password = hash_code(password1)
            new_user.is_active = False
            new_user.save()
            status = send_register_email(email, "register")
            if status == 1:
                return redirect('users:login')
            else:
                return render(request, 'users/register.html', {'message': "发送邮件失败!"})

        return render(request, 'users/register.html', {'register_form': register_form})
