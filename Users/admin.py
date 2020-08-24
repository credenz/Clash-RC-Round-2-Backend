from django.contrib import admin
from .models import Profile, Question, Submissions
# Register your models here.
myModel = [Profile, Question, Submissions]
admin.site.register(myModel)