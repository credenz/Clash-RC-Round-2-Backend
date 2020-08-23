from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	totalScore = models.IntegerField(default=0)
	name = models.CharField(max_length=100)
	#email = models.EmailField(default='example@gmail.com')
	#phone = models.CharField(max_length=10)
	#timer = models.TimeField(default='00:00') # about this not sure will be required or not.
	def_lang = models.CharField(max_length=5, default='cpp')
	cur_lang = models.CharField(max_length=3, default='cpp') # maybe if he chooses to submit current question in any other lang


    def __str__(self):
		return self.user.username

class Question(models.Model):
	#fs = FileSystemStorage(location = './Questions')
	#fs2 = FileSystemStorage(location = './Questions/Input')
	#fs3 = FileSystemStorage(location = './Questions/Output')
	#question = models.FileField(storage = fs)
	#consoleinput = models.FileField(storage = fs2)
	#consoleoutput = models.FileField(storage = fs3)
	def __init__(self):
		path = "%dummypath%"
		basename = "question_"
		os.makedirs("{}{}{}".format(path, basename, self.id))

    questiontitle = models.CharField(max_length = 20)

	def __str__(self):
		return self.questiontitle

class TestCase(models.Model):
	question = models.OneToOneField(Questions, on_delete = models.CASCADE)
	timerequired = models.IntegerField()
	spacerequired = models.IntegerField()

    





'''class Responses(models.Model):
	#def __init__(self):
		#check file extension and send to respective compiler
		#also add validation code here

	Python = '.py'
	Cpp = '.cpp'
	C = '.c'
	Java = '.java'
	lang = [(Python, 'python'), (Cpp, 'cpp'), (C, 'C'), (Java, 'Java')]

	fs4 = FileSystemStorage(location = './Responses')
	user1 = models.ForiegnKey(UserInfo, on_delete = models.CASCADE)
	#language = models.CharField(max_length = 5, choices = lang, default = Python) <--- just to use in init not storing in db
	response = models.FileField(storage = fs4)
	questions = models.ForiegnKey(Questions, on_delete = models.CASCADE)'''



