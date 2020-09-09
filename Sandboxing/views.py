from typing import Dict

from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os
from resource import *

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


def compileAndRun(request, qno=None,testcase=None):
    defaultDir = os.getcwd()
    os.chdir("questions/")
    with open("standard/output/question1/output1.txt", "r") as idealOutput, open("usersub/newuser/question1/output.txt",
                                                                                 "w+") as userOutput, open(
            "standard/input/question1/input1.txt", "r") as idealInput, open("usersub/newuser/question1/error.txt",
                                                                            "w+") as e:
        os.chdir("usersub/newuser/question1/")  # CHANGE DIR BASED ON USERNAME AND QUESTION
        try:
            a = subprocess.run(["g++", "question1.cpp"], stderr=e)
            if (a.returncode == 0):
                p = subprocess.run(["./a.out"], stdin=idealInput, stdout=userOutput, stderr=e,
                                   preexec_fn=imposeLimits(qno,testcase))
                # p.wait()
                userOutput.seek(0)
                o1 = userOutput.readlines()
                o2 = idealOutput.readlines()
                if (o1 == o2):
                    os.chdir(defaultDir)
                    return HttpResponse("SUCCESS")
                else:
                    os.chdir(defaultDir)
                    return HttpResponse("FAILED")
            os.chdir(defaultDir)
            return HttpResponse("FAILED")
        except:
            return HttpResponse("ERROR")
