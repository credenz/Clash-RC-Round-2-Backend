import json
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from .models import Profile, Questions, Submission,multipleQues
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import traceback
from django.contrib import messages
from Sandboxing.views import compile, run, compileCustomInput, runCustomInput

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
            return render(request, 'Users/Instructions_final.html')
        else :
            return render (request, 'Users/LoginPage.html', context={'error' : True})

    return render (request, 'Users/LoginPage.html')


@login_required(login_url='/login')
def questionHub(request) :
    print("dfde")
    questions = Questions.objects.all ( )

    for q in questions :
        if (q.totalSubmision == 0) :
            q.accuracy = 0.0
        else :
            q.accuracy = ((q.SuccessfulSubmission / q.totalSubmision) * 100)
            q.accuracy=round(q.accuracy,1)

    return render (request, 'Users/questionhub.html', context={'questions' : questions,}) #we had made questions.html for testing have replaced eith questionhub for frontend integration  # we can pass accuracy too but we can acess it with question.accuracy



@login_required(login_url='/login')
def code_input(request,ques_id=1):
    que= Questions.objects.get(pk=ques_id)
    print(ques_id)
    User = request.user
    username = User.username
    isCustomInput = request.POST.get('isCustomInput')
    if request.method == 'POST':
        code = request.POST.get('user_code')
        print(code[0])
        lang = request.POST.get('lang')
        try:
            mul_que = multipleQues.objects.get(user=User, que=que)
            print("mulque",mul_que)
        except multipleQues.DoesNotExist:
            print("inside mulque")
            mul_que = multipleQues(user=User, que=que)
            mul_que.save()
        att = mul_que.attempts
        print("attempts:",att)
        path=os.getcwd() + '/questions/usersub/{}/question{}'.format(username,ques_id-1)
        if not(os.path.exists(path)):
            os.mkdir(path)
            file=open("{}/error.txt".format(path),'w')
            file.close()
            for i in range(1, 7):
                file1 = open("{}/output{}.txt".format(path, i), 'w+')
                file1.close()

        if (not isCustomInput):
            user_sub_path = os.getcwd() + '/questions/usersub/{}/question{}/question{}'.format(username, ques_id - 1,att)
        else:
            user_sub_path = os.getcwd() + '/questions/usersub/{}/question{}/customInputCode'.format(username, ques_id - 1)
        user_sub = user_sub_path + ".{}".format(lang)
        code = str(code)
        now_time = datetime.datetime.now()
        now_time_sec = now_time.second + now_time.minute * 60 + now_time.hour * 60 * 60
        global starttime
        submit_Time = now_time_sec - starttime

        hour = submit_Time // (60 * 60)
        val = submit_Time % (60 * 60)
        min = val // 60
        sec = val % 60

        subTime = '{}:{}:{}'.format(hour, min, sec)
        
        if (not isCustomInput):
            sub = Submission(code=code, user=User, quesID=que, attempt=att, subTime=subTime)
            sub.save()
            mul_que.attempts+=1
            mul_que.save()
        BASE_DIR = os.getcwd() + '/Sandboxing/include/'
        if lang == 'cpp' or lang == 'c':
            try:
                header_file = '#include "{}sandbox.h"\n'.format(BASE_DIR)
                parts = code.split("main()")
                beforemain=parts[0]+"main()"
                aftermain=parts[1]
                funcpoint = aftermain.find('{') + 1
                main = beforemain + aftermain[0:funcpoint] + "install_filters();" + aftermain[funcpoint:]
                with open(user_sub, 'w+') as inf:
                    inf.write(header_file)
                    inf.write(main)
                    inf.close()
            except IndexError:
                with open(user_sub, 'w+') as inf:
                    inf.write(code)
                    inf.close()

        else:
            with open(user_sub, 'w+') as inf:
                inf.write('import sandbox\n'.format(BASE_DIR))
                inf.write(code)
                inf.close()
            with open(BASE_DIR + 'sandbox.py', "r") as pythonHeader:
                sandboxFile = open("{}/sandbox.py".format(path), "w+")
                sandboxFile.writelines(pythonHeader.read())
                sandboxFile.close()

        # region custom input
        if (isCustomInput):
            try:
                customInput = request.POST.get('customInput')
                customInputFile = open(path+"/input.txt", "w")
                customInputFile.truncate(0)
                customInputFile.writelines(str(customInput))
                customOutputFile = open(path + "/customoutput.txt", "w")
                customOutputFile.truncate(0)
                customOutputFile.close()
                compileStatus = {
                    "returnCode":"CE"
                }
                # compileStatus['returnCode'] = 'CE'
                if (lang != 'py'):
                    compileStatus = compileCustomInput(username, ques_id - 1, lang)


                if compileStatus['returnCode'] != 'AC':
                    output={"output":compileStatus['error']}
                    return output
                    #return render(request, 'Users/question_view.html',context={'error':compileStatus['error']})

                runStatus = runCustomInput(username, ques_id - 1, att, lang)
                if runStatus['returnCode'] != "AC":
                    output = {"output": runStatus['error']}
                    return output
                    #return render(request, 'Users/question_view.html',context={'error':runStatus['error']})

                output = {"output": runStatus['output']}
                return output
                #return render(request, 'Users/question_view.html',context={'output':runStatus['output']})
            except Exception as e:
                output = {"output": "Something went wrong on the server."}
                return output
                #return render(request, 'Users/question_view.html',context={'error':'Something went wrong on the server.'})
        # endregion custom input

        #currentQues = Questions.objects.get(pk=ques_id - 1)
        casesPassed = 0
        console = os.getcwd() + '/questions/usersub/{}/question{}/error.txt'.format(username, ques_id - 1)
        consoleop = open(console, 'r')
        cases = [False, False, False, False, False, False]

        errorStatus = ["CTE", "SE", "RTE", "TLE","WA"]
        userOutputStatus = ["WA","WA","WA","WA","WA","WA"]

        currentScore = 0
        try:
            compileStatus = compile(username, ques_id - 1, att, lang)
            for status in errorStatus:
                if status == compileStatus:
                    case_list1 = json.dumps(cases)
                    return render(request, 'Users/testcases.html',context={'question': que , 'user': User, 'error': '', 'casesPassed': casesPassed, 'compileStatus': compileStatus, 'score': currentScore,'list':case_list1,'op':consoleop.read(),'status':status})
            if compileStatus == 'AC' or lang == 'py':
                for i in range(1, 7):
                    runStatus = run(username, ques_id - 1, att, i, lang)
                    # useroutfile = open(path + "/output{}.txt".format(i), "r")
                    # useroutfile.seek(0)
                    # print("asd " + useroutfile.readlines())
                    if runStatus == "AC":
                        cases[i-1] = True
                        casesPassed += 1
                        userOutputStatus[i-1]=runStatus
                    else:
                        for status in errorStatus:
                            if status == runStatus:
                                userOutputStatus[i-1]=runStatus
                allCorrect = True
                for i in userOutputStatus:
                    if i != 'AC':
                        allCorrect = False
                        break


                ans = "WA"

                if allCorrect:
                    ss = Questions.objects.get(pk=ques_id).SuccessfulSubmission + 1
                    Questions.objects.filter(pk=ques_id).update(SuccessfulSubmission=ss)
                    currentUser = Profile.objects.get(user=request.user)
                    mul = multipleQues.objects.get(user=request.user, que=ques_id)
                    currentScore = currentUser.totalScore
                    if (mul.scoreQuestion < 100):
                        currentScore = currentUser.totalScore + 100
                    multipleQues.objects.filter(user=request.user, que=ques_id).update(scoreQuestion=100)

                    Profile.objects.filter(user=request.user).update(totalScore=currentScore)
                    tp = Submission.objects.filter(user=User.id, quesID=ques_id).order_by('-subTime')[0]
                    tp.TestCasesPercentage=100
                    tp.save()

                    Submission.objects.filter(user=request.user, quesID=ques_id).update(subStatus='PASS')
                    #Submission.objects.filter(user=User.id, quesID=ques_id).last().update(subScore=mul.scoreQuestion)
                    ans = 'AC'
                case_list = json.dumps(cases)
                return render(request, 'Users/testcases.html',context={'question': que , 'user': User, 'error': '', 'casesPassed': casesPassed, 'compileStatus': compileStatus, 'userOutputStatus': userOutputStatus, 'score': currentScore,'list':case_list,'op':consoleop.read(),'status':ans})

        except Exception as e:
            case_list = json.dumps(cases)
            return render(request, 'Users/testcases.html',context={'question': que , 'user': User, 'error': '', 'casesPassed': casesPassed, 'score': currentScore,'list':case_list,'op':consoleop.read(), 'status': 'RE','list':case_list})
    case_list = json.dumps(cases)
    return render(request, 'Users/testcases.html',context={'question': que , 'user': User, 'score': currentScore,'list':case_list,'op':consoleop.read() })


def customInput(request):
    ques_id = request.POST.get('ques_id')
    o = code_input(request, int(ques_id))
    return JsonResponse(o)

@login_required(login_url='/login')
def leaderboard(request):
    current_user = request.user
    if current_user.is_authenticated:
        data = {}
        for rank, profile in enumerate(Profile.objects.order_by("-totalScore")):
            l = [0, 0, 0, 0, 0, 0, 0]
            for n in range(0, 6):
                try:
                    mulQue = multipleQues.objects.get(user=profile.user.id, que=n+1)
                    l[n] = mulQue.scoreQuestion
                except multipleQues.DoesNotExist:
                    l[n] = 0
            l[6] = profile.totalScore # last index is the totalScore
            # Getting the leaderboard details for the current user
            if profile.user.id == current_user.id:
                current_users_rank = rank+1
                current_users_score = l[6]

            data[profile.user] = l
        sorted(data.items(), key=lambda items: (items[1][6], Submission.subTime))

        # To find the status, which is = (total number of correctly answered questions / 6) * 100
        n_correct_answers = 0
        l = []
        cnt = 0
        filtered_qlist = Submission.objects.filter(user_id=current_user.id, subStatus='PASS').order_by('quesID_id')
        if filtered_qlist.exists():
            while cnt<filtered_qlist.count():
                current_id = filtered_qlist[cnt].quesID.id
                if current_id not in l:
                    n_correct_answers += 1
                    l.append(current_id)
                cnt+=1

        return render(request, 'Users/LEADERBOARD.html', context={'data': data.items(),
                                                                  'current_user': current_user,
                                                                  'user_rank': current_users_rank,
                                                                  'user_score': current_users_score,
                                                                  'user_initials': current_user.username[0:2].upper(),
                                                                  'status': str((n_correct_answers/6)*100)[0:4]})
    return HttpResponseRedirect(reverse("usersignup"))


@login_required(login_url='/login')
def result(request):
    current_user = request.user
    is_topper = False
    if current_user.is_authenticated:
        data = []
        l = [0, 0, '']
        for rank, profile in enumerate(Profile.objects.order_by("-totalScore")[:6]):
            data.append([rank+1, profile.totalScore, profile.user.username])
            # Getting the leaderboard details for the current user
            if profile.user.id == current_user.id:
                is_topper = True
                current_users_score = data[rank][1]
                current_users_rank = data[rank][0]

        if not is_topper:
            for rank, profile in enumerate(Profile.objects.order_by('-totalScore')):
                if profile.user.id == current_user.id:
                    current_users_rank = rank + 1
                    current_users_score = profile.totalScore
                    break
        # for correctly attempted questions, a.k.a 'Questions Solved'
        cnt = 0
        ls=[]
        n_correct_answers = 0
        filtered_qlist = Submission.objects.filter(user=current_user.id, subStatus='PASS').order_by('quesID_id')
        if filtered_qlist.exists():
            while cnt < filtered_qlist.count():
                current_id = filtered_qlist[cnt].quesID.id
                if current_id not in ls:
                    n_correct_answers += 1
                    ls.append(current_id)
                cnt += 1
        # To get the count of questions attempted by the user
        cnt = 0
        attempts = 0
        filtered_qlist = Submission.objects.filter(user=current_user.id).order_by('quesID_id')
        if filtered_qlist.exists():
            while cnt < filtered_qlist.count():
                current_id = filtered_qlist[cnt].quesID.id
                if current_id not in ls:
                    attempts += 1
                    ls.append(current_id)
                cnt += 1
        return render(request, 'Users/clash_resultpage_final.html', context={'data': data,
                                                                              'current_user': current_user,
                                                                              'que_attempted':attempts+n_correct_answers,
                                                                              'que_solved':n_correct_answers,
                                                                              'user_rank': current_users_rank,
                                                                              'user_score': current_users_score})
    else:
         return HttpResponseRedirect(reverse("usersignup"))

'''@login_required(login_url='/login')
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
            submission = Submission (quesID=questions, userID=userID, codeLang=codeLang, score=score,
                                      SubTime=datetime.datetime.now ( ))
            submission.save ()
            # Incrementing the attemptID of a submission for a *particular* user, each time he/she makes one, for a
            # *particular* question (Note that attemptID defaults to 0). This will hence result in a uniform file
            # structure as was shown on Slack
            last_submission_of_the_user = Submission.objects.filter (quesID=questions,
                                                                      userID=userID).order_by ('attempt').last ( )
            last_attempt_id = last_submission_of_the_user.attemptID
            submission.attemptID = last_attempt_id + 1
            submission.save ( )
            return render (request, 'Users/code_input_area.html', context={'status' : 'SUCCESS', 'score' : score,'questions':questions})
        except Exception :
            return render (request, 'Users/code_input_area.html', context={'status' : 'FAIL',
                                                                           'traceback' : traceback.format_exc ( )})
'''


@login_required(login_url='/login')
def showSubmission(request, id=0):

    current_user = request.user
    submissions = Submission.objects.filter(user=current_user.id, quesID=id).order_by('subScore')  #parameter should be the latest submission time for ordering
    questions = Questions.objects.all()
    try:
        return render(request, 'Users/submission.html',
                      context={'error': 'Some error', 'questions': questions, 'submissions': submissions})
    except:
        return render(request, 'Users/submission.html',
                      context={'error': 'Some error', 'questions': questions, 'submissions': submissions})


@login_required(login_url='/login')
def view_submission(request,qno,subid):
    context = {}
    context['data'] = Questions.objects.get(id=qno)
    print("contexr[data] id:", context['data'].id)
    if request.method == 'GET':
        context = {}
        sub = Submission.objects.get(id=subid)
        code = sub.code
        context['data'] = Questions.objects.get(id=qno)
        questions = Questions.objects.all()
        current_user = request.user
        us = Profile.objects.get(user=current_user)
        submissions = Submission.objects.filter(user=current_user.id, quesID=qno).order_by('-subScore')
        return render(request, 'Users/cp_style.html',
                      context={'user': us, 'questions': questions, 'context': context, 'submissions': submissions,
                               'code': code})
    elif request.method == 'POST':
        # submissions = Submission.objects.filter(user=current_user.id, quesID=ques_id).order_by('-subScore')[0]
        if request.method == 'POST':
            totsub = Questions.objects.get(pk=qno).totalSubmision + 1
            Questions.objects.filter(pk=qno).update(totalSubmision=totsub)
            return code_input(request, context['data'].id)

    return HttpResponse("Error")




@login_required(login_url='/login/')
def instruction(request):
    if request.user.is_authenticated:
        try :
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = Profile()
        if request.method == 'POST':
            check=request.POST.get('check')
            if(check):
                return render(request, 'Users/questionhub.html')
        return render(request, 'Users/Instructions_final.html')
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
    print("Question id:", id)

    context['data'] = Questions.objects.get(id=id)
    print("contexr[data] id:", context['data'].id)
    questions = Questions.objects.all()
    current_user = request.user
    us = Profile.objects.get(user=current_user)
    submissions = Submission.objects.filter(user=current_user.id, quesID=id).order_by('-subScore')
    if request.method == 'POST':
        totsub = Questions.objects.get(pk=id).totalSubmision + 1
        Questions.objects.filter(pk=id).update(totalSubmision=totsub)
        return code_input(request,context['data'].id)

    return render(request,'Users/cp_style.html',context={'user':us,'questions' : questions,'context':context,'submissions':submissions,'code':''})
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
    que = Questions.objects.get(pk=qn)
    print("qn:",qn)
    lang = request.POST.get('lang')

    try:
        mul_que = multipleQues.objects.get(user=user.user, que=que)
        attempts = mul_que.attempts
    except:
        attempts = 1



    response_data = {}
    codeFile = 'questions/usersub/{}/question{}/question{}.{}'.format(username, str(int(qn)-1),int(attempts)-1,  lang)
    BASE_DIR=os.getcwd() + '/Sandboxing/include/'
    try:
        f = open(codeFile, "r")
        txt = f.read()
        f.close()
    except FileNotFoundError:
        pass

    if lang == 'cpp' or lang=='c':
        try:
            header_file = '#include "{}sandbox.h"\n'.format(BASE_DIR)
            parts = txt.split(header_file)
            aftermain = parts[1]
            newpart=aftermain.split("install_filters();")
            aftermain=newpart[0]+newpart[1]
        except:
            aftermain = ""
            pass
    else:
        try:
            parts = txt.split("import sandbox")
            aftermain = parts[1]

        except:
            aftermain = ""
            pass

    txt=aftermain
    response_data["txt"] = txt
    return JsonResponse(response_data)

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