from django.contrib import admin
from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.wait, name='wait'),
    path('signup', views.usersignup, name='signup'),
    path('login/', views.usersignin, name='login'),
    path('login/upload', views.codeInput, name='upload'),
    path('timer/', views.Timer, name='timer'),
    #path('login/submit', views.submit, name='submit'),
    path('showSubmissions', views.showSubmission, name='showSubmissions'),
    path('instruction',views.instruction,name="instruction"),
    #path('emergency',views.emergency_login,name="emergency"),
    path('question/<id>/',views.question_view,name='question_view'),
    path ('password_reset/', views.reset, name='password_reset'),
    path ('security_questions/', views.security, name='security_questions'),
]
