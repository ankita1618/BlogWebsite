from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm, userloginform,SignUpForm ,UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import post, Profile
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# def index(request):
# 	# print(dir(request))
# 	return HttpResponse("Hello World 1st view")

# def current_datetime(request):
# 	html = "<html><body>Calander and Clock say it's <b>%s</b> </body></html>" %datetime.now()
# 	return HttpResponse(html)


def post_list(request):
	post_list=post.published.all().order_by('-id')
	query = request.GET.get('q')
	if query:
		post_list =post.published.filter(     			#title__icontains=query)
		Q(title__icontains=query)|
		Q(author__username=query)|
		Q(body__icontains=query)
		)	
	paginator= Paginator(post_list, 4)
	page=request.GET.get('page')
	try:
		posts=paginator.page(page)
	except PageNotAnInteger:
		posts= paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	if page is None:
		start_index = 0
		end_index= 5
	else:
		(start_index,end_index)=proper_pagination(posts, index=3)
	
	page_range=list(paginator.page_range)[start_index:end_index]
	[]

	   			
	context = {
		'pposts' : posts,
		'page_range': page_range,
	}
	return render(request, 'blog/post_list.html',context)

def proper_pagination(posts,index):
	start_index=0
	end_index=4
	if posts.number>index:
		start_index = posts.number - index
		end_index =start_index +end_index
	return (start_index,end_index)

def post_detail(request,id):
	POST=get_object_or_404(post,id=id)
	context = {
		'post': POST,
	}
	return render(request, 'blog/post_detail.html', context)

def post_create(request):
	if request.method =='POST':
		form = PostCreateForm(request.POST)
		if form.is_valid():
			post =form.save(commit=False)
			post.author= request.user
			post.save()
	else:
		form =PostCreateForm()
	context={
	'form': form,
	}
	return render(request, 'blog/post_create.html', context)

def user_login(request):
	if request.method =='POST':
		form= userloginform(request.POST)
		if form.is_valid():
			username =request.POST['username']
			password=request.POST['password']
			user =authenticate(username=username,password=password)
			if user:
				if user.is_active:
					login(request,user)
					return HttpResponseRedirect(reverse('post_list'))
				else:
					return HttpResponse("User id Deactive")
			else:
				return HttpResponse("User is not signed in")
	else:
		form =userloginform()
		context = {
		'form':form,
		}
		return render(request, 'blog/login.html',context)




def user_logout(request):
	logout(request)
	return redirect('post_list')
	# return HttpResponseRedirect(reverse('post_list'))


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			raw_password=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=raw_password)
			Profile.objects.create(user=user)
			login(request,user)
			return redirect('post_list')
	else:
		form=SignUpForm()
	return render(request, 'registration/signup.html',{'form':form})

@login_required
def edit_profile(request):
	if request.method == 'POST':
		user_form =UserEditForm(data=request.POST or None, instance=request.user)
		profile_form=ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return HttpResponseRedirect(reverse("blog:edit_profile"))
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form=ProfileEditForm(instance=request.user.profile)

	context = {
		'user_form': user_form,
		'profile_form': profile_form,
	}
	return render(request , 'blog/edit_profile.html',context)

def like_post (request):
	postt= get_object_or_404(post,id=request.POST.get('post_id'))
	postt.likes.add(request.user)
	return HttpResponseRedirect(postt.get_absolute_url())