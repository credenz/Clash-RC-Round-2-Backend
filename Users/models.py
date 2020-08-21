from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your models here.
class UserInfo(models.Model):
	#levels for users
	#this we will use from round 1 people only right now let it be for dummy data
	Beginner = 'B'
	Intermediate = 'I'
	Expert = 'E'
	
	groups = [(Beginner, 'Beginner'), (Intermediate, 'Intermediate'), (Expert, 'Expert')]
	

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	phonenumber = models.IntegerField()
	group = models.CharField(max_length = 1, choices = groups, default = Beginner)


	def __str__(self):
		return self.user.username

class Questions(models.Model):
	fs = FileSystemStorage(location = './Questions')
	fs2 = FileSystemStorage(location = './Questions/Input')
	fs3 = FileSystemStorage(location = './Questions/Output')
	question = models.FileField(storage = fs)
	consoleinput = models.FileField(storage = fs2)
	consoleoutput = models.FileField(storage = fs2)



class Responses(models.Model):
	def __init__(self):
		#check file extension and send to respective compiler

    Python = '.py'
	Cpp = '.cpp'
	C = '.c'
	Java = '.java'
	lang = [(Python, 'python'), (Cpp, 'cpp'), (C, 'C'), (Java, 'Java')]
	
	fs4 = FileSystemStorage(location = './Responses')
	user1 = models.ForiegnKey(UserInfo, on_delete = models.CASCADE)
	#language = models.CharField(max_length = 5, choices = lang, default = Python) <--- just to use in init not storing in db
	response = models.FileField(storage = fs4)
	questions = models.ForiegnKey(Questions, on_delete = models.CASCADE)



