from django.db import models
from django.contrib.auth.models import User
# from django.core.files.storage import FileSystemStorage
# import os


class Profile(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	totalScore = models.IntegerField(default=0)
	name = models.CharField(max_length=100)
	email = models.EmailField(default='example@gmail.com')
	phone = models.CharField(max_length=10)
	# timer = models.TimeField(default='00:00') # about this not sure will be required or not.
	def_lang = models.CharField(max_length=5, default='cpp')
	# cur_lang = models.CharField(max_length=3, default='cpp') # maybe if he chooses to submit current question in any other lang
	college = models.CharField(blank=True, max_length=255)

	def __str__(self):
		return self.user.username



class Questions(models.Model):
	quesTitle = models.CharField(max_length=255)
	quesDesc = models.TextField()
	sampleInput = models.TextField()
	sampleOutput = models.TextField()

	def __str__(self):
		return self.quesTitle + '-' + self.quesDesc

	def IDNumber(self):
		return self.pk


class Submissions(models.Model):
	languages = [('c', 'C'), ('cpp', 'C++'), ('py', 'Python')]

	quesID = models.ForeignKey(Questions, on_delete=models.CASCADE) #as we are going to keep it as 1,2,3,4,5,6
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	codeLang = models.CharField(max_length=3, choices=languages)

	# submission = models.FileField(upload_to='./responses', max_length=100)
	# submittedCode = models.FilePathField
	# testResult = models.JSONField() or HStoreField (django.contrib.postgres required) or ArrayField --> TBD

	# To keep a track of the submissions made by a user for a particular question
	# See 'submit' and 'codeInput' views for usage of this attribute
	attemptID = models.IntegerField(default=0)

	submissionTime = models.DateTimeField(auto_now=True)
	score = models.IntegerField()
	latestSubTime = models.TimeField(default='00:00')
