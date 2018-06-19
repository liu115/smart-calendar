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
        r1=Group.objects.create(group_id=request.user.id,starter_id=request.user.id,starter_name=request.user.username,target_id=target_user_instance.id,target_name=target_user,is_pending=True,is_success=False )
        r1.save()
        messages.add_message(request, messages.INFO, 'Invitation was sent')
        
    except:
        messages.add_message(request, messages.WARNING, 'target user not exists!')
        return HttpResponseRedirect(reverse_lazy('index'))


    
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

def group_result(request,gid):
    '''
    View of accepted grouping result
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    
    res_data={}
    
    try:
        import datetime
        g1=Group.objects.get(id=gid)
        if g1.starter_id != request.user.id and g1.target_id != request.user.id:
            res_data['ok']=False
            res_data['messages'] = "Group_{} does not belong to you !!".format(gid)
        elif g1.starter_id == request.user.id and g1.is_pending == True:
            res_data['ok']=False
            res_data['messages'] = "Group_{} does not been accepted !!".format(gid)

        elif g1.target_id == request.user.id and g1.is_pending == True:
            res_data['ok']=False
            res_data['messages'] = "You have not accepted the invite!!".format(gid)
        else:
            #TODO: get starter's and target's events from db
            #TODO: compute the two user's same free time
            u1_events=Event.objects.filter(owner_user_id=g1.starter_id,
                                           starttime__lte=(datetime.datetime.now()+datetime.timedelta(days=7)),
                                           endtime__gte=datetime.datetime.now())
            
            u2_events=Event.objects.filter(owner_user_id=g1.target_id,
                                           starttime__lte=(datetime.datetime.now()+datetime.timedelta(days=7)),
                                           endtime__gte=datetime.datetime.now())
            
            t =datetime.timedelta(hours=2)
            basetime=datetime.datetime.now(datetime.timezone.utc)
            nowtime=basetime
            freetime=[]
            while (basetime-nowtime <= datetime.timedelta(hours=168)):
                free=True
                if u1_events !=[]:
                    for event in u1_events:
                        if((event.starttime < (basetime+t) and event.starttime > basetime)  
                            or (event.endtime < (basetime+t) and event.endtime > basetime)
                            or (event.starttime < basetime and event.endtime > basetime+t)):
                            free=False
                            break
                if u2_events != [] and free ==True:
                    for event in u2_events:
                        if((event.starttime < (basetime+t) and event.starttime > basetime)  
                            or (event.endtime < (basetime+t) and event.endtime > basetime)
                            or (event.starttime < basetime and event.endtime > basetime+t)):
                            free=False
                            break
                if (free ==True):
                    freetime.append([basetime.timestamp(),(basetime+t).timestamp()])
                basetime =basetime + t
            print(len(freetime))
            
            if(freetime == []):
                res_data['ok']=False
                res_data['messages']='no free time in this week'
            else:
                res_data['ok']=True
                res_data['time'] = freetime








    except Group.DoesNotExist:
        res_data['ok']=False
        res_data['messages'] = "Group_{} does not exit !!".format(gid) 

    return HttpResponse(json.dumps(res_data), content_type="application/json")
    
    # TODO: Calculate the free time in this week and show 
    # TODO: Show with graph
    # TODO: Calculate first and save in DB?
    pass

def events(request):
    '''
    API to show all events for the user
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')

    events_objects = Event.objects.filter(owner_user_id= request.user.id)

    res_data={}
    #e1= Event.objects.create(owner_user_id=request.user.id,title='group meeting',starttime='2018-6-20',endtime='2018-6-21')
    #e1.save()
    res_data['data']= [ g.as_dict() for g in events_objects ]

    return HttpResponse(json.dumps(res_data), content_type="application/json")


    # TODO: check user auth
    pass
def add_event(request):
    '''
    API to add a new event for the user from POST
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    owner_user_id =request.user.id

    title=request.POST.get('title')
    starttime=request.POST.get('starttime')
    endtime=request.POST.get('endtime')
    p_color = request.POST.get('p_color')
    s_color = request.POST.get('s_color')
    comment=request.POST.get('comment','')

    e1= Event.objects.create(owner_user_id=owner_user_id,title=title,starttime=starttime,endtime=endtime,p_color=p_color,s_color=s_color,comment=comment)
    e1.save()
    
    res_data={}
    res_data['ok'] = True
    res_data['messages'] = 'Add a new events successfully'
    
    return HttpResponse(json.dumps(res_data), content_type="application/json")

    # TODO: check user auth
    # TODO: read data from POST
    pass

def update_event(request):
    '''
    API to update an event for the user from POST
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    
    owner_user_id =request.user.id
    event_id= request.POST.get('event_id')
    title=request.POST.get('title')
    starttime=request.POST.get('starttime')
    endtime=request.POST.get('endtime')
    p_color = request.POST.get('p_color')
    s_color = request.POST.get('s_color')
    comment=request.POST.get('comment','')
    res_data={}
    
    try:
        e1=Event.objects.get(id = event_id)

        if e1.owner_user_id != owner_user_id :
            res_data['ok']=False
            res_data['messages'] = "Event {} does not belong to you !!".format(id) 
        else :
            e1.title= title
            e1.starttime = starttime
            e1.endtime = endtime
            e1.comment = comment
            e1.p_color = p_color
            e1.s_color = s_color
            e1.save()
            res_data['ok']=True
            res_data['messages'] = "Event {} has been update".format(id) 
    except Event.DoesNotExist:
        res_data['ok']=False
        res_data['messages'] = "Event {} does not exit !!".format(id) 
    
    return HttpResponse(json.dumps(res_data), content_type="application/json")
    # TODO: check user auth
    # TODO: check the user own the event
    # TODO: read data from POST
    pass
    
def del_event(request, id):
    '''
    API to del event id=id using GET
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')

    res_data={}
    try:
        e1=Event.objects.get(id = id)
        if e1.owner_user_id != request.user.id:
            res_data['ok']=False
            res_data['messages'] = "Event {} does not belong to you !!".format(id) 
        else:
            e1.delete()
            res_data['ok']=True
            res_data['messages'] = "Event {} has been removed !!".format(id) 
    except Event.DoesNotExist:
        res_data['ok']=False
        res_data['messages'] = "Event {} does not exit !!".format(id) 
    # TODO: check user auth
    # TODO: check the user own the event
    # TODO: refer my function accept_group
    return HttpResponse(json.dumps(res_data), content_type="application/json")


def calendar(request):
    '''
    Show users calendars
    '''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You are no authenticated!')
    print(request.user.username, request.user.id)
    # TODO: read data from db and render

    # Fake data
    #import time
    #events = [
    #    { 'title': 'group meeting', 'starttime': time.asctime(time.localtime()), 'duration': 20 },
    #    { 'title': 'ML class', 'starttime': time.asctime(time.localtime(time.time() + 1000000)), 'duration': 300 }
    #]
    return render(request, 'calendar.html', locals())


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = CalendarSerializer

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
