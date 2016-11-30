from __future__ import unicode_literals

from django.db import models
# User class for built-in authentication module
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class Plan(models.Model):
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	plan_date = models.CharField(max_length=20, default='not decided yet', blank= True)
	name = models.CharField(max_length=200, default='not decided yet', blank= True)
	create_date = models.DateField(auto_now=True)
# several events may belong to one plan
class Event(models.Model):
	plan = models.ForeignKey(Plan, related_name='events', on_delete=models.CASCADE)
	period = models.CharField(max_length=200, default='', blank= True)
	activity = models.CharField(max_length=200, default='', blank= True)
	destination = models.CharField(max_length=200, default='', blank= True)
	url = models.CharField(max_length=200, default='', blank= True)
	img = models.CharField(max_length=1000, default='', blank= True)
	order = models.IntegerField(default=0, blank= True)
# detailed informatino of user
class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	first_name = models.CharField(max_length=420, default='', blank= True)
	last_name = models.CharField(max_length=420, default='', blank= True)
	age = models.IntegerField(default=0, blank= True)
	bio = models.CharField(max_length=420, default='', blank= True)
	interest = models.CharField(max_length=420, default='', blank= True)
	gender = models.CharField(max_length=20, default='', blank= True)
	region = models.CharField(max_length=20, default='', blank= True)
	picture = models.ImageField(upload_to="ins", blank = True)
	# rate = 

# the blog user posted on the web, several blogs can belong to one user
class Blog(models.Model):
	title = models.CharField(max_length=50)
	content = models.CharField(max_length=500)
	user = models.ForeignKey(User)
	profile = models.ForeignKey(UserProfile, null=True)
	time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.blog

	
# several comment may belong to one plan, to one user
class Comment(models.Model):
	plan = models.ForeignKey(Plan, related_name='comments', on_delete=models.CASCADE)
	author = models.ForeignKey(User)
	author_profile = models.ForeignKey(UserProfile, null=True)
	content = models.CharField(max_length=420)
	time = models.DateTimeField(auto_now=True)
# user can review on other user
class Review(models.Model):
	reviewed = models.ForeignKey(User, related_name='reviews', null=True)
	reviewer = models.ForeignKey(User, null=True)
	reviewer_profile = models.ForeignKey(UserProfile, null=True)
	content = models.CharField(max_length=420)
	time = models.DateTimeField(auto_now=True)

