from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os
from resource import *

# Create your views here.

virMem = 10 * 1024 * 1024   # READ AND CHANGE ACCORDING TO QUESTION
timeout = 0.01  # READ AND CHANGE ACCORDING TO QUESTION

def imposeLimits():
    setrlimit(RLIMIT_AS, (virMem, virMem))
    # setrlimit(RLIMIT_RTTIME, (1, 1)) # WILL LIMIT CPU TIME FOR THE PROCESS

def compileAndRun(request):
    defaultDir = os.getcwd()
    os.chdir("questions/")
    with open("standard/output/question1/output1.txt", "r") as idealOutput, open("usersub/newuser/question1/output.txt", "w+") as userOutput, open("standard/input/question1/input1.txt", "r") as idealInput, open("usersub/newuser/question1/error.txt", "w+") as e:
        os.chdir("usersub/newuser/question1/") # CHANGE DIR BASED ON USERNAME AND QUESTION
        try:
            a = subprocess.run(["g++", "question1.cpp"], stderr=e)
            if (a.returncode == 0):
                p = subprocess.run(["./a.out"], stdin=idealInput, stdout=userOutput, stderr=e, preexec_fn=imposeLimits(), timeout=timeout)
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