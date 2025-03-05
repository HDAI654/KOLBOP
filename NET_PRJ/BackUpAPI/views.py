from django.shortcuts import render
from rest_framework import generics
from .models import BU_model
from .serialize import BU_ModelSerializer
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
import base64
from . import forms
from django.contrib.auth import authenticate, login, logout
import sqlite3
import os

class MyModelList(generics.ListCreateAPIView):
    queryset = BU_model.objects.all()
    serializer_class = BU_ModelSerializer

@csrf_exempt 
def return_uploaded_files(request, tkn, user):
    if tkn == "AkkOk0d5seeS5S29eDe25ddDEc":
        files = BU_model.objects.filter(user=user)
        file_data = {}
        for file in files:
            with open(file.file.path, "rb") as fb:
                f = base64.b64encode(fb.read()).decode('utf-8')
                file_data[file.file.name] = f
        return JsonResponse(file_data, safe=False)
    else:
        return JsonResponse([], safe=False)

@csrf_exempt 
def return_uploaded_files_names(request, tkn, user):
    if tkn == "AkkOk0d5seeS5S29eDe25ddDEc":
        files = BU_model.objects.filter(user=user)
        return JsonResponse([file.file.name for file in files], safe=False)
    else:
        return JsonResponse([], safe=False)
   
@csrf_exempt   
def delete_all_files(request, tkn, user):
    if request.method == "DELETE":
        if tkn == "K5DKdid45doNDOJM5885sD5dojdOIJDddojm5":
            try:
                files_to_delete = BU_model.objects.filter(user=user)

                for file_obj in files_to_delete:
                    file_path = file_obj.file.path
                    if os.path.exists(file_path):
                        os.remove(file_path)

                files_to_delete.delete()
                return HttpResponse("DELETED")
            except:
                return HttpResponse("ERROR")
        else:
            return HttpResponse("ERROR")
    else:
        return HttpResponse("ERROR")

@csrf_exempt     
def delete_one_file(request):
    if request.method == "DELETE":
        if request.GET.get('tkn') == "G71fT9oqLp2BZx80h":
            try:
                record = BU_model.objects.get(file=request.GET.get('name')) 
                os.remove(record.file.path)
                record.delete()
                
                return HttpResponse("DELETED")
            except:
                return HttpResponse("ERROR")
        else:
            return HttpResponse("ERROR")
    else:
        return HttpResponse("ERROR")

def show_saved(request):
    if request.user.is_authenticated:  
        files =  BU_model.objects.filter(user=request.user)
        fls = []
        for i in files:
            if str(os.path.splitext(i.file.name)[1]) == ".db":
                if os.path.exists(str(i.file.path)):
                    
                    # tables
                    conn = sqlite3.connect(str(i.file.path))
                    cur = conn.cursor()
                    tables = [tbl[0] for tbl in list(cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())]
                    
                    tables_html = []
                    
                    # tables data
                    for tbl in tables :
                        html = """<h2 class='text-light'>{tbl_name}</h2></br><table class='table bg-transparent shadow-sm rounded table-hover text-light'>{_tbl_}</table>"""
                        
                        
                        heads = "<thead><tr>{heads}</tr></thead>".format(heads=''.join([str("<th>" + hd + "</th>") for hd in  [h[0] for h in cur.execute(f"SELECT * FROM {tbl}").description]]))
                        
                        rows = []
                        for row in list(cur.execute(f"SELECT * FROM {tbl}").fetchall()):
                            a = "<tr>{tds}</tr>"
                            tds = []
                            for td in row:
                                tds.append(f"<td>{td}</td>")
                            rows.append(a.format(tds=''.join(tds)))
                            
                        rows = "<tbody>{body}</tbody>".format(body=''.join(rows))
                        
                        html = html.format(_tbl_=heads+''+rows, tbl_name=str(tbl))
                        
                        tables_html.append(html)
                    
                    # get now host address
                    host = request.get_host()
                    # make download link for file
                    download_link = f"http://{host}/media/{i.file.name}"
                    fls.append((i.file.name, f"<a class='text-primary border border-primary p-2' href='{download_link}' download> download {i.file.name}</a> </br></br>"+'</br></br></br>'.join(tables_html)))
            
            elif str(os.path.splitext(i.file.name)[1]) in [".jpg", ".png", ".jpeg", ".ico"]:
                if os.path.exists(str(i.file.path)):
                    # get now host address
                    host = request.get_host()
                    # make download link for file
                    download_link = f"http://{host}/media/{i.file.name}"
                    img = f"<h2 class='text-light'>{i.file.name}</h2></br><a class='text-primary border border-primary p-2' href='{download_link}' download>download {i.file.name}</a></br></br><img class='rounded' alt='{i.file.name}' src='{download_link}' width=500></img></br>" 
                    fls.append((i.file.name, img))
            
            elif str(os.path.splitext(i.file.name)[1]) in ['.mp3', '.wav', '.ogg', '.aac', '.m4a']:
                if os.path.exists(str(i.file.path)):
                    # get now host address
                    host = request.get_host()
                    # make download link for file
                    download_link = f"http://{host}/media/{i.file.name}"
                    fls.append((i.file.name, f"<h2 class='text-light'>{i.file.name}</h2></br><a class='text-primary border border-primary p-2' href='{download_link}' download> download {i.file.name}</a></br></br><audio controls><source src='{download_link}' ></audio></br></br></br>"))
            
            elif str(os.path.splitext(i.file.name)[1]) in ['.mp4', '.mkv', '.avi', '.webm', '.mov', '.wmv', '.flv', '.3gp', '.m4v']:
                if os.path.exists(str(i.file.path)):
                    # get now host address
                    host = request.get_host()
                    # make download link for file
                    download_link = f"http://{host}/media/{i.file.name}"
                    fls.append((i.file.name, f"<h2 class='text-light'>{i.file.name}</h2></br><a class='text-primary border border-primary p-2' href='{download_link}' download> download {i.file.name}</a></br></br><video controls><source src='{download_link}'></video></br></br></br>"))
            
            
            else:
                # get now host address
                host = request.get_host()
                # make download link for file
                download_link = f"http://{host}/media/{i.file.name}"
                fls.append((i.file.name, f"<h2 class='text-light'>{i.file.name}</h2></br><a class='text-primary border border-primary p-2' href='{download_link}' download> download {i.file.name}</a>"))
        return render(request, 'show_saved.html', {"files":fls, "user":request.user})
    else:
        return HttpResponseRedirect("login")
    
def login_page(request):
    return render(request, 'login.html', context={"form":forms.flogin}) 
    
def check_login(request):
    form = forms.flogin(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            res = HttpResponseRedirect("panel")
            res.set_cookie('username', str(username))
            return res
        else:
            return HttpResponseRedirect("login")
    else:
        return HttpResponseRedirect("login")
    
def logout_func(request):
    logout(request)
    return HttpResponseRedirect("login") 
  
    
    