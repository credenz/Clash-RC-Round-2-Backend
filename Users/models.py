from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
	#levels for users
	Beginner = 'B'
	Intermediate = 'I'
	Expert = 'E'
	groups = [(Beginner, 'Beginner'), (Intermediate, 'Intermediate'), (Expert, 'Expert')]

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	phonenumber = models.IntegerField()
	group = models.CharField(max_length = 1, choices = groups, default = Beginner)


	def __str__(self):
		return self.user.username

