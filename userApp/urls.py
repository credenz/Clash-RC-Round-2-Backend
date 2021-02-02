from django.urls import path
from . import views
from django.conf.urls import url
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('', views.signin, name='login'),
    path('signup', views.signup, name='signup'),
    path('timer/', views.timer, name='timer'),
    path('cheat/',views.cheatcounter,name='cheat'),
    path('hlogout/', views.hardlogout, name='hlogout'),
    path('logout/', views.user_logout, name='logout'),
    path('leaderboard', never_cache(views.leader), name='leader'),
    path('lsus/', views.leadsus, name='lsus'),
    path('instructions', views.instructions, name='instructions'),
    path('checkUsername', views.check_username, name='check_username'),
    path('loadBuffer', views.loadBuffer, name='loadBuffer'),
    path('submissions/<int:qno>/<int:_id>/', views.view_sub, name='view_sub'),
    path('questionhub/', views.questionHub, name='questionHub'),
    path('user/<int:qn>', views.codeSave, name='codeSave'),
    path('emerlogin/', views.emergency_login),
    path('run', views.run, name='run'),
    path('submission/<qn>/', views.submission, name='submission'),
    url(r'^(?P<garbage>.*)/$', views.garbage, name='redirect'),
]
