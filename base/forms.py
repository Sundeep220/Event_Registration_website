from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'avatar', 'bio', 'twitter', 'linkedin', 'website' ,'facebook' ,'github']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-field--input'}),
            'name':forms.TextInput(attrs={'class':'form-field--input'}),
            'email':forms.EmailInput(attrs={'class':'form-field--input'}),
            'bio':forms.Textarea(attrs={'class':'form-field--input-txarea'}),
            'twitter': forms.TextInput(attrs={'class':'form-field--input'}),
            'linkedin':forms.TextInput(attrs={'class':'form-field--input'}),
            'facebook':forms.TextInput(attrs={'class':'form-field--input'}),
            'github':forms.TextInput(attrs={'class':'form-field--input'}),
            'website':forms.TextInput(attrs={'class':'form-field--input'})
        }


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['details', 'project_url']
        widgets = {
            'details': forms.Textarea(attrs={'class':'form-field--input-txarea'}),
            'project_url' : forms.TextInput(attrs={'class':'form-field--input'})
        }

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-field--input'}),
            'name':forms.TextInput(attrs={'class':'form-field--input'}),
            'email':forms.EmailInput(attrs={'class':'form-field--input'})
        }
