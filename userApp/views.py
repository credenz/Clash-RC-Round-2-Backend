from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Question, Submission, UserProfile, MultipleQues
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
import datetime
import os, re
import json
from judgeApp.views import exec_main

start = 0
end_time = 0
duration = 0
starttime = datetime.datetime(2021, 2, 1, 18, 0,0)
print(start)
print(datetime.datetime.now())
flag = False
end = "Feb 14, 2021 00:00:00"
path_usercode = 'data/usersCode/'
standard = 'data/standard'

NO_OF_QUESTIONS = 6
NO_OF_TEST_CASES = 6

#this function needs to be activated
# @login_required(login_url='/')
# def cheatcounter(request):
#     usern = UserProfile.objects.filter(user=request.user)[0]
#     data = {'cheatcounter': usern.cheatcounter}
#     print("outside post")
#     if(request.method=='POST'):
#         print("inside post")
#         usern.cheatcounter-=1
#         usern.save()
#         return JsonResponse(data)
#     elif(request.method=='GET'):
#         return JsonResponse(data)

def hardlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

@login_required(login_url='/')
def leadsus(request):
    return render(request, 'userApp/ldb.html',context={'endtime':end})

def waiting(request):
    if request.user.is_authenticated:
        return redirect(reverse("questionHub"))
    else:
        global flag
        if  flag:
            return render(request, 'userApp/waiting.html')
        else:
            now = datetime.datetime.now()
            global start
            if now != start:
                return redirect(reverse("signup"))
            elif now > start:
                return redirect(reverse("signup"))
            else:
                return render(request, 'userApp/waiting.html')


def timer(request):
    if request.method == 'GET':
        return render(request, 'userApp/timer.html')

    elif request.method == 'POST':
        global starttime, start
        global end_time
        global duration
        global flag
        flag = True
        duration = 7200  # request.POST.get('duration')
        start = datetime.datetime.now()
        start = start + datetime.timedelta(0, 15)
        time = start.second + start.minute * 60 + start.hour * 60 * 60
        starttime = time
        end_time = time + int(duration)
        return HttpResponse(" time is set ")


def calculate():
    time = datetime.datetime.now()
    nowsec = (time.hour * 60 * 60) + (time.minute * 60) + time.second
    global starttime
    global end_time
    diff = end_time - nowsec
    if nowsec < end_time:
        return diff
    else:
        return 0


def signup(request):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user = UserProfile()
    else:
        if request.method == 'POST':
            try:
                username = request.POST.get('username')
                username = username.replace(' ', '_')
                password = request.POST.get('password')
                name1 = request.POST.get('name1')
                phone1 = request.POST.get('phone1')
                email1 = request.POST.get('email1')
                junior = request.POST.get('optradio')

                junior = True if (junior == 'fe' or junior == 'se') else False

                if username == "" or password == "":
                    return render(request, 'userApp/login.html')
                print(junior)
                user = User.objects.create_user(username=username, password=password)
                userprofile = UserProfile(user=user, name1=name1,phone1=phone1, email1=email1,
                                           junior=junior)
                userprofile.save()
                # print(username)
                os.system('mkdir {}/{}'.format(path_usercode, username))
                login(request, user)
                return redirect(reverse("instructions"))

            except IntegrityError:
                return render(request, 'userApp/login.html')

            except HttpResponseForbidden:
                return render(request, 'userApp/login.html')

        elif request.method == 'GET':
            return render(request, "userApp/login.html")

    return HttpResponseRedirect(reverse("login"))



def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("questionHub"))
    if request.method == 'POST':
        username = request.POST.get('user')
        pass_e = request.POST.get('auth_pass')
        user = authenticate(request, username=username, password=pass_e)

        if(UserProfile.objects.filter(user=user).exists()):
            cheatcheck=UserProfile.objects.filter(user=user)[0]
        if user is not None and cheatcheck.cheatcounter>0:
            login(request, user)
            return render(request, 'userApp/Instructions_final.html')
        elif user is not None and cheatcheck.cheatcounter<=0:
            messages.error(request, 'You went against the rules and switched tabs. You are now not allowed to participate further.')
        else:
            messages.error(request, 'username or password is incorrect.')
            # return render (request, 'Users/LoginPage.html', context={'error' : "Login Failed! Enter the username and password correctly"})

    return render(request, 'userApp/LoginPage.html')


@login_required(login_url='/')
def questionHub(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return signup(request)

        all_questions = Question.objects.all()
        all_users = User.objects.all()
        tickcross=[0,0,0,0,0,0,0]

        for que in all_questions:
            try:
                mul_que = MultipleQues.objects.get(user=request.user, que=que)
                print(tickcross)
                if(mul_que.scoreQuestion==100):
                    tickcross[que.id]=1
                    print(tickcross)
                elif(mul_que.scoreQuestion==0):
                    tickcross[que.id] = 2
                    print(tickcross)
            except MultipleQues.DoesNotExist:
                pass
            try:
                que.accuracy = round((que.totalSuccessfulSub * 100/que.totalSub), 1)
            except ZeroDivisionError:
                que.accuracy = 0
        print(tickcross)
        json.dumps(tickcross)
        var = calculate()
        if var != 0:
            return render(request, 'userApp/questionhub.html', context={'questions': all_questions,'tickcross':tickcross,'endtime': end})
        else:
            return render(request, 'userApp/questionhub.html', context={'questions': all_questions,'tickcross':tickcross, 'endtime': end})
    else:
        return HttpResponseRedirect(reverse("questionHub"))


def change_file_content(content, extension, code_file):
    if extension != 'py':
        sandbox_header = '#include"../../../include/sandbox.h"\n'
        try:
            # Inject the function call for install filters in the user code file
            # Issue with design this way (look for a better solution (maybe docker))
            # multiple main strings
            before_main = content.split('main')[0] + 'main'
            after_main = content.split('main')[1]
            index = after_main.find('{') + 1
            main = before_main + after_main[:index] + 'install_filters();' + after_main[index:]
            print(code_file)
            with open(code_file, 'w+') as f:
                f.write(sandbox_header)
                f.write(main)
                f.close()

        except IndexError:
            with open(code_file, 'w+') as f:
                f.write(content)
                f.close()

    else:
        with open(code_file, 'w+') as f:
            f.write('import temp\n')
            f.write(content)
            f.close()

@login_required(login_url='/')
def codeSave(request, qn):
    if request.user.is_authenticated:  # Check Authentication
        caselist=[False,False,False,False,False,False]
        questions = Question.objects.all()
        if request.method == 'POST':
            que = Question.objects.get(pk=qn)
            user = request.user
            username= user.username

            content = request.POST.get('user_code')
            extension = request.POST.get('ext')

            user_profile = UserProfile.objects.get(user=user)
            user_profile.choice = extension

            temp_user = UserProfile.objects.get(user=user)
            temp_user.qid = qn
            temp_user.lang = extension
            temp_user.save()

            try:
                    mul_que = MultipleQues.objects.get(user=user, que=que)

            except MultipleQues.DoesNotExist:
                mul_que = MultipleQues(user=user, que=que)
                mul_que.save()

            att = mul_que.attempts

            user_question_path = '{}/{}/question{}/'.format(path_usercode, username, qn)

            if not os.path.exists(user_question_path):
                os.system('mkdir ' + user_question_path)

            code_file = user_question_path + "code{}.{}".format(att, extension)

            content = str(content)

            change_file_content(content, extension, code_file)

            testcase_values = exec_main(
                username=username,
                qno=qn,
                custominput="false",
                attempts=att,
                lang=extension,
            )
            print(type(testcase_values))

            code_f = open(code_file, 'w+')
            code_f.seek(0)
            code_f.write(content)
            code_f.close()

            now_time = datetime.datetime.now()
            now_time_sec = now_time.second + now_time.minute * 60 + now_time.hour * 60 * 60
            global starttime
            st = starttime.second + starttime.minute * 60 + starttime.hour * 60 * 60
            submit_Time = now_time_sec - st
            print(submit_Time)

            hour = submit_Time // (60 * 60)
            val = submit_Time % (60 * 60)
            min = val // 60
            sec = val % 60

            subTime = '{}:{}:{}'.format(hour, min, sec)

            # print(subTime)
            # print("submit time" + str(submit_Time))

            sub = Submission(code=content, user=user, que=que,qid=int(qn), attempt=att, subTime=subTime)
            sub.save()

            mul_que.attempts += 1
            mul_que.save()

            error_text = ""

            epath = path_usercode + '/{}/question{}/error.txt'.format(username, qn)

            if os.path.exists(epath):
                ef = open(epath, 'r')
                error_text = ef.read()
                if(extension!="py"):
                    error_text = re.sub('data/.*?:', '', error_text)  # regular expression
                    error_text = re.sub('install_filters\(\);', '', error_text)
                else:
                    error_text=re.sub('File(.*?)(\.cpp:|\.py",|\.c:)','',error_text)

                ef.close()

            no_of_pass = 0
            iter=0
            tle=0
            wa=0
            ac=0
            cte=0
            for i in testcase_values:
                if i == 'AC':
                    no_of_pass += 1
                    caselist[iter]=True
                    ac+=1

                elif(i=='TLE'):
                    tle+=1
                elif(i=='WA'):
                    wa+=1
                elif(i=="CTE"):
                    cte+=1
                iter+=1

            # print(error_text)

            sub.correctTestCases = no_of_pass
            sub.TestCasesPercentage = (no_of_pass / NO_OF_TEST_CASES) * 100
            sub.save()

            status = ''  # overall Status
            if(ac==NO_OF_TEST_CASES):
                status += 'AC'
            elif(wa>0 and tle==0 and cte==0):
                status+='WA'
            elif(tle>0 and cte==0):
                status+='TLE'
            else:
                status+="CTE"

            if mul_que.attempts == 1:
                que.totalSub += 1

            if status == 'AC':
                if mul_que.scoreQuestion == 0:
                    user_profile.totalScore += 100
                    user_profile.correctly_solved +=1
                    que.totalSuccessfulSub += 1
                mul_que.scoreQuestion = 100
                user_profile.save()
                mul_que.save()

            que.save()
            var = calculate()

            data = {
                'testcase': testcase_values,
                'error': error_text,
                'status': status,
                'score': mul_que.scoreQuestion,
                'time': var,
                'list': json.dumps(caselist),
                'endtime':end,
            }

            if var != 0:
                return render(request, 'userApp/testcases_latest.html', context=data)
            else:
                return render(request, 'userApp/testcases_latest.html', context=data)

        elif request.method == 'GET':
            que = Question.objects.get(pk=qn)
            user_profile = UserProfile.objects.get(user=request.user)
            user = request.user

            var = calculate()
            if var != 0:
                return render(request, 'userApp/cp_style.html', context={'questions':questions,'question': que, 'user': user, 'time': var,
                                                                           'total_score': user_profile.totalScore,
                                                                           'question_id': qn, 'code': '',
                                                                           'junior': user_profile.junior,'endtime':end})
            else:
                return render(request, 'userApp/cp_style.html', context={'questions':questions,'question': que, 'user': user, 'time': var,
                                                                           'total_score': user_profile.totalScore,
                                                                           'question_id': qn, 'code': '',
                                                                           'junior': user_profile.junior,'endtime':end})
    else:
        return HttpResponseRedirect(reverse("questionHub"))

@login_required(login_url='/')
def instructions(request):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user = UserProfile()
        if user.flag:
            return HttpResponseRedirect(reverse('questionHub'))
        if request.method == "POST":
            return HttpResponseRedirect(reverse('questionHub'))
        return render(request, 'userApp/Instructions_final.html')
    else:
        return HttpResponseRedirect(reverse("questionHub"))

@login_required(login_url='/')
def leader(request):
    if request.user.is_authenticated:
        data = {}
        current_user = UserProfile.objects.get(user=request.user)
        initials=str(current_user.user)
        initials=initials[0:2]
        status=(current_user.correctly_solved*100)//6
        object = UserProfile.objects.order_by("-totalScore", "latestSubTime")
        current_rank=0
        for user in object:
            current_rank += 1
            if str(user.user) == str(request.user.username):
                break
        for user in UserProfile.objects.order_by("-totalScore"):
            l = []
            for n in range(1, 7):
                que = Question.objects.get(pk=n)
                try:
                    mulQue = MultipleQues.objects.get(user=user.user, que=que)
                    l.append(mulQue.scoreQuestion)
                except MultipleQues.DoesNotExist:
                    l.append(0)
            l.append(user.totalScore)
            data[user.user] = l

        sorted(data.items(), key=lambda items: (items[1][6], user.latestSubTime))
        paginator = Paginator(tuple(data.items()), 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        var = calculate()
        if var != 0:
            return render(request, 'userApp/LEADERBOARD.html', context={'dict': data,'status':status,'initials':initials,'username':current_user.user,'rank':current_rank,'score': current_user.totalScore, 'range': range(1, 7, 1),
                                                                        'time': var,'endtime':end,
                                                                        'page_obj': page_obj,
                                                                        'page_range': page_range,})
        else:
            return render(request, 'userApp/LEADERBOARD.html', context={'dict': data,'status':status,'initials':initials,'username':current_user.user,'rank':current_rank,'score': current_user.totalScore, 'range': range(1, 7, 1),
                                                                        'time': var,'endtime':end,
                                                                        'page_obj': page_obj,
                                                                        'page_range': page_range,})

    else:
        return HttpResponseRedirect(reverse("questionHub"))





@login_required(login_url='/')
def submission(request, qn):
    que = Question.objects.get(pk=qn)
    all_submission = Submission.objects.all()

    userQueSub = list()
    submissions = Submission.objects.filter(user=request.user.id, que=qn).order_by(
        'id')
    for i in submissions:
        userQueSub.append(i)
    # var = calculate()
    #
    # if var != 0:
    #     return render(request, 'userApp/submissions.html', context={'allSubmission': userQueSub, 'endtime': end, 'qn': qn})
    # else:
    #     return render(request, 'userApp/submissions.html', context={'allSubmission': userQueSub, 'endtime': end, 'qn': qn})

  # parameter should be the latest submission time for ordering
    questions = Question.objects.all()
    try:
        return render(request, 'userApp/submission.html',
                      context={'error': 'Some error', 'questions': questions, 'submissions': userQueSub,
                               'endtime': end})
    except:
        return render(request, 'userApp/submission.html',
                      context={'error': 'Some error', 'questions': questions, 'submissions': userQueSub,
                               'endtime': end})


def user_logout(request):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return signup(request)
        object = UserProfile.objects.order_by("-totalScore", "latestSubTime")
        rank = 0
        j = 0
        dict = []
        for user in object:
            if rank < 6:
                dict.append(str(user.user))
                rank = rank + 1
            else:
                break

        for user in object:
            j += 1
            if str(user.user) == str(request.user.username):
                break


        print(dict)
        path = path_usercode + user.user.username
        print(path)
        # if os.path.exists(path):
        #     os.system("rm -rf " + path)
        attempts = 0
        for i in range(1,7):
            que = Question.objects.get(pk=i)
            ats=MultipleQues.objects.filter(user=request.user, que=que)
            if ats.exists():
                attempts+=1
        logout(request)

        return render(request, 'userApp/resultpage_1.html', context={'dict': dict,'que_solved': user.correctly_solved,'que_attempted':attempts,'rank': j, 'name': user.user,'initials':str(user.user)[0],
                                                               'score': user.totalScore})
    else:
        return HttpResponseRedirect("/")


def loadBuffer(request):
    user = UserProfile.objects.get(user=request.user)
    username = request.user.username
    qn = request.POST.get('question_no')
    que = Question.objects.get(pk=qn)
    mul_que = MultipleQues.objects.get(user=user.user, que=que)
    attempts = mul_que.attempts
    ext = request.POST.get('ext')
    response_data = {}

    codeFile = path_usercode + '{}/question{}/code{}.{}'.format(username, qn, int(attempts) - 1, ext)
    print(codeFile)
    txt = ""

    try:
        f = open(codeFile, "r")
        txt = f.read()
        f.close()
    except FileNotFoundError:
        print("in error")
        pass

    response_data["txt"] = txt

    return JsonResponse(response_data)


def garbage(request, garbage):
    return HttpResponseRedirect(reverse('login'))


def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'username already exits.'

    return JsonResponse(data)

@login_required(login_url='/')
def view_sub(request,_id, qno=1):
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        sub = Submission.objects.get(id=_id)
        code = sub.code

        # print(code)

        que = Question.objects.get(pk=int(qno))
        user = request.user

        var = calculate()
        questions = Question.objects.all()
        return render(request, 'userApp/cp_style.html', context={'question': que,'questions':questions ,'user': user, 'time': var,
                                                                   'total_score': user_profile.totalScore,
                                                                   'question_id': qno, 'code': code,'endtime':end})
    else:
        return codeSave(request,qno)
        #return HttpResponse("fdshfhsdlkfnlksdjfnlsdnflkdsnflds")


def emergency_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        AdminPass = request.POST.get('admin_password')
        user = authenticate(username=username, password=password)
        if AdminPass == '1234':
            if user.is_active:
                login(request, user)
                return redirect(reverse('questionHub'))
        else:
            return HttpResponse('invalid details')
    else:
        return render(request, 'userApp/emerlogin.html')

@login_required(login_url='/')
def run(request):
    if request.user.is_authenticated:
        response_data = {}
        username = request.user.username
        que_no = request.POST.get('question_no')
        ext = request.POST.get('ext')
        code = request.POST.get('code')
        ici=request.POST.get('isCustomInput')
        ci=request.POST.get('custominput')

        user_question_path = path_usercode + '{}/question{}/'.format(username, que_no)
        code_file_path = user_question_path + 'code.{}'.format(ext)
        if not os.path.exists(user_question_path):
            os.system('mkdir ' + user_question_path)

        if(ici=="true"):
            with open(user_question_path+"custominput.txt",'w+') as cin:
                cin.write(ci)




        code_f = open(code_file_path, 'w+')
        code_f.write(code)
        code_f.close()

        change_file_content(code, ext, code_file_path)

        status = exec_main(
            username=username,
            qno=que_no,
            lang=ext,
            custominput=ici,
            run=True,

        )[0]

        # exp_op_path = standard + "output/question{}/expected_output7.txt".format(que_no)

        op_path = user_question_path + "output7.txt"
        err_path = user_question_path + "error.txt"

        op_f = open(op_path, 'r')
        err_f = open(err_path, 'r')
        # exp_f = open(exp_op_path, 'r')

        errcodes = ['CTE', 'RTE', 'AT', 'TLE']

        if status in errcodes:
            if status == "CTE":
                err_text = err_f.read()
                if(ext!="py"):
                    err_text = re.sub('data/.*?:', '', err_text)  # regular expression
                    err_text = re.sub('install_filters\(\);', '', err_text)
                else:
                    err_text=re.sub('File(.*?)(\.cpp:|\.py",|\.c:)','',err_text)
                actual = err_text
            else:
                actual = ""
        else:
            if status == 'AC':
                status = 'OK'
            actual = op_f.read()

        op_f.close()
        err_f.close()

        # expected = exp_f.read()

        # print(expected, actual)

        response_data["status"] = status
        response_data["expected"] = 0
        response_data["actual"] = actual
        print(actual)

        return JsonResponse(response_data)

    else:
        return HttpResponseRedirect(reverse(""))
