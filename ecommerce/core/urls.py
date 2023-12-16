from django.urls import path
from . import views

# main html file and other file also can be here
urlpatterns = [path('', views.index, name='index'),
               ]
