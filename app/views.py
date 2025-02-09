from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse( "<h1>Hola mundo</h1>")

def Error404(request, exception):
    return render( request, '404.html', status=404)

def Error500(request, exception):
    return render( request, '500.html', status=500)

def Error(request, exception):
    return 7/0

def onepage(request):
    return render( request, 'onepage.html', status=200)