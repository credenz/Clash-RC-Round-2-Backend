from typing import Dict

from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os
from resource import *
import datetime
from Users import models
# Create your views here.

def quotais(qno, test_case_no):
    pathquota = 'questions/standard/description/question{}/quota{}.txt'.format(qno, test_case_no)
    quotafile = open(pathquota)
    data = quotafile.readlines()
    memlimit = data[0].strip()
    time = data[1].strip()
    time = int(time)
    memlimit = int(memlimit)
    limits = {'time': time, 'memlimit': memlimit, }
    return limits


def imposeLimits(qno,tc):
    limit=quotais(qno,tc)
    setrlimit(RLIMIT_AS, (limit['memlimit'], limit['memlimit']))
    setrlimit(RLIMIT_CPU, (limit['time'], limit['time']))
    # setrlimit(RLIMIT_RTTIME, (1, 1)) # WILL LIMIT CPU TIME FOR THE PROCESS


def compileAndRun(username, qno,testcase, lang):
    res = {
        'compiled': 'FAIL',
        'testcase': 'FAIL'
    }
    defaultDir = os.getcwd()
    os.chdir("questions/")
    with open("standard/output/question{}/output{}.txt".format(qno,testcase), "r") as idealOutput, open("usersub/newuser/question{}/output.txt".format(qno),
                                                                                 "r+") as userOutput, open(
            "standard/input/question{}/input{}.txt".format(qno,testcase), "r") as idealInput, open("usersub/newuser/question{}/error.txt".format(qno),
                                                                            "w+") as e:
        os.chdir("usersub/{}/question{}/".format(username, qno))  # CHANGE DIR BASED ON USERNAME AND QUESTION
        arg1 = arg2 = arg3 = arg4 = ''
        if lang == 'c':
            arg1 = 'gcc'
            arg2 = 'question{}.c'.format(qno)
            arg3 = './a.out'
        elif lang == 'cpp':
            arg1 = 'g++'
            arg2 = 'question{}.cpp'.format(qno)
            arg3 = './a.out'
        elif lang == 'py':
            arg3 = 'python3'
            arg4 = 'question{}.py'.format(qno)
        compileCode = [arg1, arg2]
        runCode = [arg3, arg4]
        compiled = True
        try:
            if lang != 'py':
                a = subprocess.run(compileCode, stderr=e)
                if a.returncode != 0:
                    compiled = False
            if (compiled):
                res['compiled'] = 'SUCCESS'
                userOutput.truncate(0) # EMPTY OUTPUT FILE TO PREVENT UNNECESSARY CONTENT FROM PREVIOUS RUNS.
                p = subprocess.run(runCode, stdin=idealInput, stdout=userOutput, stderr=e,
                                   preexec_fn=imposeLimits(qno,testcase))
                # p.wait()
                userOutput.seek(0)
                o1 = userOutput.readlines()
                o2 = idealOutput.readlines()
                if (o1 == o2):
                    os.chdir(defaultDir)
                    res['testcase'] = 'SUCCESS'
                    return res
                else:
                    os.chdir(defaultDir)
                    res['testcase'] = 'FAIL'
                    return res
            os.chdir(defaultDir)
            return res
        except:
            res['compiled'] = 'FAIL'
            return res
