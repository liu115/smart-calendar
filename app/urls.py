from django.urls import path,include
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('SmartCalendar.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('invite', views.invite, name='invite'),
    path('calendar', views.calendar, name='calendar'),
    path('', views.index, name='index'),
    path('api/query_group', views.query_group, name='query_group'),
    path('api/accept_group/<int:pid>', views.accept_group, name='accept_group'),
    path('api/events', views.events, name='event'),
    path('api/add_event', views.add_event, name='add_event'),
    path('api/update_event', views.update_event, name='update_event'),
    path('api/del_event/<int:id>', views.del_event, name='del_event'),
]
