from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from app.models import Calendar, User
from app.serializers import CalendarSerializer

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

def index(request):
    return render_to_response('index.html',locals())
class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer




def login(request):

    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/index/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render_to_response('login.html')

def register(request):
    
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        context = {
            "name": request.POST['name'],
            "password": request.POST['password']
        }
        new_user = User.objects.create()
        new_user.name = request.POST['name']
        new_user.password = request.POST['password']
        new_user.save()
        return render(request, 'register.html', context)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
