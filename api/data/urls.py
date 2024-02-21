from django.urls import path, include
from data import views

urlpatterns = [
    path('data_pipe', views.data_pipe)
]
