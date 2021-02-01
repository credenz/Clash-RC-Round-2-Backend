from django.contrib import admin
from .models import Question, Submission, UserProfile, MultipleQues

admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(UserProfile)
admin.site.register(MultipleQues)
