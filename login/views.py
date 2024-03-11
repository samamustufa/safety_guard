from django.shortcuts import render
from login.models import Login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def loginPage(request):
    try:
        return render(request,'login.html' )
    except Exception as e:
        pass

def loginaction(request):
    
    try:
        if request.method == "POST":
            login_username = request.POST.get('user_name')
            login_password = request.POST.get('password')

            loginData = Login.objects.all()

            for i in loginData:
                if i.user_name == login_username and i.password ==login_password:
                    return render(request, 'welcome.html')
                else:
                    return render(request, "error.html")


    except:
        print("An exception occurred")

    return render(request, "login.html")

@login_required(login_url='/')
def Welcomepage(request):
    try:
        return render(request,'welcome.html' )
    except Exception as e:
        pass


# def Welcomepage(request):
    
#     try:
#         print("Inside TRY")
#         print(request.method )
#         if request.method == "GET":
#             print("Inside IFF")
#             login_username = request.POST.get('user_name')
#             login_password = request.POST.get('password')

#             loginData = Login.objects.all()

#             for i in loginData:
#                 if i.user_name == login_username and i.password ==login_password:
#                     return render(request, 'welcome.html')
#                 else:
#                     return render(request, "error.html")


#     except:
#         print("An exception occurred")
#     return HttpResponse("hello")