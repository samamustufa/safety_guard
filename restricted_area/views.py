from django.shortcuts import render

def restrictArea(request):
    try:
        return render(request,'restricted_page.html' )
    except Exception as e:
        pass