from django.contrib import admin
from .models import Profile, Questions, Submission
# Register your models here.
myModel = [Profile, Questions, Submission]
admin.site.register(myModel)