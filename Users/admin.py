from django.contrib import admin
from .models import Profile, Questions, Submissions
# Register your models here.
myModel = [Profile, Questions, Submissions]
admin.site.register(myModel)