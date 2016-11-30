from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator
#helper function
from mimetypes import guess_type

from travelapp.models import *
from travelapp.forms import *

import urllib2
import json

@login_required
def index(request):
	context = {}

	if request.method == 'GET':
		context['form'] = SearchForm()
		# context['item'] = 
		if request.GET and request.GET['date']:
			# make a new plan object
			plan = Plan(owner = request.user, plan_date = request.GET['date'], name = request.GET['name'])
			plan.save()
			# get id to retrieve later
			context['id'] = plan.id
			return render(request, 'travelapp/main.html', context)
		else:
			new_plan = Plan.objects.filter(owner = request.user).order_by("-id")[0]
			all_event = Event.objects.filter(plan = new_plan)
			context['events'] = all_event
			context['id'] = new_plan.id
			return render(request, 'travelapp/main.html', context)

	form = SearchForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'travelapp/main.html', context)
	#get keyowrd and city for api use
	keyword = form.cleaned_data['place']
	city = form.cleaned_data['city']
	# url = "https://api.yelp.com/v3/businesses/search?term=delis&location=abcdr3"
	url = 'https://api.yelp.com/v3/businesses/search?'
	query = 'term='+keyword+'&location='+city
	final_url = url+query
	req = urllib2.Request(final_url)
	bearer_token = 'NaMZiXUy2KVRRqz48HE5M6muVGNYVqDuUdeCX-RRpYRZiBO1hSQSxFljQ9mJ8eszW176R2ElQE2_CBggic3bS2q8d77_UlBhsEWtIEG5dH5zQockdelRsXYRGmodWHYx'
	req.add_header('Authorization', 'Bearer '+ bearer_token + '')
	try:
		json_obj = urllib2.urlopen(req)
	except urllib2.HTTPError as err:
		return redirect(reverse('index'))
	# json_obj = urllib2.urlopen(req)
	data = json.load(json_obj)
	#select the five most relevant
	context['foods'] = data['businesses'][:5]
	context['id'] = request.POST['id']
		
	return render(request, 'travelapp/search_result.html', context)
	# return HttpResponse()

@login_required
def add(request):
	context = {}
	period = request.POST['period']
	destination = request.POST['destination']
	url = request.POST['url']
	img = request.POST['img']
	activity = request.POST['activity']
	if period == 'morning':
		order = 1
	elif period == 'noon':
		order = 2
	elif period == 'afternoon':
		order = 3
	elif period == 'evening':
		order = 4
	else:
		order = 5
	id = request.POST['id']
	plan = Plan.objects.get(id=id)
	# create an event
	event = Event(plan=plan, period=period, destination=destination, url=url, img=img, activity=activity, order=order)
	event.save()
	context['id'] = id
	return redirect(reverse('index'))

@login_required
def plan_result(request):
	context= {}
	result_plan = Plan.objects.filter(owner = request.user).order_by("-id")[0]
	all_event = Event.objects.filter(plan = result_plan).order_by("order")
	context['events'] = all_event
	return render(request, 'travelapp/plan_result.html', context)

@login_required
def navigate(request):
	context = {}
	if request.method == 'GET':
		return render(request, 'travelapp/navigation.html', context)
	# create a plan instance
	return redirect(reverse('index'))

@login_required
def tour_pal(request):
	context = {}
	all_plan = Plan.objects.all().order_by("-id")
	context['plans'] = all_plan
	#each plan has a comment form
	context['comment'] = CommentForm()
	context['num_user'] = UserProfile.objects.all().count()
	context['num_plan'] = Plan.objects.all().count()
	context['num_blog'] = Blog.objects.all().count()
	return render(request, 'travelapp/travel_pal.html', context)

@login_required
def add_comment(request,id):
	# if not 'comment' in request.POST or not request.POST['comment']:
 #        raise Http404
 #    else:
	profile = UserProfile.objects.get(user=request.user)
	plan = Plan.objects.get(id=id)
# new_comment = Comment(author=request.user, author_profile=profile, post=item,content=request.POST['comment'])
	new_comment = Comment(author=request.user, author_profile=profile, plan=plan)
        # new_comment.save()
	form = CommentForm(request.POST, instance=new_comment)
	if not form.is_valid():
		return redirect(reverse('tour_pal'))
    
	form.save()
	return redirect(reverse('tour_pal'))

@login_required
def add_review(request,id):
	reviewed = User.objects.get(id=id)
	reviewer_profile = UserProfile.objects.get(user=request.user)
	new_review = Review(reviewed=reviewed, reviewer=request.user, reviewer_profile=reviewer_profile)
        # new_comment.save()
	form = ReviewForm(request.POST, instance=new_review)
	if not form.is_valid():
		return redirect(reverse('profile'))
    
	form.save()
	return redirect(reverse('profile', args=id))

# delete the choosen event
@login_required
def delete_event(request,id):
	event = Event.objects.get(id=id)
	event.delete()

	return redirect(reverse('index'))

# delete the choosen plan
@login_required
def delete_plan(request,id):
	plan = Plan.objects.get(id=id)
	plan.delete()

	return redirect(reverse('my_profile'))

@login_required
def edit_profile(request):
	profile_to_edit = get_object_or_404(UserProfile, user=request.user)
	if request.method == 'GET':
		form = ProfileForm(instance=profile_to_edit)  # Creates form from the 
		context = {'form':form}                       # existing entry.
		return render(request, 'travelapp/edit_profile.html', context)

    # if method is POST, get form data to update the model
	form = ProfileForm(request.POST, request.FILES, instance=profile_to_edit)

	if not form.is_valid():
		context = {'form':form} 
		return render(request, 'travelapp/edit_profile.html', context)
	form.save()
	return redirect(reverse('my_profile'))

@login_required
def icon(request,id):
    profile = get_object_or_404(UserProfile, id=id)
    if not profile.picture:
        raise Http404

    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type)

@login_required
def my_profile(request):
    errors = []
    context = {}
    context['user'] = request.user
    try:
        detail_profile = UserProfile.objects.get(user=request.user)
        context['profile'] = detail_profile
    except ObjectDoesNotExist:
        errors.append('The user did not exist.')

    plans = Plan.objects.filter(owner=request.user).order_by('create_date').reverse()
    context['plans'] = plans
    blogs = Blog.objects.filter(user=request.user).order_by('time').reverse()
    context['blogs'] = blogs
    context['errors'] = errors
    context['review'] = ReviewForm()
    context['comment'] = CommentForm()
    return render(request, 'travelapp/myprofile.html', context)

@login_required
def profile(request, id):
    errors = []
    context = {}
    try:
        user= User.objects.get(id=id)
        context['user'] = user
        profile = UserProfile.objects.get(user=user)
        context['profile'] = profile
    except ObjectDoesNotExist:
        errors.append('The user did not exist.')

    #followed_by = detail_profile.followed_by.all();
    plans = Plan.objects.filter(owner=user).order_by('create_date').reverse()
    context['plans'] = plans
    blogs = Blog.objects.filter(user=user).order_by('time').reverse()
    context['blogs'] = blogs
    context['errors'] = errors
    context['review'] = ReviewForm()
    context['comment'] = CommentForm()
    return render(request, 'travelapp/profile.html', context)

@login_required
def blog(request):
	context = {}
	all_blogs = Blog.objects.all().order_by('time').reverse()
	context['blogs'] = all_blogs
	context['user'] = request.user.username
	# context['find'] = FindForm()
	
	return render(request, 'travelapp/blog_stream.html', context)

@login_required
def new_blog(request):
	context = {}
	if request.method == 'GET':
		context['form'] = BlogForm()
		return render(request, 'travelapp/new_blog.html', context)

	profile = UserProfile.objects.get(user=request.user)
	new_blog = Blog(user=request.user, profile=profile)
	form = BlogForm(request.POST, instance=new_blog)
	if not form.is_valid():
	    context['form'] = BlogForm()
	    return render(request, 'travelapp/new_blog.html', context)
	
	form.save()
	return redirect(reverse('blog'))

@login_required
def search(request):
	context = {}
	if not 'key' in request.POST or not request.POST['key']:
		raise Http404
	else:
		key = request.POST['key']
		related_blogs = Blog.objects.filter(content__contains=key).order_by('time').reverse()
		context['blogs'] = related_blogs
		# context['find'] = FindForm()
		return render(request, 'travelapp/search_blog.html', context)


def register(request):
	context = {}
	# Just display the registration form if this is a GET request
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'travelapp/register.html', context)

	form = RegistrationForm(request.POST)
	context['form'] = form
	# Validates the form.
	if not form.is_valid():
		return render(request, 'travelapp/register.html', context)
	# Creates the new user from the valid form data
	new_user = User.objects.create_user(username=form.cleaned_data['username'], 
	                                    password=form.cleaned_data['password1'],
	                                    email=form.cleaned_data['email'])
	new_user.save()
	#while at the same time, create the profile so that it can be edited later
	new_user_profile = UserProfile(user=new_user)
	new_user_profile.save()
	# Logs in the new user and redirects to main page
	new_user = authenticate(username=form.cleaned_data['username'], 
	                        password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect(reverse('navigate'))
