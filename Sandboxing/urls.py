from django.contrib import admin
from . import views
from django.urls import path,include

urlpatterns = [
    path('compile', views.compile, name='compile'),
    path('run', views.run, name='run')
]
