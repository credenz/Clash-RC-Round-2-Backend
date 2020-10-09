from typing import Dict

from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os
from resource import *
import datetime
from Users import models
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
    pathquota = 'description/question{}/quota{}.txt'.format(qno, test_case_no)
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


def compile(username, qno, lang):
    with open(BASE_DIR + USER_DIR.format(username, qno) + "error.txt".format(qno), "w+") as e:
        arg1 = arg2 = arg3 = arg4 = ''
        if lang == 'c':
            arg1 = 'gcc'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.c'.format(qno)
            arg3 = '-o'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'.format(qno)
        elif lang == 'cpp':
            arg1 = 'g++'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.cpp'.format(qno)
            arg3 = '-o'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'.format(qno)
        elif lang == 'py':
            arg3 = 'python3'
            arg4 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.py'.format(qno)
        compileCode = [arg1, arg2, arg3, arg4]
        try:
            if lang != 'py':
                a = subprocess.run(compileCode, stderr=e)
                return Return_codes[a.returncode]
        except:
            return Return_codes[1]


def run(username, qno, testcase, lang):
    with open(BASE_DIR + STATIC_FILES_DIR.format("output", qno) + "output{}.txt".format(testcase), "r") as idealOutput, open(BASE_DIR + USER_DIR.format(username, qno) + "output.txt",
                                                                                 "r+") as userOutput, open(
            BASE_DIR + STATIC_FILES_DIR.format("input", qno) + "input{}.txt".format(testcase), "r") as idealInput, open(BASE_DIR + USER_DIR.format(username, qno) + "error.txt".format(qno),
                                                                            "w+") as e:
        arg1 = arg2 = ''
        if lang == 'c':
            arg1 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'.format(qno)
        elif lang == 'cpp':
            arg1 = BASE_DIR + USER_DIR.format(username, qno) + 'a.out'.format(qno)
        elif lang == 'py':
            arg1 = 'python3'
            arg2 = BASE_DIR + USER_DIR.format(username, qno) + 'question{}.py'.format(qno)
        if lang == 'py':
            runCode = [arg1, arg2]
        else:
            runCode = [arg1]
        try:
            userOutput.truncate(0) # EMPTY OUTPUT FILE TO PREVENT UNNECESSARY CONTENT FROM PREVIOUS RUNS.
            p = subprocess.run(runCode, stdin=idealInput, stdout=userOutput, stderr=e, preexec_fn=imposeLimits())
            userOutput.seek(0)
            o1 = userOutput.readlines()
            o2 = idealOutput.readlines()
            if (o1 == o2):
                return Return_codes[0]
            print(p.returncode)
            return Return_codes[p.returncode]
        except:
            return Return_codes[159]