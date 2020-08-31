from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from .models import Profile, Questions, Submissions
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# whenever well write a function which requires the user to be logged in user login_required decorator.

starttime = 0
endtime = 0
totaltime = 0
start = datetime.datetime(2020, 1, 1, 00, 59)  # contest time is to be set here


def check():
    global starttime
    global endtime
    time = datetime.datetime.now()
    now = (time.hour * 60 * 60) + (time.minute * 60) + time.second
    if now < endtime:
        return 1  # we can also return endtime - now
    else:
        return 0


def wait(request):
    check = datetime.datetime.now()
    global start
    if check >= start:
        return usersignup(request)
    else:
        return render(request, 'Users/wait.html')


def Timer(request):
    if request.method == 'POST':
        global starttime, start, endtime, totaltime
        request.POST.get('totaltime')  # mostly it will remain preset just in case needed
        start = datetime.datetime.now()
        time = start.second + start.minute * 60 + start.hour * 60 * 60
        starttime = time
        endtime = time + int(totaltime)
        return HttpResponse(" timer is set ")

    return render(request, 'Users/timer.html')


def usersignup(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            college = request.POST.get('college')
            user = User.objects.create_user(username=username, password=password)
            profile = Profile(user=user, name=name, phone=phone, email=email, college=college)
            profile.save()

            parent_dir = "questions/usersub/"
            path = os.path.join(parent_dir, username)
            os.mkdir(path)
            login(request, user)
            return render(request, "Users/sucess.html")  # next page as of now user has logged in

        except:
            return render(request, 'Users/home.html')

    elif request.method == 'GET':
        return render(request, "Users/home.html")
    return (questionHub(request))


def leaderboard(request):
    # it will always be post request  so no if....
    scoremap = {}
    for user in Profile.objects.order_by("-totalScore"):
        qscores = []
        for n in range(1, 7):
            try:
                check = Submissions.objects.get(quesID=n)
                qscores.append(check.scoreQuestion)
            except Submissions.DoesNotExist:
                qscores.append(0)
        qscores.append(user.totalScore)
        scoremap[user.user] = qscores

    sorted(qscores.items(), key=lambda items: (items[1][6], Submissions.latestSubTime))
    # incase we want to check if the latest sub. time is before end time we need to add here something working on it ...
    return render(request, 'Users/home.html', context={'dict': qscores, 'range': range(1, 7, 1)})
    # html for leaderboard is to be created


def DisplayQuestion(request):
    # if is not required as request is always POST
    questionnumber = int(request.POST.get('#'))  # # wil be replaced with the question number variable on the tab
    question = Questions.objects.get(id=questionnumber)
    questiondata = [question.quesTitle, question.quesDesc, question.sampleInput, question.sampleOutput]
    return render(request, '#', context={'ques': questiondata})  # # will be replaced with question display page


def CodeInput(request):
    if request.method == 'POST' and request.FILES['#']:
        codefile = request.FILES['#']
        lines = codefile.readlines()
        for line in lines:
            # code to print lines to compiler, not sure how it exactly works so leaving it black for now
            pass
        render(request, '#', context={'success': 'File Uploaded!'})
    render(request, '#')  # # is questions page

def questionHub(request):

    questions = Questions.objects.all()

    for q in questions:
        if(q.totalSubmision==0):
            q.accuracy = 0
        else:
            q.accuracy = (q.SuccessfulSubmission/q.totalSubmision) * 100
        return render(request, 'Users/question.html', context={'questions': questions}) # we can pass accuracy too but we can acess it with question.accuracy