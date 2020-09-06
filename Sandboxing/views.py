from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os

# Create your views here.

def compileAndRun(request):
    defaultDir = os.getcwd()
    os.chdir("questions/") # change dir based on username and question
    with open("standard/output/question1/output1.txt", "r") as idealOutput, open("usersub/newuser/question1/output.txt", "r+") as userOutput, open("standard/input/question1/input1.txt", "r") as idealInput, open("usersub/newuser/question1/error.txt", "w+") as e:
        os.chdir("usersub/newuser/question1/")
        a = subprocess.run(["g++", "question1.cpp"], stderr=e)
        if (a.returncode == 0):
            p = subprocess.run(["./a.out"], stdin=idealInput, stdout=userOutput, stderr=e)
            userOutput.seek(0)
            o1 = userOutput.readlines()
            o2 = idealInput.readlines()
            if (o1 == o2):
                os.chdir(defaultDir)
                return HttpResponse("SUCCESS")
            else:
                os.chdir(defaultDir)
                return HttpResponse("FAILED")
        os.chdir(defaultDir)
        return HttpResponse("FAILED")
    return HttpResponse("ERROR")