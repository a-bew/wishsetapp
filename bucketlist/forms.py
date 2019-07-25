from django import forms
#from django.forms import ModelForm
#from .models import Page, Category
from .models import Tbl_wish
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
	  	  model = User
	  	  fields = ('username', 'email', 'password')

#class UserProfileForm(forms.ModelForm):
#    	username = forms.CharField(help_text="Please enter a name.")

#	class Meta:
#		model = UserProfile
#		fields = ('username',)

class Tbl_wishForm(forms.ModelForm):
    wish_title = forms.CharField(help_text="Please enter a title.")
    wish_description = forms.CharField(widget=forms.Textarea)
    wish_date = forms.DateField(widget=forms.HiddenInput(), required=False)
    class Meta:

        model = Tbl_wish
        fields = ['wish_title', 'wish_description','wish_date']
        exclude = ('user',)
