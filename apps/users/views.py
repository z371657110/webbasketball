from django.shortcuts import render
# from django.shortcuts import render_to_response
import json, os, time
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import apps.users.logics as Logics
from datetime import datetime
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login,authenticate
# Create your views here.
def register(request):
    print("register")
    if request.method == 'POST':
        user = Logics.register(request.POST)
    if user:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        auth_login(request,user)
        return render(request, "auth/login.html")
    return HttpResponseRedirect('/auth/login.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        pws = request.POST['password']
        user = authenticate(username=username, password=pws)
        if user :
            auth_login(request,user)
            return render(request, "auth/login.html")
        else:
            return HttpResponseRedirect('/auth/login')

@login_required
def editUserInfo(request):
    response_data = {}
    if request.method == "POST":
        username = request.user.username
        result = Logics.editUserInfo(username,request.POST)
    if result:
        response_data['success'] = 1
        response_data['message'] = '修改成功'
    else:
        response_data['success'] = 0
        response_data['message'] = '修改失败'
    return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def changePwd(request):
    response_data = {}
    response_data['success'] = 0
    response_data['message'] = '修改失败'
    if request.method == "POST":
        username = request.user.username
        oldPwd = request.POST['oldPwd']
        user = authenticate(username=username,password=oldPwd)
        if user is not None and user.is_active:
            newPwd = request.POST['newPwd']
            result = Logics.cheangePwd(user,newPwd)
            if result:
                response_data['success'] = 1
                response_data['message'] = '修改成功'
    return HttpResponse(json.dumps(response_data),content_type='application/json')

@login_required
def  logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/auth/login')

# 用户头像更改view
@login_required
def updateImage(request):
    response_data = {}
    if request.method == 'POST':
        upfile = request.FILES['file']
        username = request.user.username
        extention =  upfile.name[upfile.name.rfind('.'):]
        fileName = str(int(time.time() * 10)) + extention
        with open(settings.UPLOADED_DIR + '/' + fileName, 'wb+') as dest:
            for chunk in upfile.chunks():
                dest.write(chunk)
        result = Logics.updateImage(username,fileName)
        if not result:
            response_data['success'] = 0
            response_data['message'] = '保存失败'
        else: 
            response_data['success'] = 1
            response_data['message'] = '保存成功'
            response_data['fileInfo']={
                                                    "filename":upfile.name,
                                                    "url":"/static/upload/" + fileName,
                                                    "uname":fileName
                                                        };
    return HttpResponse(json.dumps(response_data), content_type='application/json')
