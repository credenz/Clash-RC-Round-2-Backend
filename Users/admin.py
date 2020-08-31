from django.contrib import admin
<<<<<<< HEAD
from .models import Profile, Question, Submissions
# Register your models here.
myModel = [Profile, Question, Submissions]
=======
from .models import Profile, Questions, Submissions
# Register your models here.
myModel = [Profile, Questions, Submissions]
>>>>>>> 9ef0b6f714148c3cc847ac5b2ee48f6d17df6b4b
admin.site.register(myModel)