from django.shortcuts import render
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def reg(request, us, psw, tkn):
    if str(tkn) == "AsB3dC022dFdGeH45jauwjHFR5s98ejxHDdeujhjsjEEJeje6ejdu58662D":
        if not User.objects.filter(username=us).exists():
            us = User.objects.create_user(password=psw, username=us)
            return HttpResponse("1")
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("2")
    

def login(request, us, psw):
    user = authenticate(request, username=us, password=psw)
    if user is not None:
        return HttpResponse("1")
    else:
        return HttpResponse("0")

@csrf_exempt
def del_acc(request, us, psw):
    try: 
        if request.method == "DELETE":
            if request.GET.get('tkn') == "JDR55EECncd88Ddd":
                try:
                    user = authenticate(request, username=us, password=psw)
                    if user is not None:
                        user.delete()
                        return HttpResponse("1")
                    else:
                        return HttpResponse("ERROR")
                    
                except:
                    return HttpResponse("ERROR")
            else:
                return HttpResponse("ERROR")
        else:
            return HttpResponse("ERROR")
    except:
        return HttpResponse("ERROR")