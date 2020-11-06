from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import Profile,Feedback
from posts.models import Comment
from validate_email import validate_email
from django.forms.widgets import PasswordInput,TextInput
import requests
# from django.core.validators import validate_email

class CreateUserForm(UserCreationForm):
    email=forms.EmailField(widget=TextInput(attrs={'placeholder':'Email'}),required=True)
    username=forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder':'Username'}))
    password1=forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    password2=forms.CharField(widget=PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password1',
            'password2'
        ]
    def clean_email(self,*args,**kwargs):
        cleaned_data = super(CreateUserForm, self).clean()
        email = cleaned_data.get("email")
        
        response = requests.get("https://apilayer.net/api/check?access_key=a448482d0743db46d06084a7c97f32c9&email={}".format(email))
        dic = response.json()
        if dic['smtp_check']==True and dic['format_valid']==True and dic['mx_found']==True:
            return email
        else:
            raise forms.ValidationError("Invalid Email")



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model=User
        fields=[
            'username',           
        ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        bio = forms.CharField(required=False)
        # name = forms.CharField(default =User.username)
        model=Profile
        fields=[
            'profilepic',
            'bio',
            'name'
        ]

class login(AuthenticationForm):
    username=forms.CharField(label=None,widget=TextInput(attrs={'class':'validate','placeholder':'Username'}))
    password=forms.CharField(label=None,widget=PasswordInput(attrs={'class':'password','placeholder':'Password'}))

class CommentForm(forms.ModelForm):
    content = forms.CharField(label=None,widget=forms.Textarea(attrs={'placeholder':' \n Add Comment'}),required=True)
    class Meta :
        model = Comment
        fields = ['content']
        
class FeedbackForm(forms.ModelForm):
    content = forms.CharField(label=None,widget=forms.Textarea(attrs={'placeholder':' \n Write Your Feedback'}),required=True)

    class Meta:
        model = Feedback
        fields = ['content']
    