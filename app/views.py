from rest_framework import viewsets
from app.models import Event
from app.serializers import CalendarSerializer

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.views.decorators.http import require_POST
from django.contrib import messages


def index(request):
    '''
    Index view
    '''
    messages.add_message(request, messages.INFO, 'Hello world.')
    return render(request, 'index.html', locals())

@require_POST
def invite(request):
    '''
    Handle sending invitation
    user -> target_user
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    
    target_user = request.POST.get('invite_user', '')
    
    if target_user == '':
        messages.add_message(request, messages.WARNING, 'no invite target')
        return HttpResponseRedirect(reverse_lazy('index'))

    try:
        target_user_instance = User.objects.get(username=target_user)
        messages.add_message(request, messages.INFO, 'Invitation was sent')
    except:
        messages.add_message(request, messages.WARNING, 'target user not exists!')
        return HttpResponseRedirect(reverse_lazy('index'))
    
    # TODO: Send grouping invitation to target user
    # TODO: Add multiple invite target at once
    return HttpResponseRedirect(reverse_lazy('index'))

def calendar(request):
    '''
    Show users calendars
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    print(request.user.username, request.user.id)
    # TODO: read data from db and render

    # Fake data
    import time
    events = [
        { 'title': 'group meeting', 'starttime': time.asctime(time.localtime()), 'duration': 20 },
        { 'title': 'ML class', 'starttime': time.asctime(time.localtime(time.time() + 1000000)), 'duration': 300 }
    ]
    return render(request, 'calendar.html', locals())

@require_POST
def add_event(request):
    '''
    Add new event
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    
    # TODO: extract all the data from POST with clean()

    messages.add_message(request, messages.INFO, 'Add new event')
    
    # TODO: Add the event to DB
    return HttpResponseRedirect(reverse_lazy('calendar'))

@require_POST
def update_event(request):
    '''
    Update an event
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')

    # TODO: MUST check the event is belongs to the user
    return HttpResponseRedirect(reverse_lazy('calendar'))

@require_POST
def del_event(request):
    '''
    Del new event
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    # TODO: MUST check the event is belongs to the user
    return HttpResponseRedirect(reverse_lazy('calendar'))

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = CalendarSerializer

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
