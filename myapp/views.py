import datetime
import uuid
import redis
from django.conf import settings
from django.shortcuts import render, render_to_response
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect,response
from jedi.evaluate.context import iterable
from myapp.models import Message,Comment
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
session={}
conn=redis.Redis()

def exit(request):
    logout(request)
    return render_to_response("login.html")

def articleview(request):
    #resp =  HttpResponse("hello")
    # resp.set_cookie("secret", "xxklgjaljgilatjgalgj
    if "sessionid" not in request.COOKIES:
        return HttpResponseRedirect('/myapp/login/')

    elif  conn.get(request.COOKIES['sessionid'])!=None  :
        #print(session[request.COOKIES['sessionid']])
        find = conn.get(request.COOKIES['sessionid'])
        s = User.objects.get(id=find)
        x = Message.objects.filter(userid=find)
        if request.method=='POST':
            title1=request.POST['title']
            msg1=request.POST['context']
            add=Message(msg=msg1,title=title1,userid_id=find)
            add.save()
        return render_to_response('article.html',context={"article":x,"user":s})
    else:
        return HttpResponseRedirect('/myapp/login/')

def findcookie(request):
    if conn.get(request.COOKIES['sessionid'])!=None:
        find = conn.get(request.COOKIES['sessionid'])
        return User.objects.get(id=find)
    else :
        return  None
def person(request):
    x=findcookie(request)
    if x==None:
        return HttpResponse(status=404)
    else :
        return HttpResponse(content="该用户id为{}".format(x.id),status=200)

def articlepageview(request,id):

    x=Message.objects.get(id=id)
    c=Comment.objects.filter(MessageId=id)
    #print(c[0].MessageId_id)
    return render_to_response('article_detail.html',context={"articlepage":x,"comments":c})

def articledelete(request,id):
    x=Message.objects.get(id=id)
    x.delete()
    return HttpResponseRedirect('/myapp/article')
def commentview(request,id):
    x=request.POST['comment']
    s=Comment(message=x,MessageId_id=id)
    s.save()
    return HttpResponseRedirect('/myapp/article/%s'% id)

def commentpageview(request,id,bid):
    # x=findcookie(request)
    x=Comment.objects.get(MessageId=id,id=bid)
    #print(x)
    x.delete()
    return HttpResponseRedirect('/myapp/article/%s'%id)


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.get(username=username,password=password)
    except User.DoesNotExist as e:
        return HttpResponse(content = "用户名或密码错误")
    x = HttpResponseRedirect('/myapp/article/')
    s = uuid.uuid4().hex
    x.set_cookie("sessionid", s)
    conn.set(s, user.id, 600)
    return x

def signupindex(request):
    return render_to_response("signup.html")

def signup(request):
    username = request.POST['name']
    password = request.POST['password']
    try :
        User.objects.get(username=username)
        return HttpResponse(content="该用户已存在")
    except User.DoesNotExist:
        new = User(username=username,password=password)
        new.save()
        return HttpResponseRedirect('/myapp/article/')

# def set_cookie(key,value,days_expire=7):
#     if days_expire is None:
#         max_age = 365 * 24 * 60 * 60  # one year
#     else:
#         max_age = days_expire * 24 * 60 * 60
#     expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT")
#     response = HttpResponse("222")
#     response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,secure=settings.SESSION_COOKIE_SECURE or None)
#     session[key] = value
#     return  response
def loginview(request):
    return render_to_response("login.html")
