from typing import Dict

from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os
from resource import *
import re
import datetime
from Users import models
import time
# Create your views here.

Return_codes = {
        0: 'AC',  # Correct ans

        1: 'CTE',  # compile time error

        127: 'CTE', # compile time error

        159: 'SE', # system call did not match 31

        135: 'SE', # bus error 7

        136: 'RTE', # SIGFPE 8

        139: 'RTE', # SIGSEGV (segmentation fault) 11

        137: 'TLE', # SIGKILL (resource overload) 9

        -8: 'RTE',  # SIGFPE (Div by 0)

        -11: 'RTE',  #SIGSEGV

        -9: 'TLE',  # SIGKILL   (Time limit)

        'wa': 'WA',  # Wrong answer
    }

BASE_DIR = os.getcwd() + '/'
STATIC_FILES_DIR = 'questions/standard/{}/question{}/'
USER_DIR = 'questions/usersub/{}/question{}/'


def quotais(qno, test_case_no):
    pathquota = BASE_DIR + 'questions/standard/description/question{}/quota{}.txt'.format(qno, test_case_no)
    quotafile = open(pathquota)
    data = quotafile.readlines()
    memlimit = data[0].strip("\ufeff")
    memlimit = memlimit.strip()
    time = data[1]
    time = int(time)
    memlimit = int(memlimit)
    limits = {'time': time, 'memlimit': memlimit, }
    return limits


def imposeLimits(qno,tc):
    limit=quotais(qno,tc)
    setrlimit(RLIMIT_AS, (limit['memlimit'], limit['memlimit']))
    setrlimit(RLIMIT_CPU, (limit['time'], limit['time']))
    # setrlimit(RLIMIT_RTTIME, (1, 1)) # WILL LIMIT CPU TIME FOR THE PROCESS


def compile(username, qno, attempt, lang):
    with open(BASE_DIR + USER_DIR.format(username, qno) + "error.txt".format(qno), "w+") as e:
        arg1 = arg2 = arg3 = arg4 = ''
        if lang == 'c':
            arg1 = 'gcc'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.c'.format(attempt)
            arg3 = '-o'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'.format(qno)
        elif lang == 'cpp':
            arg1 = 'g++'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.cpp'.format(attempt)
            arg3 = '-o'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'.format(qno)
        elif lang == 'py':
            arg3 = 'python3'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.py'.format(attempt)
        compileCode = [arg1, arg2, arg3, arg4, "-lseccomp"]
        try:
            if lang != 'py':
                a = subprocess.run(compileCode, stderr=e)
                return Return_codes[a.returncode]
        except:
            return Return_codes[1]


def run(username, qno, attempt, testcase, lang):
    with open(BASE_DIR + STATIC_FILES_DIR.format("output", qno) + "output{}.txt".format(testcase), "r") as idealOutput, open(BASE_DIR + USER_DIR.format(username, qno) + "output{}.txt".format(testcase),
                                                                                 "r+") as userOutput, open(
            BASE_DIR + STATIC_FILES_DIR.format("input", qno) + "input{}.txt".format(testcase), "r") as idealInput, open(BASE_DIR + USER_DIR.format(username, qno) + "error.txt",
                                                                            "w+") as e:
        arg1 = arg2 = ''
        if lang == 'c':
            arg1 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'
        elif lang == 'cpp':
            arg1 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'
        elif lang == 'py':
            arg1 = 'python3'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.py'.format(attempt)
        if lang == 'py':
            runCode = [arg1, arg2]
        else:
            runCode = [arg1]
        try:
            userOutput.truncate(0) # EMPTY OUTPUT FILE TO PREVENT UNNECESSARY CONTENT FROM PREVIOUS RUNS.
            # p = subprocess.run(runCode, stdin=idealInput, stdout=userOutput, stderr=e, preexec_fn=imposeLimits(qno, testcase)) # ADD BELOW LINE FOR RESOURCE LIMITS AND REMOVE THIS LINE
            p = subprocess.Popen(runCode, stdin=idealInput, stdout=userOutput, stderr=e, preexec_fn=imposeLimits(qno, testcase))
            p.wait()
            userOutput.seek(0)
            if (p.returncode == -9 or p.returncode == 137):
                return Return_codes[p.returncode]
            o1 = userOutput.read()
            o2 = idealOutput.read().splitlines()
            o1=o1.rstrip()  #to remove excess spaces at end which may occur in o/p to textually match with compiler o/p
            o1=o1.splitlines()
            print("o1: ",o1)

            if (p.returncode == 0):
                if (o1 == o2):
                    return Return_codes[0]
                return Return_codes["wa"]
            return Return_codes[p.returncode]
        except e:
            print(e)
            return Return_codes[159]


def compileCustomInput(username, qno, lang):
    with open(BASE_DIR + USER_DIR.format(username, qno) + "error.txt", "r+") as e:
        arg1 = arg2 = arg3 = arg4 =  arg5 = ''
        if lang == 'c':
            arg1 = 'gcc'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'customInputCode.c'
            arg3 = '-o'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'
            arg5 = '-lseccomp'
        elif lang == 'cpp':
            arg1 = 'g++'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'customInputCode.cpp'
            arg3 = '-o'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'
            arg5 = '-lseccomp'
        compileCode = [arg1, arg2, arg3, arg4, arg5]
        try:
            if lang != 'py':
                a = subprocess.run(compileCode, stderr=e)
                if (a.returncode != 0):
                    e.seek(0)
                    er = re.sub('/home(.*?)(\.cpp:|\.py",|\.c:)', '', e.read())
                    return {'returnCode': Return_codes[a.returncode], 'error': er}
                return {'returnCode': Return_codes[a.returncode]}
        except:
            e.seek(0)
            er = re.sub('/home(.*?)(\.cpp:|\.py",|\.c:)', '', e.read())
            return {'returnCode': Return_codes[159], 'error': er}


def runCustomInput(username, qno, attempt, lang):
    print("inside!!")
    with open(BASE_DIR + USER_DIR.format(username, qno) + "customoutput.txt", "r+") as userOutput, open(BASE_DIR + USER_DIR.format(username, qno) + "error.txt", "w+") as e, open(BASE_DIR + USER_DIR.format(username, qno) + "input.txt","r") as input:
        arg1 = arg2 = ''

        if lang == 'c':
            arg1 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'
        elif lang == 'cpp':
            arg1 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'
        elif lang == 'py':
            arg1 = 'python3'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'customInputCode.py'
        print("161 here")
        if lang == 'py':
            runCode = [arg1, arg2]
        else:
            runCode = [arg1]
        try:
            #userOutput.truncate(0) # EMPTY OUTPUT FILE TO PREVENT UNNECESSARY CONTENT FROM PREVIOUS RUNS.
            print("above subprocess")
            p = subprocess.Popen(runCode, stdin=input, stdout=userOutput, stderr=e, preexec_fn=imposeLimits(qno, 1))
            print("below subprocess")
            p.wait()
            print("returncode: ", p.returncode)
            userOutput.seek(0)
            if (p.returncode == -9 or p.returncode == 137):
                return {'returnCode': Return_codes[p.returncode], 'error': "TLE Error!!"}

            s=userOutput.read() #string s contains the output of custom input
            print("returncode: ",p.returncode)
            print("s: ", s)

            if (p.returncode != 0):
                e.seek(0)
                er = re.sub('/home(.*?)(\.cpp:|\.py",|\.c:)', '', e.read())
                print(er)
                return {'returnCode': Return_codes[p.returncode], 'error': er}
            return {'returnCode': Return_codes[p.returncode], 'output': s}
        except:
            e.seek(0)
            er = re.sub('/home(.*?)(\.cpp:|\.py",|\.c:)', '', e.read())
            return {'returnCode': Return_codes[159], 'error': er}


