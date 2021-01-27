from django.db import models
from django.contrib.auth.models import User


# from django.core.files.storage import FileSystemStorage
# import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(default='example@gmail.com')
    def_lang = models.CharField(max_length=5, default='cpp')
    college = models.CharField(blank=True, max_length=255)
    totalScore = models.IntegerField(default=0)
    category = models.CharField(default='junior', max_length=6)
    cheatcounter=models.IntegerField(default=3)

    # timer = models.TimeField(default='00:00') # about this not sure will be required or not.
    # cur_lang = models.CharField(max_length=3, default='cpp') # maybe if he chooses to submit current question in any other lang

    def __str__(self):
        return self.user.username


class Questions(models.Model):
    quesTitle = models.CharField(max_length=255)
    quesDesc = models.TextField()
    constraints = models.TextField(default="NA")
    explanation = models.TextField(default="NA")
    iformat = models.TextField(default="NA")
    oformat = models.TextField(default="NA")
    sampleInput = models.TextField(default="NA")
    sampleOutput = models.TextField(default="NA")
    testcases = models.IntegerField(default=2)  # REMEMBER TO CHANGE IT TO ZERO
    totalSubmision = models.IntegerField(default=0)
    SuccessfulSubmission = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)
    category_tag = models.CharField(default='junior', max_length=6)

    def __str__(self):
        return self.quesTitle + '-' + self.quesDesc

    def IDNumber(self):
        return self.pk


class multipleQues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    que = models.ForeignKey(Questions, on_delete=models.CASCADE)
    scoreQuestion = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quesID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000)
    attempt = models.IntegerField(default=0)  # Current Attempt
    out = models.IntegerField(default=0)
    subStatus = models.CharField(default='NA', max_length=5)  # four type of submission status(WA, PASS, TLE, CTE)
    subTime = models.CharField(default='', max_length=50)
    subScore = models.IntegerField(default=0)
    correctTestCases = models.IntegerField(default=0)
    TestCasesPercentage = models.IntegerField(default=0)
