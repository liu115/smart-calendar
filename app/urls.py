from django.urls import path,include
from .views import login, index
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    #path('accounts/', include('SmartCalendar.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),

]
