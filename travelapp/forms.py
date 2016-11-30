from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


from models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20,label='Username',
        widget=forms.TextInput(attrs={'placeholder':"Username", 'class':"form-control"}))
    password = forms.CharField(max_length=200, label='Password',
        widget=forms.PasswordInput(attrs={'placeholder':'Password','class':"form-control"}))

class RegistrationForm(forms.Form):
	#the elements user has to provide
    username = forms.CharField(max_length = 20,
    			             label = 'Username', widget=forms.TextInput(attrs={'placeholder':"Username", 'class': 'form-control'}))
    # email = forms.CharField(label = 'E-mail', widget=forms.TextInput(attrs={'placeholder':"E-mail",'class': 'form-control'}))
    email = forms.CharField(max_length = 100, label='Email', widget = forms.EmailInput())
    password1 = forms.CharField(max_length = 200,
                                label = 'Password',
                                widget = forms.PasswordInput(attrs={'placeholder':"Password",'class': 'form-control'}))
    password2 = forms.CharField(max_length = 200,
                                label = 'Confirm Password',
                                widget = forms.PasswordInput(attrs={'placeholder':"Confirm Password",'class': 'form-control'}))

    #validations here.
    #overides the clean function, all fields are required as default unless marked as false
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_username(self):
    	# Are called after the general clean function
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username




class SearchForm(forms.Form):
    #the element user has to provide
    place = forms.CharField(max_length = 20,
                            label = "Want to visit")
    city = forms.CharField(max_length = 20,
                            label = "in the city of")
    #validations here,indeed no validation, api will take care of it
    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        return cleaned_data

# class FindForm(forms.Form):
#     #the element user has to provide
#     key = forms.CharField(max_length = 20)
#     #validations here,indeed no validation, api will take care of it
#     def clean(self):
#         cleaned_data = super(SearchForm, self).clean()

#         return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'];

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        content = cleaned_data.get('content')
        if len(content) > 420:
            raise forms.ValidationError("the comment should be less 420 characters")

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content'];

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()
        content = cleaned_data.get('content')
        if len(content) > 420:
            raise forms.ValidationError("the review should be less 420 characters")
        return cleaned_data


# need further stuff on validation
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        widgets = {'picture' : forms.FileInput() }

    def clean(self):

        cleaned_data = super(ProfileForm, self).clean()

        text = cleaned_data.get('bio')
        if len(text) > 420:
            raise forms.ValidationError("the bio can't be longer than 420 characters")

        return cleaned_data

# the blog uer is posting
class BlogForm(forms.ModelForm):
    #inherite from model class
    class Meta:
        model = Blog
        exclude = ('user','time','profile')
        widgets = {
            'content': forms.TextInput(
                attrs={'id': 'post-text', 'required': True}
            ),
        }
    #check if the text is more than 42 characters
    def clean(self):
        
        cleaned_data = super(BlogForm, self).clean()

        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if len(title) > 50:
            raise forms.ValidationError("the post can't be longer than 50 characters")
        if len(content) > 500:
            raise forms.ValidationError("the post can't be longer than 500 characters")
        return cleaned_data
