from rest_framework import viewsets
from app.models import Event, Group
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
import json

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


def query_group(request):
    '''
    Used for AJAX
    Query for notification
    Including recieved group and accepted group
    '''
    res_data = {}
    if not request.user.is_authenticated:
        res_data = { 
            'ok': False,
            'message': 'You are no authenticated!',
        }
        return HttpResponse(json.dumps(res_data), content_type="application/json")

    # Query recieved group invitaions
    recieved_groups = Group.objects.all().filter(
        target_id=request.user.id)

    # Query accepted group invitaoins (start by user)
    sent_groups = Group.objects.all().filter(
        starter_id=request.user.id)

    res_data['ok'] = True
    res_data['recieved'] = [g.as_dict() for g in recieved_groups]
    res_data['sent'] = [g.as_dict() for g in sent_groups]
    return HttpResponse(json.dumps(res_data), content_type="application/json")

def accept_group(request, pid):
    '''
    Used for AJAX
    Accept received (pending) group

    Find the group from db and change
        pending: 1 -> 0
        success: 0 -> 1
    '''
    res_data = {}
    if not request.user.is_authenticated:
        res_data = {
            'ok': False,
            'message': 'You are no authenticated!',
        }
        return HttpResponse(json.dumps(res_data), content_type="application/json")
    
    # group_pid = request.POST.get('id', '')

    # # Check there is a group id
    # if group_pid == '':
    #     res_data = res_data = { 'ok': False, 'message': 'No id is sent' }
    #     return HttpResponse(json.dumps(res_data), content_type="application/json")
    
    try:
        group_instance = Group.objects.get(id=pid)
    except:
        res_data = res_data = { 'ok': False, 'message': 'Group does not exsit' }
        return HttpResponse(json.dumps(res_data), content_type="application/json")

    # Verify the group id is own by request.user
    if group_instance.target_id != request.user.id:
        res_data = res_data = { 'ok': False, 'message': 'Not target user'}
        return HttpResponse(json.dumps(res_data), content_type="application/json")

    # Verify the group is in a valid state
    if group_instance.is_pending == False or group_instance.is_success == True:
        res_data = res_data = {'ok': False, 'message': 'The group is not waiting, maybe already accepted'}
        return HttpResponse(json.dumps(res_data), content_type="application/json")

    # Change the state of group
    group_instance.is_pending = False
    group_instance.is_success = True
    group_instance.save()

    res_data['ok'] = True
    res_data['data'] = group_instance.as_dict()
    return HttpResponse(json.dumps(res_data), content_type="application/json")

def group_result(request):
    '''
    View of accepted grouping result
    '''

    # TODO: Calculate the free time in this week and show 
    # TODO: Show with graph
    # TODO: Calculate first and save in DB?
    pass

def events(request):
    '''
    API to show all events for the user
    '''

    # TODO: check user auth
    pass
def add_event(request):
    '''
    API to add a new event for the user from POST
    '''
    # TODO: check user auth
    # TODO: read data from POST
    pass

def update_event(request):
    '''
    API to update an event for the user from POST
    '''
    # TODO: check user auth
    # TODO: check the user own the event
    # TODO: read data from POST
    pass
    
def del_event(request, id):
    '''
    API to del event id=id using GET
    '''
    # TODO: check user auth
    # TODO: check the user own the event
    # TODO: refer my function accept_group
    pass 

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


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = CalendarSerializer

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
