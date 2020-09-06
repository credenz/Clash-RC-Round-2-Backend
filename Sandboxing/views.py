from django.shortcuts import render
import subprocess
import os

# Create your views here.

def compileAndRun(request):
    
    path=os.join("questions/usersub/newuser/question1")
    with open("questions/standard/output/question1/output1.txt", "r+") as idealOutput, open('questions/usersub/newuser/question1/output.txt', 'r') as userOutput, open("questions/standard/input/question1/input1.txt", "r") as input, open("questions/usersub/newuser/question1/error.txt", "w") as e, open(""):
        a = subprocess.run(["g++", "question1.cpp"], stderr=e)
        if (a.returncode == 0):
            p = subprocess.run(["./a.out"], stdin=i, stdout=o, stderr=e, shell=True)
            o.seek(0)
            o1 = o.readlines()
            o2 = t.readlines()
            if (o1 == o2):
                return render(request, "SUCCESSFUL")
            else:
                print("F")
                return render(request, "FAILED")