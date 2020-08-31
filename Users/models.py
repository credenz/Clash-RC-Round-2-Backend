from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    totalScore = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='example@gmail.com')
    phone = models.CharField(max_length=10)
    # timer = models.TimeField(default='00:00') # about this not sure will be required or not.
    # def_lang = models.CharField(max_length=5, default='cpp')
    # cur_lang = models.CharField(max_length=3, default='cpp') # maybe if he chooses to submit current question in any other lang
    college = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.user.username


class Questions(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=10000)
    totalSubmission = models.IntegerField(default=0)
    SuccessfulSubmission = models.IntegerField(default=0)
    accuracy = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.description


class TestCase(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
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
	user1 = models.ForiegnKey(Profile, on_delete = models.CASCADE)
	#language = models.CharField(max_length = 5, choices = lang, default = Python) <--- just to use in init not storing in db
	response = models.FileField(storage = fs4)
	questions = models.ForiegnKey(Questions, on_delete = models.CASCADE)'''


class Submissions(models.Model):
    languages = [('c', 'C'), ('cpp', 'C++'), ('py', 'Python')]

    quesID = models.ForeignKey(Questions, on_delete=models.CASCADE)  # as we are going to keep it as 1,2,3,4,5,6
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    codeLang = models.CharField(max_length=3, choices=languages)
    submission = models.FileField(upload_to='./responses', max_length=100)
    # submittedCode = models.FilePathField
    # testResult = models.JSONField() or HStoreField (django.contrib.postgres required) or ArrayField --> TBD
    submissionTime = models.DateTimeField(auto_now=True)
    score = models.IntegerField()
    latestSubTime = models.TimeField(default='00:00')