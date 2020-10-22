from django.contrib import admin
from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.wait, name='wait'),
    path('signup', views.usersignup, name='signup'),
    #path('login/', auth_views.LoginView.as_view(template_name="Users/LoginPage.html"), name='login'),
    path('login/', views.usersignin, name='login'),
    path('login/upload', views.code_input, name='upload'),
    path('loadBuffer', views.loadBuffer, name='loadBuffer'),
    path('timer/', views.Timer, name='timer'),
    #path('login/submit', views.submit, name='submit'),
    path('showSubmissions/<id>/', views.showSubmission, name='showSubmissions'),
    path('instruction/',views.instruction,name="instruction"),
    #path('emergency',views.emergency_login,name="emergency"),
    path('question/<id>/',views.question_view,name='question_view'),
    path ('password_reset/', views.reset, name='password_reset'),
    path ('security_questions/', views.security, name='security_questions'),
    path ('leaderboard/', views.leaderboard, name='leaderboard'),
    path ('questionhub/', views.questionHub, name='questionhub'),
    path('test/', views.test, name='testcases'),
    path('result/',views.result,name='result'),


]
