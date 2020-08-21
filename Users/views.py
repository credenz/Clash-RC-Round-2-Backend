from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import datetime

starttime = 0
endtime = 0
totaltime = 0
start = datetime.datetime(2020, 1, 1, 0, 0)
flag = False


def timer(request):
    if request.method == 'GET':
        return render(request, 'Users/timer.html')

    elif request.method == 'POST':
        global starttime, start
        global endtime
        global totaltime
        global flag
        flag = True
        request.POST.get('totaltime')
        start = datetime.datetime.now()
        time = start.second + start.minute * 60 + start.hour * 60 * 60
        starttime = time
        endtime = time + int(totaltime)
        return HttpResponse(" timer is set ")
