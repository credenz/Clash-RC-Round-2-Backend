from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib.auth.decorators import login_required
#whenever well write a function which requires the user to be logged in user login_required decorator.

starttime = 0
endtime = 0
totaltime = 0
start = datetime.datetime(2020, 1, 1, 0, 0)


#since the timer is required in every page well call this function in every view function
#ive hashed out the pages bcuz well get the pages from frontend team and well implement on those templates accordingly
def Timer(request):
    if request.method == 'POST':
        global starttime, start
        global endtime
        global totaltime
        request.POST.get('totaltime')
        start = datetime.datetime.now()
        time = start.second + start.minute * 60 + start.hour * 60 * 60
        starttime = time
        endtime = time + int(totaltime)
        return HttpResponse(" timer is set ")
    
    return render(request, '#')


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('#')
        password = request.POST.get('#')
        user = authenticate(username = username, password = password)
        if user:
            return render(request, '#')#login page
        else:
            return render(request, '#', context = {'invalid':'Details Entered are Incorrect!'})#samepage

    return render(request, '#')
