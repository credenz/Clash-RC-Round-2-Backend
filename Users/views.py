from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from .models import Profile, Questions, Submissions
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import traceback
from django.contrib import messages

# whenever well write a function which requires the user to be logged in user login_required decorator.

starttime = 0
endtime = 0
totaltime = 0
start = datetime.datetime (2020, 1, 1, 00, 59)  # contest time is to be set here


def check() :
    global starttime
    global endtime
    time = datetime.datetime.now ( )
    now = (time.hour * 60 * 60) + (time.minute * 60) + time.second
    if now < endtime :
        return 1  # we can also return endtime - now
    else :
        return 0


def wait(request) :
    check = datetime.datetime.now ( )
    global start
    if check >= start :
        return usersignup (request)
    else :
        return render (request, 'Users/wait.html')


def Timer(request) :
    if request.method == 'POST' :
        global starttime, start, endtime, totaltime
        request.POST.get ('totaltime')  # mostly it will remain preset just in case needed
        start = datetime.datetime.now ( )
        time = start.second + start.minute * 60 + start.hour * 60 * 60
        starttime = time
        endtime = time + int (totaltime)
        return HttpResponse (" timer is set ")

    return render (request, 'Users/timer.html')


def usersignup(request) :
    if request.method == 'POST' :
        try :
            username = request.POST.get ('username')
            password = request.POST.get ('password')
            name = request.POST.get ('name')
            phone = request.POST.get ('phone')
            email = request.POST.get ('email')
            college = request.POST.get ('college')
            user = User.objects.create_user (username=username, password=password)
            profile = Profile (user=user, name=name, phone=phone, email=email, college=college)
            profile.save ( )

            parent_dir = "questions/users/"	#add 'users' directory inside questions directory while deploying as empty
            # folders don't get committed to repo
            path = os.path.join (parent_dir, username)
            os.mkdir (path)
            login (request, user)
            return render (request, "Users/success.html")  # next page as of now user has logged in

        except :
            return render (request, 'Users/home.html')

    elif request.method == 'GET' :
        return render (request, "Users/home.html")
    return (questionHub (request))


# Just a crude, temporary sign-in function
def usersignin(request) :
    if request.method == 'POST' :
        username = request.POST.get ('user')
        pass_e = request.POST.get ('auth_pass')

        user = authenticate (request, username=username, password=pass_e)

        if user is not None :
            login(request, user)
            return render (request, 'Users/code_input_area.html')
        else :
            return render (request, 'Users/login.html', context={'error' : True})

    return render (request, 'Users/login.html')


def leaderboard(request) :
    # it will always be post request so no if....
    scoremap = {}
    for user in Profile.objects.order_by ("-totalScore") :
        qscores = [ ]
        for n in range (1, 7) :
            try :
                check = Submissions.objects.get (quesID=n)
                qscores.append (check.score)
            except ObjectDoesNotExist :
                qscores.append (0)
        qscores.append (user.totalScore)
        scoremap[ user.user ] = qscores

    sorted (qscores.items ( ), key=lambda items : (items[ 1 ][ 6 ], Submissions.latestSubTime))
    # in case we want to check if the latest sub. time is before end time we need to add here something working on it ...
    return render (request, 'Users/home.html', context={'dict' : qscores, 'range' : range (1, 7, 1)})
    # html for leaderboard is to be created


# @login_required
def codeInput(request) :
    if request.method == 'POST' and request.FILES[ 'code_file' ] :
        username = request.user.username
        ques_id = 1  # Currently hard coded to 1, so make sure you have at least 1 question in your dummy questions
        # table. Later we'll add appropriate logic here

        current_submission_of_the_user = Submissions.objects.filter (userID=request.user.id).order_by (
            'attemptID').last ( )
        current_attempt_id = current_submission_of_the_user.attemptID
        extension = Submissions.objects.filter (quesID=ques_id, userID=request.user.id,
                                                attemptID=current_attempt_id).last ( ).codeLang  # This line of code is a
        # bit doubtful, as I am not able to figure out: whether or not last() works always or there exists an
        # exceptional case

        if 'question{}'.format (ques_id) not in os.listdir ('questions/users/{}'.format (username)) :
            ques_dir = os.path.join ('questions/users/{}'.format (username), 'question{}'.format (ques_id))
            os.mkdir (ques_dir)

        with open ('questions/users/{}/question{}/code{}.{}'.format (username, ques_id, current_attempt_id, extension),
                   'wb') as copy :
            for chunk in request.FILES[ 'code_file' ].chunks ( ) :
                copy.write (chunk)

        return HttpResponse ('File has been uploaded Successfully!')  # Later, we'll remove this statement and uncomment
        # the bottom one:
        # render(request, '#', context={'success': 'File Uploaded!'})
    render (request, 'Users/submissions.html')


def questionHub(request) :
    questions = Questions.objects.all ( )

    for q in questions :
        if (q.totalSubmision == 0) :
            q.accuracy = 0
        else :
            q.accuracy = (q.SuccessfulSubmission / q.totalSubmision) * 100
        return render (request, 'Users/question.html', context={
            'questions' : questions})  # we can pass accuracy too but we can acess it with question.accuracy


# @login_required
def submit(request) :
    if request.method == 'POST' :
        try :
            # title = request.POST.get('title')
            # username = request.user.username
            codeLang = request.POST.get ('lang')
            question = Questions.objects.get (id=1)  # Currently hard coded to 1, so make sure you have at least 1
            # question in your dummy questions table. Later we'll add appropriate logic here

            userID = request.user
            score = 0  # calculated by checking criteria
            submission = Submissions (quesID=question, userID=userID, codeLang=codeLang, score=score,
                                      latestSubTime=datetime.datetime.now ( ))
            submission.save ( )

            # Incrementing the attemptID of a submission for a *particular* user, each time he/she makes one, for a
            # *particular* question (Note that attemptID defaults to 0). This will hence result in a uniform file
            # structure as was shown on Slack
            last_submission_of_the_user = Submissions.objects.filter (quesID=question,
                                                                      userID=userID).order_by ('attemptID').last ( )
            last_attempt_id = last_submission_of_the_user.attemptID
            submission.attemptID = last_attempt_id + 1
            submission.save ( )

            # question.totalSubmision += 1
            # question.SuccessfulSubmission += 1
            # question.save()
            return render (request, 'Users/code_input_area.html', context={'status' : 'SUCCESS', 'score' : score})
        except Exception :
            return render (request, 'Users/code_input_area.html', context={'status' : 'FAIL',
                                                                           'traceback' : traceback.format_exc ( )})


def showSubmission(request) :
    if request.method == 'POST' :
        try :
            username = request.POST.get ('username')
            userID = User.objects.get (username=username)
            submissions = Submissions.objects.filter (userID=userID).order_by ('-submissionTime')
            return render (request, 'Users/submissions.html', context={'submissions' : submissions})
        except :
            return render (request, 'Users/submissions.html', context={'error' : 'Some error'})
    return render (request, 'Users/submissions.html', context={'error' : 'Some error'})


def instruction(request):
    if request.user.is_authenticated:
        try :
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = Profile()
        if request.method == 'POST':
            return render(request, 'Users/questionhub.html')
        return render(request, 'Users/instruction.html')
    else :
        return redirect("signup")


'''def emergency_login(request):  #Later on we will decide it should be needed or not
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        AdminPass = request.POST.get('admin_password')
        user = authenticate(username=username, password=password)
        if AdminPass == '#':
            if user.is_active:
                login(request, user)
                return redirect('questionHub')
        else:
            return HttpResponse('Invalid credentials!!!')
    else:
        return render(request, 'Users/emglogin.html')'''

def question_view(request,id):
    context = {}
    context['data'] = Questions.objects.get(id=id)
    return render(request,'Users/question_view.html',context)

def reset(request) :
    if request.method == "POST" :
        usern=request.POST.get('unam')
        pas = request.POST.get ('pas')
        pas1 = request.POST.get ('pas1')
        if User.objects.filter (username=usern).exists ( ):

             if pas == pas1 and usern==unameeee:
                messages.success (request, f'Password has been created!!!You Can Login now with new password!')
                u=User.objects.get(username=usern)
                u.set_password(pas)
                u.save()
                return render(request,"Users/password_reset.html")
             else :
                messages.warning (request, f'Invalid Credentials!!!')
                return redirect ('/password_reset')
        else:
             messages.warning (request, f'User does not exist!!!')
             return redirect('/password_reset')


    return render (request, "Users/password_reset.html")


def security(request) :
    global unameeee
    if request.method == "POST" :
        username1 = request.POST.get ('u_name')
        phoneno1 = request.POST.get ('ppno')
        unameeee=username1
        #  dob1 = request.POST.get('dob11')
        if User.objects.filter(username=username1).exists() and Profile.objects.filter(phone=phoneno1).exists() :
            if set(Profile.objects.filter(phone=phoneno1)) == set(Profile.objects.filter(user=User.objects.get (username=username1))):
                return redirect("/password_reset")

            else:
                messages.warning (request, f' Invalid credentials!!!!')
                return redirect ("/security_questions")
        else :
            messages.warning (request, f'Invalid credentials!!!!')
            return redirect ("/security_questions")
    return render ( request,'Users/security_questions.html')

