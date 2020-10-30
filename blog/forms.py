from django import forms
from .models import post, Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

class PostCreateForm(forms.ModelForm):
	class Meta:
		model = post
		fields = (
			'title',
			'body',
			'status',
			)


class userloginform(forms.Form):
	username = 	forms.CharField(label="")
	password = forms.CharField(label="", widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UserEditForm(forms.ModelForm):
	username =forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	email =forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	class Meta:
		model =User
		fields = {
			'username',
			'first_name',
			'last_name',
			'email',
		}

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = {'user',}