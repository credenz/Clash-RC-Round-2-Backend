"""ClashRCRound2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Users import views
from Sandboxing import views
#ive removed thee paths also, as ryt now we dot need to configure all paths.....later on itll be a tedious job if we do it from now for every page!!

handler404 = 'Users.views.handler404'
handler500 = 'Users.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Users.urls')),
    path('', include('Sandboxing.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]


