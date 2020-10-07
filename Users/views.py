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
from Sandboxing.views import compile, run

# whenever well write a function which requires the user to be logged in user login_required decorator.

starttime = 0
endtime = 0
totaltime = 0
start = datetime.datetime (2020, 1, 1, 00, 59)  # contest time is to be set here


def handler404(request, exception):
    return render(request, 'Users/404.html', status=404)


def handler500(request):
    return render(request, 'Users/500.html', status=500)


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
        now = datetime.datetime.now()
        global start
        if now >= start:
            return usersignup(request)
        else:
            return render(request, 'Users/wait.html')


def Timer(request) :    # this will be hit by admins
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
            lang = request.POST.get('def_lang')
            college = request.POST.get ('college')
            print("34263987")
            try:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                print("34")
                profile = Profile(user=user, name=name, phone=phone, email=email, def_lang=lang, college=college)
                # q=Questions(quesTitle="0's n 1's",quesDesc="Sample Question 3: should return o/p 1 mfor i/p 0",sampleInput="0",sampleOutput="1")   #added a sample question from this for time being will need to modify this later
                # q.save()
                print("wddws")
                profile.save()
                # print("2")
                parent_dir = "questions/usersub/"  # add 'users' directory inside questions directory while deploying as empty
                # folders don't get committed to repo
                path = os.path.join(parent_dir, username)
                os.mkdir(path)
                login(request, user)
                print("4433")
                return questionHub(request)  # next page as of now user has logged in
            except:
                messages.error(request, 'username already taken, try something else.')
            print("34")
            profile = Profile (user=user, name=name, phone=phone, email=email,def_lang=lang, college=college)
            #q=Questions(quesTitle="0's n 1's",quesDesc="Sample Question 3: should return o/p 1 mfor i/p 0",sampleInput="0",sampleOutput="1")   #added a sample question from this for time being will need to modify this later
            #q.save()
            print("wddws")
            profile.save ()
            #print("2")
            parent_dir = "questions/usersub/"	#add 'users' directory inside questions directory while deploying as empty
            # folders don't get committed to repo
            path = os.path.join (parent_dir, username)
            os.mkdir (path)
            login (request, user)
            print("4433")
            return questionHub(request)  # next page as of now user has logged in

        except :
            return render(request, "Users/home.html")


    elif request.method == 'GET' :
        return render (request, "Users/home.html")


# Just a crude, temporary sign-in function
def usersignin(request) :
    if request.method == 'POST' :
        username = request.POST.get ('user')
        pass_e = request.POST.get ('auth_pass')

        user = authenticate (request, username=username, password=pass_e)

        if user is not None :
            login(request, user)
            q = Questions(quesTitle="Question 1", quesDesc="Sample Question 1: description",
                          sampleInput="0",
                          sampleOutput="1")  # added a sample question from this for time being will need to modify this later
            q.save()
            q = Questions(quesTitle="Question 2", quesDesc="Sample Question 2: description",
                          sampleInput="0",
                          sampleOutput="1")  # added a sample question from this for time being will need to modify this later
            q.save()
            q = Questions(quesTitle="Question 3", quesDesc="Sample Question 3: description",
                          sampleInput="0",
                          sampleOutput="1")  # added a sample question from this for time being will need to modify this later
            q.save()
            q = Questions(quesTitle="Question 4", quesDesc="Sample Question 4: description",
                          sampleInput="0",
                          sampleOutput="1")  # added a sample question from this for time being will need to modify this later
            q.save()
            q = Questions(quesTitle="Question 5", quesDesc="Sample Question 5: description",
                          sampleInput="0",
                          sampleOutput="1")  # added a sample question from this for time being will need to modify this later
            q.save()
            q = Questions(quesTitle="Question 6", quesDesc="Sample Question 6: description",
                          sampleInput="0",
                          sampleOutput="1")  # added a sample question from this for time being will need to modify this later
            q.save()
            #return render (request, 'Users/code_input_area.html')   #login for time being, work through signup for now
            return render(request, 'Users/instructpage.html')
        else :
            return render (request, 'Users/LoginPage.html', context={'error' : True})

    return render (request, 'Users/LoginPage.html')


@login_required(login_url='/login')
def questionHub(request) :
    print("dfde")
    questions = Questions.objects.all ( )
    for q in questions :
        if (q.totalSubmision == 0) :
            q.accuracy = 0
        else :
            q.accuracy = (q.SuccessfulSubmission / q.totalSubmision) * 100
    print("dvbdivbuidhvi")
    return render (request, 'Users/questionhub.html', context={'questions' : questions,}) #we had made questions.html for testing have replaced eith questionhub for frontend integration  # we can pass accuracy too but we can acess it with question.accuracy



@login_required(login_url='/login')
def code_input(request,ques_id=1):

    description = Questions.objects.get(pk=ques_id)
    User = request.user
    username = User.username
    if request.method == 'POST':
        code = request.POST.get('user_code')
        lang = request.POST.get('lang')

        user_sub_path = 'questions/usersub/{}/question{}'.format(username, ques_id)
        user_sub = user_sub_path + ".{}".format(lang)
        code = str(code)

        BASE_DIR = os.getcwd() + '/Sandboxing/include/sandbox.h'
        if lang == 'cpp':
            header_file = '#include "{}"\n'.format(BASE_DIR)
            parts = code.split("main()")
            beforemain=parts[0]+"main()"
            aftermain=parts[1]
            funcpoint = aftermain.find('{') + 1
            main = beforemain + aftermain[0:funcpoint] + "install_filters();" + aftermain[funcpoint:]
            with open(user_sub, 'w+') as inf:
                inf.write(header_file)
                inf.write(main)
                inf.close()

        else:
            with open(user_sub, 'w+') as inf:
                inf.write('import sandbox\n')
                inf.write(code)
                inf.close()

        sub = Submissions( userID=User, quesID=description ,codeLang=lang, score=0)
        sub.save()

        currentQues = Questions.objects.get(pk=ques_id)
        casesPassed = 0
        errorStatus = ["CTE", "SE", "RTE", "TLE"]
        userOutputStatus = []
        currentScore = 0
        try:
            compileStatus = compile(username, ques_id, lang)
            for status in errorStatus:
                if status == compileStatus:
                    return render(request, 'Users/testcases.html',context={'question': description , 'user': User, 'error': '', 'casesPassed': casesPassed, 'compileStatus': compileStatus, 'score': currentScore})
            if compileStatus == 'AC':
                for i in range(1, currentQues.testcases):
                    runStatus = run(username, ques_id, i, lang)
                    if runStatus == "AC":
                        casesPassed += 1
                        userOutputStatus.append(runStatus)
                    else:
                        for status in errorStatus:
                            if status == runStatus:
                                userOutputStatus.append(runStatus)
                    allCorrect = True
                    for i in userOutputStatus:
                        if i != 'AC':
                            allCorrect = False
                            break
                    if allCorrect:
                        currentUser = Profile.objects.get(user=request.user)
                        currentScore = currentUser.totalScore + 100
                        Profile.objects.update(user=request.user, totalScore=currentScore)
                return render(request, 'Users/testcases.html',context={'question': description , 'user': User, 'error': '', 'casesPassed': casesPassed, 'compileStatus': compileStatus, 'userOutputStatus': userOutputStatus, 'score': currentScore})
        except:
            return render(request, 'Users/testcases.html',context={'question': description , 'user': User, 'error': '', 'casesPassed': casesPassed, 'score': currentScore })
    return render(request, 'Users/testcases.html',context={'question': description , 'user': User, 'score': currentScore })

@login_required(login_url='/login')
def leaderboard(request):
    # it will always be post request so no if....
    questions = Questions.objects.all()
    scoremap = {}
    for user in Profile.objects.order_by ("-totalScore") :
        qscores = []
        for n in range (1, 7) :
            try :
                check = Submissions.objects.get (quesID=n)
                qscores.append (check.score)
            except ObjectDoesNotExist :
                qscores.append (0)
        qscores.append (user.totalScore)
        scoremap[ user.user ] = qscores

    sorted (scoremap.items ( ), key=lambda items : (items[ 1 ][ 6 ], Submissions.latestSubTime))
    # in case we want to check if the latest sub. time is before end time we need to add here something working on it ...
    return render (request, 'Users/LEADERBOARD.html', context={'dict' : qscores, 'range' : range (1, 7, 1),'questions':questions,})
    # html for leaderboard is to be created



@login_required(login_url='/login')
def createsubmission(request) :
    if request.method == 'POST' :
        try :
            # title = request.POST.get('title')
            # username = request.user.username
            codeLang = request.POST.get ('lang')
            questions = Questions.objects.get (id=1)  # Currently hard coded to 1, so make sure you have at least 1
            # question in your dummy questions table. Later we'll add appropriate logic here

            userID = request.user
            score = 0  # calculated by checking criteria
            submission = Submissions (quesID=questions, userID=userID, codeLang=codeLang, score=score,
                                      latestSubTime=datetime.datetime.now ( ))
            submission.save ()

            # Incrementing the attemptID of a submission for a *particular* user, each time he/she makes one, for a
            # *particular* question (Note that attemptID defaults to 0). This will hence result in a uniform file
            # structure as was shown on Slack
            last_submission_of_the_user = Submissions.objects.filter (quesID=questions,
                                                                      userID=userID).order_by ('attemptID').last ( )
            last_attempt_id = last_submission_of_the_user.attemptID
            submission.attemptID = last_attempt_id + 1
            submission.save ( )

            # question.totalSubmision += 1
            # question.SuccessfulSubmission += 1
            # question.save()
            return render (request, 'Users/code_input_area.html', context={'status' : 'SUCCESS', 'score' : score,'questions':questions})
        except Exception :
            return render (request, 'Users/code_input_area.html', context={'status' : 'FAIL',
                                                                           'traceback' : traceback.format_exc ( )})

@login_required(login_url='/login')
def showSubmission(request) :
    questions = Questions.objects.all()

    for q in questions:
        if (q.totalSubmision == 0):
            q.accuracy = 0
        else:
            q.accuracy = (q.SuccessfulSubmission / q.totalSubmision) * 100

    if request.method == 'POST' :
        try :

            username = request.POST.get ('username')
            userID = User.objects.get (username=username)
            submissions = Submissions.objects.filter (userID=userID).order_by ('-submissionTime')
            return render (request, 'Users/submission.html', context={'submissions' : submissions,'questions':questions, })
        except :
            return render (request, 'Users/submission.html', context={'error' : 'Some error'})
    return render (request, 'Users/submission.html', context={'error' : 'Some error','questions':questions,})

@login_required(login_url='/login/')
def instruction(request):
    if request.user.is_authenticated:
        try :
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = Profile()
        if request.method == 'POST':
            return render(request, 'Users/questionhub.html')
        return render(request, 'Users/instructpage.html')
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
@login_required(login_url='/login')
def question_view(request,id):
    context = {}
    context['data'] = Questions.objects.get(id=id)
    questions = Questions.objects.all()
    if request.method == 'POST':
        return code_input(request,questions[0].id)

    return render(request,'Users/cp_style.html',context={'questions' : questions,'context':context})
    #return render(request, 'Users/cp_style.html',data)

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




def loadBuffer(request):
    user = Profile.objects.get(user=request.user)
    username = request.user.username
    qn = request.POST.get('question_no')
    lang = request.POST.get('lang')

    response_data = {}

    codeFile = 'questions/usersub/{}/question{}.{}'.format(username, qn,  lang)

    txt = ""

    try:
        f = open(codeFile, "r")
        txt = f.read()
        f.close()
    except FileNotFoundError:
        pass

    response_data["txt"] = txt

    return HttpResponse(response_data)
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

def logout(request):
    request.user.logout(request)

def test(request):
    return render(request,'Users/testcases.html')