from django.contrib import admin
from . import views
from django.urls import path,include

urlpatterns = [
    path('compileAndRun', views.compileAndRun, name='compileAndRun'),
    path('question/<id>', views.code_input, name='code_input'),
]
